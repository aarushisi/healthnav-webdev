# test_model.py
from models.model import MedicalModel

def test_ollama_model():
    model = MedicalModel()  # Uses default model and host


    prompt = f"""
        User Symptoms: My foot is discolored and it hurts. The pain started 5 days ago and I think it started when I fell over playing soccer.

        Please generate one specific, medically relevant follow-up question based on the user's symptoms. Do not explain your reasoning. Just output the question.
        """



    print("[Backend] Prompt passed to model")
    response = model.llm(prompt, max_tokens=60)

    print("Model response:")
    print(response['choices'][0]['message']['content'])


if __name__ == "__main__":
    test_ollama_model()