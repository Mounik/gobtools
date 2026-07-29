FROM ollama/ollama:0.32.5

RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENV OLLAMA_HOST=0.0.0.0
ENV OLLAMA_MODEL=qwen2.5:1.5b

ENTRYPOINT ["/entrypoint.sh"]
