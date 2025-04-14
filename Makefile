.PHONY: serve model app test_model all test stop install

install:
	@echo "📦 Installing required Python packages..."
	pip install --upgrade pip
	pip install -r requirements.txt

serve:
	@echo "🔌 Starting Ollama server (if not already running)..."
	@pgrep -f "ollama serve" > /dev/null || ollama serve &

model:
	@echo "🧠 Launching LLM model (if not already running)..."
	@pgrep -f "ollama run koesn/llama3-openbiollm-8b:Q6_K" > /dev/null || ollama run koesn/llama3-openbiollm-8b:Q6_K &

app:
	@echo "🌐 Starting Flask app..."
	python app.py

test_model:
	@echo "🧪 Running test_model.py..."
	python test_model.py

all:
	@echo "🚀 Installing packages, then launching everything..."
	$(MAKE) serve
	sleep 2
	$(MAKE) model
	sleep 4
	$(MAKE) app

test:
	@echo "🧪 Installing packages, then launching test mode..."
	$(MAKE) serve
	sleep 2
	$(MAKE) model
	sleep 4
	$(MAKE) test_model

stop:
	@echo "🛑 Stopping Ollama server and LLM model..."
	@pkill -f "ollama serve" || echo "Ollama server not running."
	@pkill -f "ollama run koesn/llama3-openbiollm-8b:Q6_K" || echo "LLM model not running."
