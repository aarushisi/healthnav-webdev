# model/model.py
import requests
from sentence_transformers import SentenceTransformer
from doctor_match import build_doctor_index


class MedicalModel:
    def __init__(self, model_name="koesn/llama3-openbiollm-8b", host="http://localhost:11434"):
        self.model_name = model_name
        self.host = host
        print(f"Ollama model '{self.model_name}' ready at {self.host}")

    def llm(self, prompt, max_tokens=500):
        try:
            response = requests.post(
                f"{self.host}/api/generate",
                json={
                    "model": self.model_name,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "num_predict": max_tokens
                    }
                }
            )
            response.raise_for_status()
            result = response.json()
            return {"choices": [{"message": {"content": result["response"]}}]}
        except requests.exceptions.RequestException as e:
            print(f"[ERROR] Ollama request failed: {e}")
            return {"choices": [{"message": {"content": "Error: Failed to generate response from model."}}]}


# Initialize model + embeddings
medical_model = MedicalModel()
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# Build doctor index on startup
build_doctor_index()
