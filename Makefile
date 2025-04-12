.PHONY: serve model app test_model all test

# Start the Ollama server in the background
serve:
	@echo "Starting Ollama server..."
	ollama serve &

# Run the LLM model in the background
model:
	@echo "Launching the LLM model..."
	ollama run koesn/llama3-openbiollm-8b:Q4_K_M &

# Run the Flask backend
app:
	@echo "Starting Flask app..."
	python app.py

# Run the test script instead of the Flask app
test_model:
	@echo "Running test_model.py..."
	python test_model.py

# One command to launch everything with the Flask app
all:
	@echo "🚀 Launching Ollama server, LLM model, and Flask app..."
	$(MAKE) serve
	sleep 2
	$(MAKE) model
	sleep 4
	$(MAKE) app

# One command to launch everything with test_model.py
test:
	@echo "🧪 Launching Ollama server, LLM model, and test script..."
	$(MAKE) serve
	sleep 2
	$(MAKE) model
	sleep 4
	$(MAKE) test_model
