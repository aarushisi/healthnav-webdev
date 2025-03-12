from flask import Flask, request, jsonify, send_from_directory

app = Flask(__name__, static_folder="frontend")

# Temporary in-memory storage (to be replaced with a database)
user_data_store = []
symptom_data_store = []  # New list to store symptoms

@app.route("/")
def serve_index():
    return send_from_directory("frontend", "index.html")

@app.route("/<path:path>")
def serve_static_files(path):
    return send_from_directory("frontend", path)

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

# ✅ FIX: Add the correct POST method for /submit-symptoms
@app.route("/submit-symptoms", methods=["POST"])
def save_symptoms():
    try:
        data = request.get_json()
        if not data or "symptoms" not in data:
            return jsonify({"error": "No symptoms received"}), 400

        symptom_data_store.append(data)
        print("Symptoms received:", data)
        return jsonify({"message": "Symptoms stored successfully"}), 200
    except Exception as e:
        print("Error:", e)
        return jsonify({"error": "Internal Server Error"}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)
