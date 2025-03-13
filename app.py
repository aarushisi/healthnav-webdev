from flask import Flask, request, jsonify, send_from_directory

app = Flask(__name__, static_folder="")

# Temporary in-memory storage (to be replaced with a database)
user_data_store = []
symptom_data_store = {}  # Store symptoms per user session
follow_up_store = {}

### 🏠 Serve Frontend Files ###
@app.route("/")
def serve_index():
    return send_from_directory("frontend", "index.html")

@app.route("/<path:path>")
def serve_static_files(path):
    return send_from_directory("frontend", path)

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

        user_data_store.append(data)
        print("User data received:", data)
        return jsonify({"message": "User data received successfully"}), 200
    except Exception as e:
        print("Error:", e)
        return jsonify({"error": "Internal Server Error"}), 500

### Helper Functions ###
def generate_followup(symptoms):
    """ Temporary function to generate a follow-up question based on symptoms. """
    return "Can you describe the pain in more detail?"  # Placeholder

def analyze_medical_terms(full_response):
    """ Temporary function to analyze symptoms and suggest a specialty. """
    return "You may need to see an orthopedic specialist."  # Placeholder

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
    if not user_data_store:
        return jsonify({"error": "No user data available"}), 404

    latest_user = user_data_store[-1]  # Get most recent user
    user_id = "default"  # Temporary session handling
    latest_symptoms = symptom_data_store.get(user_id, {}).get("symptoms", "No symptoms provided")
    followups = symptom_data_store.get(user_id, {}).get("followups", [])

    user_info = {
        "name": latest_user.get("name", "Anonymous"),
        "age": latest_user.get("age", "N/A"),
        "gender": latest_user.get("gender", "N/A"),
        "insurance": latest_user.get("insurance", "N/A"),
        "symptoms": latest_symptoms,
        "followups": followups
    }
    return jsonify(user_info), 200

if __name__ == "__main__":
    app.run(debug=True, port=5000)
