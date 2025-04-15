import os
from dotenv import load_dotenv
load_dotenv()

import google.generativeai as genai
import torch
import time
from concurrent.futures import ThreadPoolExecutor, wait, FIRST_COMPLETED

os.environ["OMP_NUM_THREADS"] = "4"
torch.set_num_threads(4)

import numpy as np
from datetime import datetime
from models.model import MedicalModel
import faiss
from models.embedding import embedding_model
from models.doctor_match import match_doctor

print("[INIT] Import complete. Initializing models...")

medical_model = MedicalModel()
#embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
#print("[INIT] Embedding model loaded: all-MiniLM-L6-v2")

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
    # DO NOT MODIFY the user's 'question' here!

    # --- Build Chronological History String with Llama 3 Template ---
    conversation_history_prompt = ""
    user_hist = conversation_history["user"]
    asst_hist = conversation_history["assistant"]
    len_user = len(user_hist)
    len_asst = len(asst_hist)

    # --- Prepend the initial implicit exchange ONLY if history is empty ---
    is_first_exchange = (len_user == 0 and len_asst == 0)
    if is_first_exchange:
        print("[ASK] First exchange, prepending implicit 'Describe Symptoms' interaction.")
        conversation_history_prompt += "<|start_header_id|>assistant<|end_header_id|>\n\nPlease describe your symptoms.<|eot_id|>\n"
    else:
        # --- Build history for subsequent turns ---
        history_limit = 5
        start_index = max(0, max(len_user, len_asst) - history_limit)
        for i in range(start_index, max(len_user, len_asst)):
            if i < len_user:
                user_msg = user_hist[i].split('] ', 1)[-1].strip()
                conversation_history_prompt += f"<|start_header_id|>user<|end_header_id|>\n\n{user_msg}<|eot_id|>"
            if i < len_asst:
                asst_msg = asst_hist[i].split('] ', 1)[-1].strip()
                conversation_history_prompt += f"<|start_header_id|>assistant<|end_header_id|>\n\n{asst_msg}<|eot_id|>"
        if conversation_history_prompt:
             conversation_history_prompt += "\n"

    print(f"[ASK] Constructed templated history snippet (last 500 chars):\n...{conversation_history_prompt[-500:]}")

    prompt = f"<|begin_of_text|><|start_header_id|>system<|end_header_id|>\n\nYou are a caring AI assistant acting as a doctor. Your ONLY task is to understand the patient's symptoms by asking clarifying follow-up questions.\n\n**RULES:**\n1. Ask only ONE concise question (a single sentence) to gather more information.\n2. The question MUST seek new, relevant medical details not already provided.\n3. Output **ONLY** the single question itself. Do **NOT** add greetings, summaries, explanations, or rephrasing of the user's input.\n4. Do **NOT** provide diagnoses or medical advice.\n5. Do **NOT** repeat previous questions.\n\nYour *entire* response must be just the question.<|eot_id|>\n{conversation_history_prompt}<|start_header_id|>user<|end_header_id|>\n\n{question}<|eot_id|>\n<|start_header_id|>assistant<|end_header_id|>" # Ensure NO leading whitespace

    print("[ASK] Full Llama 3 templated prompt prepared. Sending to LLM.")

    response_data = medical_model.llm(prompt, max_tokens=50)
    raw_response = response_data["choices"][0]["message"]["content"]
    print(f"[ASK] Raw response received from model: {raw_response}")

    processed_response = raw_response.strip()
    q_mark_index = processed_response.find('?')

    if q_mark_index != -1:
        processed_response = processed_response[:q_mark_index + 1]
        print(f"[POST-PROC] Extracted question: {processed_response}")
    else:
        print(f"[WARN] No question mark found in LLM response: {processed_response}")
        processed_response = processed_response.strip().strip('"')

    processed_response = processed_response.strip().strip('"')

    print(f"[ASK] Final Processed response: {processed_response}")
    update_conversation(question, processed_response, index)
    return processed_response