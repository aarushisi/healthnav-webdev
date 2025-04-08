from models.model import MedicalModel
import models.main as main
import os

def test_ollama_model():
    print("\n--- Running test_ollama_model ---")

    model = MedicalModel()

    prompt = """
        User Symptoms: I've been coughing nonstop for 5 days and I feel very tired all the time. My stomach feels very upset. What would you recommend?

        Please generate one specific, medically relevant follow-up question in response to the user's symptoms input. Do not explain your reasoning. Just output the question.
    """

    print("[TEST] Prompt to be sent to model:")
    print(prompt)

    response = model.llm(prompt, max_tokens=60)
    print("[TEST] Response received from model:")
    print(response['choices'][0]['message']['content'])


def test_ask():
    print("\n--- Running test_ask (simulated user message) ---")

    # 💣 Delete previous FAISS index to simulate first use
    if os.path.exists("retrieval_index.faiss"):
        os.remove("retrieval_index.faiss")
        print("[TEST] Previous FAISS index deleted to simulate fresh state.")
    else:
        print("[TEST] No existing FAISS index found. Starting fresh.")

    user_question = "I am feeling very sick and my head hurts."
    print(f"[TEST] Sending user question to ask():\n{user_question}")

    response = main.ask(user_question)

    print("\n[TEST] Model response from main.ask():")
    print(response)

    print("\n[TEST] Updated conversation history:")
    for speaker in main.conversation_history:
        print(f"Speaker: {speaker}")
        for msg in main.conversation_history[speaker]:
            print(f"  {msg}")

    print("[TEST] test_ask completed successfully.")

if __name__ == "__main__":
    #print("\n--- Running test_ollama_model ---")
    #test_ollama_model()

    print("\n--- Running test_ask (simulated user message) ---")
    test_ask()
