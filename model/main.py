import faiss
import numpy as np
from datetime import datetime
from sentence_transformers import SentenceTransformer
from model import medical_model

# Initialize SentenceTransformer for embeddings
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# Per-user FAISS index storage
user_histories = {}  # Stores user conversations
user_indices = {}  # Stores user-specific FAISS indices

def create_faiss_index():
    """Creates a new FAISS index for a user."""
    index = faiss.IndexFlatL2(384)  # 384 is the embedding size for all-MiniLM-L6-v2
    return index

def retrieve_context(user_id, query, top_k=2):
    """Retrieves relevant past conversations for a user."""
    if user_id not in user_indices:
        return "No relevant documents found."
    
    retrieval_index = user_indices[user_id]
    query_embedding = np.array([embedding_model.encode(query)])
    
    if retrieval_index.ntotal == 0:
        return "No relevant documents found."
    
    distances, indices = retrieval_index.search(query_embedding, top_k)
    retrieved_docs = [user_histories[user_id][i] for i in indices[0] if i < len(user_histories[user_id])]
    
    return "\n".join(retrieved_docs) if retrieved_docs else "No relevant documents found."

def update_index(user_id, query):
    """Updates the FAISS index for a user with new query data."""
    if user_id not in user_indices:
        user_indices[user_id] = create_faiss_index()
        user_histories[user_id] = []

    user_histories[user_id].append(query)
    input_embedding = embedding_model.encode(query)
    user_indices[user_id].add(np.array([input_embedding]))

def ask(user_id, question):
    """Generates a medical response using the LLaMA model."""
    retrieved_info = retrieve_context(user_id, question)
    prompt = f"""
        You are an expert caretaker helping patients find a doctor.

        - If the patient provides location and health insurance, respond with:
        \\n DOCTOR_SEARCH.py \\n
        - If information is missing, ask for the missing details.
        - Prefix the answer with one of: 'general', 'dentist', 'dietician', 'neurologist', 'cardiologist', 'gynecologist', 'radiologist'.

        Medical question: {question}
        Previous medical info: {retrieved_info}
        Answer:
    """
    response = medical_model.llm(prompt, max_tokens=500)['choices'][0]['message']['content']
    update_index(user_id, question)
    return response

# Simulating multiple users
while True:
    user_id = input("Enter your user ID (or 'quit' to exit): ").strip()
    if user_id.lower() == "quit":
        break
    
    question = input(f"[User {user_id}] Ask a medical question: ")
    while question.lower() != "quit":
        print(ask(user_id, question))
        question = input(f"[User {user_id}] Ask another question or type 'quit': ")