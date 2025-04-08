import sqlite3
from flask import Flask, request, jsonify, send_from_directory
import models.main as main

app = Flask(__name__, static_folder=".")

# Temporary in-memory storage (to be replaced with a database)
user_data_store = []
symptom_data_store = {}  # Store symptoms per user session
follow_up_store = {}

def get_db_connection():
    conn = sqlite3.connect("healthnav.db")
    conn.row_factory = sqlite3.Row  # Allows dictionary-like row access
    return conn

### 🏠 Serve Frontend Files ###
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

### Store Symptoms & Generate Follow-Up ###
@app.route("/submit-symptoms", methods=["POST"])
def save_symptoms():
    try:
        data = request.get_json()
        user_id = data.get("user_id", "default")  # Temporary user session handling
        symptoms = data["symptoms"]

        if user_id not in symptom_data_store:
            symptom_data_store[user_id] = {"symptoms": symptoms, "followups": []}
            follow_up_store[user_id] = {"count": 0}

        # Generate a follow-up question
        followup_question = generate_followup(symptoms)
        return jsonify({"followup_question": followup_question}), 200
    except Exception as e:
        print("Error:", e)
        return jsonify({"error": "Internal Server Error"}), 500

### Store Follow-Up & Generate Diagnosis ###
@app.route("/submit-followup", methods=["POST"])
def save_followup():
    try:
        data = request.get_json()
        user_id = data.get("user_id", "default")
        followup_response = data["followup_response"]

        # Store follow-up response
        if user_id in symptom_data_store:
            symptom_data_store[user_id]["followups"].append(followup_response)
            follow_up_store[user_id]["count"] += 1

            # After 2 follow-ups, analyze symptoms for diagnosis
            if follow_up_store[user_id]["count"] >= 2:
                full_response = " ".join([symptom_data_store[user_id]["symptoms"]] + symptom_data_store[user_id]["followups"])
                diagnosis = analyze_medical_terms(full_response)
                return jsonify({"diagnosis": diagnosis}), 200
            else:
                followup_question = generate_followup(followup_response)
                return jsonify({"followup_question": followup_question}), 200

        return jsonify({"error": "User not found"}), 400
    except Exception as e:
        print("Error:", e)
        return jsonify({"error": "Internal Server Error"}), 500

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

    # ✅ Quick fix: Add symptom data from in-memory store
    symptom_info = symptom_data_store.get("default", {})
    user_dict["symptoms"] = symptom_info.get("symptoms", "Not provided")

    return jsonify(user_dict), 200

@app.route("/get-doctors", methods=["GET"])
def get_doctors():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Fetch latest user data to get their city and state
        user = cursor.execute("SELECT city, state FROM users ORDER BY id DESC LIMIT 1").fetchone()

        if not user:
            conn.close()
            return jsonify({"error": "No user data available"}), 404

        user_city = user["city"].strip().upper()  # Normalize city input
        user_state = user["state"].strip().upper()  # Normalize state input

        # Fetch doctors only from the same city and state
        doctors = cursor.execute(
            "SELECT * FROM doctors WHERE city = ? AND state = ? LIMIT 10",
            (user_city, user_state)
        ).fetchall()

        conn.close()

        # Convert results to JSON format
        return jsonify([dict(doc) for doc in doctors]), 200
    except Exception as e:
        print("Error:", e)
        return jsonify({"error": "Internal Server Error"}), 500


if __name__ == "__main__":
    app.run(debug=True, port=5000, use_reloader=False)