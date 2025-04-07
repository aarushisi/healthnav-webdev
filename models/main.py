from flask import Flask, request, jsonify
import faiss
import numpy as np
from datetime import datetime
from models.model import medical_model
from models.embedding import embedding_model
from models.doctor_match import match_doctor

app = Flask(__name__)


# Per-user FAISS index storage
conversation_history = {
    "user": [],
    "assistant": []
}

@app.route('/match-doctor', methods=['POST'])
def match_doctor_route():
    user_input = ""
    for line in conversation_history["user"]:
        user_input += line.strip()

    if not user_input:
        return jsonify({"error": "No input provided"}), 400

    doctor_suggestions = match_doctor(user_input)
    return jsonify({"matches": doctor_suggestions})

# WARNING! GLOBAL VARIABLE FOR USE OF DEMO!
# Proper version should have different indexes for each user.
index = faiss.IndexFlatL2(384)

def log_entry(speaker, message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conversation_history[speaker].append(f"[{timestamp}] {message}")

def load_history(index, path="conversation_history.txt"):
    """Loads previous user messages from .txt file."""
    try:
        with open(path, "r") as file:
            lines = file.readlines()
            for line in lines:
                message = line.strip()
                if message:
                    conversation_history["user"].append(message)

                    # Update the FAISS index with the loaded message embedding
                    input_embedding = embedding_model.encode(message)
                    index.add(np.array([input_embedding]))

        print(f"Loaded {len(conversation_history['user'])} messages from {path}")
    except FileNotFoundError:
        print(f"No existing history found at {path}. Starting fresh.")

def write_history(path="conversation_history.txt"):
    """Writes all messages in user_history to a .txt file."""
    try:
        with open(path, "w") as file:
            for message in conversation_history["user"]:
                file.write(f"{message}\n")
        print(f"Successfully saved {len(conversation_history['user'])} messages to {path}")
    except Exception as e:
        print(f"Error saving history: {e}")

def create_faiss_index():
    """Creates a new FAISS index for a user."""
    index = faiss.IndexFlatL2(384)  # 384 is the embedding size for all-MiniLM-L6-v2
    return index

# WARNING! Future version needs to account for multiple users!
# For demo build, one user is ok
def retrieve_context(query, top_k=2):
    """Retrieves relevant past conversations for a user."""
    query_embedding = np.array([embedding_model.encode(query)])

    # Load FAISS index into a separate variable
    retrieval_index = faiss.read_index("retrieval_index.faiss")

    if retrieval_index.ntotal == 0:
        return "No relevant documents found."
    
    distances, indices = retrieval_index.search(query_embedding, top_k)
    retrieved_docs = [conversation_history["user"][i] for i in indices[0] if i < len(conversation_history["user"])]
    return "\n".join(retrieved_docs) if retrieved_docs else "No relevant documents found."

# WARNING! Future version needs to account for multiple users!
# For demo build, one user is ok
def update_conversation(user_input, model_response):
    log_entry("user", user_input)
    log_entry("assistant", model_response)

    # Update FAISS with user input or conversation pair
    input_embedding = embedding_model.encode(user_input)
    index.add(np.array([input_embedding]))
    # Save updated FAISS index
    faiss.write_index(index, "retrieval_index.faiss")

# WARNING! Future version needs to account for multiple users!
# For demo build, one user is ok
def ask(question):
    """Generates a medical response using the LLaMA model."""
    retrieved_info = retrieve_context(question)
    prompt = f"""
        You are an expert caretaker helping patients find a doctor. You are not allowed to formally diagnose the patient, however you want to help patients however you can.
        You will ask the patient what kind of doctor they are looking for, and want to get them the doctor that is the best fit for them.
        You also want to make sure that you help the patient with whatever pain or discomfort they are feeling. Help them however you can without giving them a reason to panic or be afraid.
        Medical question: {question}
        Previous medical info: {retrieved_info}
        Answer:
    """
    response = medical_model.llm(prompt, max_tokens=500)['choices'][0]['message']['content']
    update_conversation(question, response, index)
    return response


@app.route('/submit-symptoms', methods=['POST'])
def submit_symptoms():
    """Receives symptoms from the frontend and processes them."""
    data = request.get_json()
    symptoms = data.get("symptoms", "").strip()

    if not symptoms:
        return jsonify({"error": "No symptoms provided"}), 400
    
    # WARNING! 
    # Because demo does not account for multiple users or leaving the site,
    # load_history(index) does not work properly.
    # write_history does but not yet

    response_text = ask(symptoms)

    update_conversation(symptoms, response_text)
    
    response = {
        "message": "Symptoms received and processed successfully.",
        "response": response_text
    }

    return jsonify(response)

if __name__ == "__main__":
    app.run(debug=True)