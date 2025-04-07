import requests
from sentence_transformers import SentenceTransformer
from models.doctor_match import build_doctor_index

class MedicalModel:
    def __init__(self, model_name="koesn/llama3-openbiollm-8b:Q4_K_M", host="http://localhost:11434"):
        self.model_name = model_name
        self.host = host
        print(f"Ollama model '{self.model_name}' ready at {self.host}")

    def llm(self, prompt, max_tokens=60):
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
                },
                timeout=500  # ⏱ 10 second limit
            )
            response.raise_for_status()
            result = response.json()
            return {"choices": [{"message": {"content": result["response"]}}]}
        except requests.Timeout:
            return {"choices": [{"message": {"content": "Timeout: Model took too long to respond."}}]}
        except requests.RequestException as e:
            return {"choices": [{"message": {"content": f"Error: {e}"}}]}


if __name__ == "__main__":
    # Initialize model + embeddings
    medical_model = MedicalModel()
    embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
    # Build doctor index on startup
    build_doctor_index()