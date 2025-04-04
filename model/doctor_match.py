import faiss
import numpy as np
from model import embedding_model

# These should match index order exactly
doctor_specialties = [
    "Cardiologist",
    "Dermatologist",
    "Endocrinologist",
    "Gastroenterologist",
    "Neurologist",
    # etc...
]

doctor_descriptions = [
    "Specializes in heart and blood vessel conditions.",
    "Treats skin, hair, and nail disorders.",
    "Focuses on hormonal and metabolic issues like diabetes or thyroid problems.",
    "Deals with digestive system issues like ulcers, IBS, and liver disease.",
    "Handles brain, spine, and nerve disorders including seizures and MS.",
    # etc...
]

def build_doctor_index(save_path="doctor_specialty_index.faiss"):
    embeddings = embedding_model.encode(doctor_descriptions)
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(np.array(embeddings))
    faiss.write_index(index, save_path)
    print(f"Doctor specialty index saved to {save_path}")

def load_doctor_index(path="doctor_specialty_index.faiss"):
    return faiss.read_index(path)

def match_doctor(user_input, top_k=3):
    query_embedding = embedding_model.encode(user_input).reshape(1, -1)
    index = load_doctor_index()

    distances, indices = index.search(query_embedding, top_k)
    results = []
    for i in indices[0]:
        if i < len(doctor_specialties):
            results.append({
                "specialty": doctor_specialties[i],
                "description": doctor_descriptions[i]
            })
    return results