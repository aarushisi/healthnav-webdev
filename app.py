from flask import Flask, request, jsonify, send_from_directory  # Correct import

app = Flask(__name__, static_folder="frontend")

@app.route("/")
def serve_index():
    return send_from_directory("frontend", "index.html")

@app.route("/<path:path>")
def serve_static_files(path):
    return send_from_directory("frontend", path)

# Temporary in-memory storage (to be replaced with a database)
user_data_store = []

@app.route("/submit", methods=["POST"])
def save_user_data():
    try:
        data = request.get_json()  # Correct JSON extraction
        if not data:
            return jsonify({"error": "No JSON received"}), 400

        user_data_store.append(data)  # Store temporarily
        print("User data received:", data)  # Debugging/logging
        return jsonify({"message": "User data received successfully"}), 200
    except Exception as e:
        print("Error:", e)
        return jsonify({"error": "Internal Server Error"}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)
