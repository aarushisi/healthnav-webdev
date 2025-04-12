.PHONY: run serve model app all

# Start the Ollama server in the background
serve:
	@echo "Starting Ollama server..."
	ollama serve &

# Run the LLM model
model:
	@echo "Launching the LLM model..."
	ollama run koesn/llama3-openbiollm-8b:Q4_K_M &

# Run the Flask backend
app:
	@echo "Starting Flask app..."
	python app.py

# One command to run everything
all:
	@echo "🚀 Launching full system (Ollama serve, model, Flask)..."
	$(MAKE) serve
	sleep 2
	$(MAKE) model
	sleep 4
	$(MAKE) app
