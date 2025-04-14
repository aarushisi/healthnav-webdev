import sqlite3
from flask import Flask, request, jsonify, send_from_directory
import models.main as main
import models.doctor_match as docmatch
from datetime import datetime
import re

app = Flask(__name__, static_folder=".")

# Temporary in-memory storage (to be replaced with a database)
user_data_store = []
symptom_data_store = {}  # Store symptoms per user session
follow_up_store = {}

def get_db_connection():
    conn = sqlite3.connect("healthnav.db")
    conn.row_factory = sqlite3.Row  # Allows dictionary-like row access
    return conn

### Serve Frontend Files ###
@app.route("/")
def serve_index():
    return send_from_directory(".", "index.html")

@app.route("/<path:path>")
def serve_static_files(path):
    return send_from_directory(".", path)

### Store User Data ###
@app.route("/submit", methods=["POST"])
def save_user_data():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON received"}), 400

        if not data.get("name"):
            data["name"] = "Anonymous"

        age = data.get("age", None)
        if age is None or not (0 <= int(age) <= 120):
            return jsonify({"error": "Invalid age. Must be between 0 and 120."}), 400

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO users (name, age, gender, insurance, street, city, state, zip) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (data["name"], data["age"], data["gender"], data["insurance"],
            data["street"], data["city"], data["state"], data["zip"]))
        conn.commit()
        conn.close()

        print("User data received:", data)
        return jsonify({"message": "User data received successfully"}), 200
    except Exception as e:
        print("Error:", e)
        return jsonify({"error": "Internal Server Error"}), 500

### Store Follow-Up & Generate Diagnosis ###
@app.route("/followup-arrow", methods=["POST"])
def followup_arrow():
    print("[FLASK] /followup-arrow route hit.")
    try:
        data = request.get_json()
        print(f"[FLASK] Incoming data: {data}")

        symptoms = data.get("symptoms", "").strip()
        if not symptoms:
            print("[FLASK] No symptoms provided.")
            return jsonify({"error": "No symptoms provided"}), 400

        print(f"[FLASK] Calling main.ask() with symptoms: {symptoms}")
        response = main.ask(symptoms)

        print(f"[FLASK] Response from main.ask(): {response}")
        return jsonify({"followup_response": response}), 200
    except Exception as e:
        print(f"[FLASK ERROR] Exception in /followup-arrow: {e}")
        return jsonify({"error": "Internal Server Error"}), 500

@app.route("/conversation-status", methods=["GET"])
def conversation_status():
    has_user_input = len(main.conversation_history["user"]) > 0
    return jsonify({"has_user_input": has_user_input})

### Retrieve User & Symptom Data for Display ###
@app.route("/get-user-data", methods=["GET"])
def get_user_data():
    conn = get_db_connection()
    cursor = conn.cursor()
    user = cursor.execute("SELECT * FROM users ORDER BY id DESC LIMIT 1").fetchone()
    conn.close()

    if not user:
        return jsonify({"error": "No user data available"}), 404

    user_dict = dict(user)

    symptom_info = symptom_data_store.get("default", {})
    user_dict["symptoms"] = symptom_info.get("symptoms", "Not provided")

    return jsonify(user_dict), 200

@app.route("/submit-symptoms", methods=["POST"])
def submit_symptoms():
    try:
        data = request.get_json()
        if data is None:
            return jsonify({"error": "No JSON received"}), 400

        textbox_symptoms = data.get("symptoms", "").strip()
        chat_history = main.conversation_history["user"]

        extra_input = ""
        if textbox_symptoms:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            extra_input = f"[{timestamp}] {textbox_symptoms}"

        # Combine everything together
        full_input = "\n".join(chat_history)
        if extra_input:
            full_input += f"\n{extra_input}"

        if not full_input.strip():
            return jsonify({"error": "No symptoms to submit"}), 400

        # Save the complete set into the in-memory store
        symptom_data_store["default"] = {"symptoms": full_input.strip()}
        print(f"[SYMPTOM SUBMIT] Full symptoms saved:\n{full_input}")
        return jsonify({"message": "Full symptoms submitted"}), 200

    except Exception as e:
        print("[ERROR] Exception in /submit-symptoms:", e)
        return jsonify({"error": "Internal Server Error"}), 500

def format_phone_number(phone):
    phone_digits = re.sub(r'\D', '', str(phone))
    if len(phone_digits) == 10:
        return f"({phone_digits[:3]}) {phone_digits[3:6]}-{phone_digits[6:]}"
    return phone

@app.route("/get-doctors", methods=["GET"])
def get_doctors():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Fetch user info
        user = cursor.execute("SELECT age, city, state FROM users ORDER BY id DESC LIMIT 1").fetchone()
        if not user:
            conn.close()
            return jsonify({"error": "No user data available"}), 404

        age = int(user["age"])
        city = user["city"].strip().upper()
        state = user["state"].strip().upper()

        # Try fetching the predicted specialty
        try:
            user_input = "\n".join(main.conversation_history["user"])
            predicted_specialty = docmatch.match_doctor(user_input, top_k=1)[0]["specialty"]
            print(f"[SPECIALTY] Using predicted specialty: {predicted_specialty}")
        except Exception as e:
            print("[FALLBACK] Error getting specialty from model. Defaulting to internal medicine.")
            predicted_specialty = "Internal Medicine"

        # Query for doctors with predicted specialty
        query = "SELECT * FROM doctors WHERE city = ? AND state = ? AND specialty LIKE ?"
        doctors = cursor.execute(query, (city, state, f"%{predicted_specialty}%")).fetchall()

        # If no doctors found, apply fallback
        if len(doctors) == 0:
            fallback_specialty = "Pediatrics" if age < 18 else "General Practice"
            print(f"[FALLBACK] No matches. Using fallback specialty: {fallback_specialty}")
            doctors = cursor.execute(query, (city, state, f"%{fallback_specialty}%")).fetchall()

        conn.close()

        doctor_list = []
        for doc in doctors:
            doctor_dict = dict(doc)
            doctor_dict["phone"] = format_phone_number(doctor_dict.get("phone", ""))
            doctor_list.append(doctor_dict)

        return jsonify(doctor_list), 200

    except Exception as e:
        print("[ERROR] Exception in /get-doctors:", e)
        return jsonify({"error": "Internal Server Error"}), 500


@app.route("/get-specialty", methods=["GET"])
def get_specialty():
    try:
        user_input = "\n".join(main.conversation_history["user"])
        if not user_input:
            return jsonify({"error": "No symptom input available"}), 400
        
        top_specialty = docmatch.match_doctor(user_input, top_k=1)[0]["specialty"]
        print(f"[SPECIALTY] Predicted top specialty: {top_specialty}")
        return jsonify({"specialty": top_specialty})
    except Exception as e:
        print("[ERROR] Exception in /get-specialty:", e)
        return jsonify({"error": "Internal Server Error"}), 500

@app.route("/clear-history", methods=["POST"])
def clear_history():
    try:
        main.conversation_history["user"].clear()
        main.conversation_history["assistant"].clear()
        print("[CLEAR] Conversation history cleared.")
        return jsonify({"message": "Conversation history cleared"}), 200
    except Exception as e:
        print("[ERROR] Failed to clear history:", e)
        return jsonify({"error": "Failed to clear history"}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5002, use_reloader=False)