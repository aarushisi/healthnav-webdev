from huggingface_hub import hf_hub_download
from llama_cpp import Llama
from sentence_transformers import SentenceTransformer
from doctor_matcher import build_doctor_index


class MedicalModel:
    def __init__(self, model_name="aaditya/OpenBioLLM-Llama3-8B-GGUF", model_file="openbiollm-llama3-8b.Q2_K.gguf"):
        self.model_path = hf_hub_download(model_name, filename=model_file, local_dir=".")
        print(f"Model path: {self.model_path}")

        self.llm = Llama(model_path=self.model_path, n_gpu_layers=40, n_ctx=4096, n_threads=8)
        print("Model loaded successfully!")

medical_model = MedicalModel()

embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

build_doctor_index()