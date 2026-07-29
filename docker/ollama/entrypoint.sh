#!/bin/bash
set -e

# Start Ollama server in background
ollama serve &
SERVER_PID=$!

# Wait for server to be ready
echo "Waiting for Ollama server..."
for i in $(seq 1 30); do
  if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo "Ollama server ready"
    break
  fi
  if [ "$i" -eq 30 ]; then
    echo "Ollama server failed to start"
    exit 1
  fi
  sleep 1
done

# Pull default model
if [ -n "$OLLAMA_MODEL" ]; then
  echo "Pulling model: $OLLAMA_MODEL"
  ollama pull "$OLLAMA_MODEL"
  echo "Model $OLLAMA_MODEL ready"
fi

# Pull extra models if configured
if [ -n "$OLLAMA_EXTRA_MODELS" ]; then
  for model in $OLLAMA_EXTRA_MODELS; do
    echo "Pulling extra model: $model"
    ollama pull "$model"
    echo "Extra model $model ready"
  done
fi

# Bring Ollama to foreground
wait $SERVER_PID
