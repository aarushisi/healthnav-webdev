import requests
from sentence_transformers import SentenceTransformer
from models.doctor_match import build_doctor_index

class MedicalModel:
    def __init__(self, model_name="koesn/llama3-openbiollm-8b:Q4_0", host="http://localhost:11434"):
        self.model_name = model_name
        self.host = host
        print(f"[INIT] MedicalModel initialized with model '{self.model_name}' at host '{self.host}'.")

    def llm(self, prompt, max_tokens=50):
        print(f"[LLM] Preparing to send prompt to model.")
        print(f"[LLM] Prompt: {prompt[:200]}{'...' if len(prompt) > 200 else ''}")  # Truncate long prompts
        print(f"[LLM] Max tokens: {max_tokens}")
        
        try:
            response = requests.post(
                f"{self.host}/api/generate",
                json={
                    "model": self.model_name,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "num_predict": max_tokens,
                        "temperature": 0.7,
                        "top_p": 0.9
                    }
                },
                timeout=600  # ⏱ 10-minute timeout
            )
            print("[LLM] Request sent. Awaiting response...")
            response.raise_for_status()
            result = response.json()
            print(f"[LLM] Response received successfully. Content: {result['response'][:200]}{'...' if len(result['response']) > 200 else ''}")
            return {"choices": [{"message": {"content": result["response"]}}]}
        
        except requests.Timeout:
            print("[ERROR] Request to model timed out.")
            return {"choices": [{"message": {"content": "Timeout: Model took too long to respond."}}]}
        
        except requests.RequestException as e:
            print(f"[ERROR] Request to model failed: {e}")
            return {"choices": [{"message": {"content": f"Error: {e}"}}]}