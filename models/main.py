import os
import torch

os.environ["OMP_NUM_THREADS"] = "1"
torch.set_num_threads(1)

import numpy as np
from datetime import datetime
from models.model import MedicalModel
import faiss
from models.embedding import embedding_model
from models.doctor_match import match_doctor
from sentence_transformers import SentenceTransformer

print("[INIT] Import complete. Initializing models...")

medical_model = MedicalModel()
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
print("[INIT] Embedding model loaded: all-MiniLM-L6-v2")

conversation_history = {
    "user": [],
    "assistant": []
}
print("[INIT] Conversation history initialized.")

def match_doctor_route():
    print("[ROUTE] match_doctor_route called.")
    user_input = ""
    for line in conversation_history["user"]:
        user_input += line.strip()
    print(f"[DEBUG] Compiled user input: {user_input}")

    if not user_input:
        print("[ERROR] No input found in conversation history.")
        return jsonify({"error": "No input provided"}), 400

    doctor_suggestions = match_doctor(user_input)
    print(f"[DEBUG] Doctor suggestions: {doctor_suggestions}")
    return jsonify({"matches": doctor_suggestions})


index = faiss.IndexFlatL2(384)
print("[INIT] FAISS index initialized with dimension 384.")


def log_entry(speaker, message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_msg = f"[{timestamp}] {message}"
    print(f"[LOG] {speaker.upper()} >> {log_msg}")
    conversation_history[speaker].append(log_msg)


def load_history(index, path="conversation_history.txt"):
    print(f"[LOAD] Attempting to load history from {path}")
    try:
        with open(path, "r") as file:
            lines = file.readlines()
            for line in lines:
                message = line.strip()
                if message:
                    conversation_history["user"].append(message)
                    input_embedding = embedding_model.encode(message)
                    index.add(np.array([input_embedding]))
                    print(f"[LOAD] Added to FAISS and history: {message}")

        print(f"[LOAD] Total loaded messages: {len(conversation_history['user'])}")
    except FileNotFoundError:
        print(f"[WARN] No existing history at {path}. Starting fresh.")


def write_history(path="conversation_history.txt"):
    print(f"[SAVE] Writing conversation history to {path}")
    try:
        with open(path, "w") as file:
            for message in conversation_history["user"]:
                file.write(f"{message}\n")
        print(f"[SAVE] Successfully saved {len(conversation_history['user'])} messages.")
    except Exception as e:
        print(f"[ERROR] Failed to save history: {e}")


def create_faiss_index():
    print("[FAISS] Creating new FAISS index.")
    index = faiss.IndexFlatL2(384)
    print("[FAISS] New FAISS index created.")
    return index


def retrieve_context(query, top_k=2):
    print(f"[RETRIEVE] Retrieving context for query: {query}")
    query_embedding = np.array([embedding_model.encode(query)])
    print("[RETRIEVE] Query embedding generated.")

    if not os.path.exists("retrieval_index.faiss"):
        print("[RETRIEVE] Index file not found. Creating a blank one.")
        index = faiss.IndexFlatL2(384)
        faiss.write_index(index, "retrieval_index.faiss")

    retrieval_index = faiss.read_index("retrieval_index.faiss")
    print(f"[RETRIEVE] Index loaded. Total entries: {retrieval_index.ntotal}")

    if retrieval_index.ntotal == 0:
        print("[RETRIEVE] Index is empty.")
        return "No relevant documents found."

    try:
        distances, indices = retrieval_index.search(query_embedding, top_k)
    except RuntimeError as e:
        print("[RETRIEVE] FAISS search error:", e)
        return "No relevant documents found."
        
    print(f"[RETRIEVE] Distances: {distances[0]}, Indices: {indices[0]}")
    retrieved_docs = [conversation_history["user"][i] for i in indices[0] if i < len(conversation_history["user"])]
    print(f"[RETRIEVE] Retrieved docs: {retrieved_docs}")
    return "\n".join(retrieved_docs) if retrieved_docs else "No relevant documents found."


def update_conversation(user_input, model_response, index):
    print(f"[UPDATE] Updating conversation history and FAISS index.")
    log_entry("user", user_input)
    log_entry("assistant", model_response)

    input_embedding = embedding_model.encode(user_input)
    index.add(np.array([input_embedding]))
    print("[UPDATE] FAISS index updated with new user input.")

    if not os.path.exists("retrieval_index.faiss"):
        print("[UPDATE] Saving updated FAISS index to file.")
        faiss.write_index(index, "retrieval_index.faiss")


def ask(question):
    print(f"[ASK] Question received: {question}")
    retrieved_info = retrieve_context(question)
    print(f"[ASK] Retrieved context: {retrieved_info}")

    prompt = f"""
        You are a helpful medical assistant. Give a relevant and specific follow-up question. Do not diagnose. Be clear and reassuring.
        Medical question: {question}
        Previous medical info: {retrieved_info}
        Answer:
    """
    print("[ASK] Prompt sent to LLM.")
    response = medical_model.llm(prompt, max_tokens=50)['choices'][0]['message']['content']
    print(f"[ASK] Response received from model: {response}")
    update_conversation(question, response, index)
    return response


def submit_symptoms():
    print("[ROUTE] submit_symptoms called.")
    data = request.get_json()
    print(f"[INPUT] Raw JSON: {data}")
    symptoms = data.get("symptoms", "").strip()
    print(f"[INPUT] Extracted symptoms: '{symptoms}'")

    if not symptoms:
        print("[ERROR] No symptoms provided.")
        return jsonify({"error": "No symptoms provided"}), 400

    response_text = ask(symptoms)
    print(f"[OUTPUT] Generated response: {response_text}")

    update_conversation(symptoms, response_text)
    print("[ROUTE] Conversation updated.")

    response = {
        "message": "Symptoms received and processed successfully.",
        "response": response_text
    }

    print("[ROUTE] Returning response JSON.")
    return jsonify(response)