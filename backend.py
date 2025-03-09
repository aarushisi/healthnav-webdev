from flask import Flask, request, jsonify

app = Flask(__name__)

# fake database for doctors to test
doctors_db = [
    {"name": "Dr. Alice", "specialty": "Cardiology", "insurance": "Cigna"},
    {"name": "Dr. Bob", "specialty": "Dermatology", "insurance": "Aetna"},
    {"name": "Dr. Charlie", "specialty": "Neurology", "insurance": "Blue Cross Blue Shield"},
    {"name": "Dr. David", "specialty": "Pediatrics", "insurance": "United Healthcare"}
]

@app.route('/search_doctors', methods=['POST'])
def search_doctors():
    data = request.get_json()

    name = data.get('name', '')
    age = data.get('age', 0)
    gender = data.get('gender', '')
    insurance = data.get('insurance', '')
    symptoms = data.get('symptoms', '')

    # just matching doctors on insurance right now to test flask api endpoint
    matched_doctors = [doctor for doctor in doctors_db if doctor['insurance'] == insurance]

    if not matched_doctors:
        return jsonify({"message": "No doctors found for your insurance provider."}), 404

    return jsonify(matched_doctors)

if __name__ == '__main__':
    app.run(debug=True)
