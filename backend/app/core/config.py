from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    POSTGRES_USER: str = "gobtools"
    POSTGRES_PASSWORD: str = "changeme"
    POSTGRES_DB: str = "gobtools"
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432

    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379

    JWT_SECRET: str = "changeme-please-use-a-strong-secret"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_MINUTES: int = 60

    LLM_PROVIDER: str = "ollama"
    LLM_MODEL: str = "qwen2.5:1.5b"
    LLM_TEMPERATURE: float = 0.2
    LLM_MAX_TOKENS: int = 4096
    LLM_TIMEOUT: int = 60

    OLLAMA_BASE_URL: str = "http://localhost:11434"

    OPENAI_API_KEY: str = ""
    OPENAI_MODEL: str = "gpt-4o"

    ANTHROPIC_API_KEY: str = ""
    ANTHROPIC_MODEL: str = "claude-sonnet-4-20250514"

    GEMINI_API_KEY: str = ""
    GEMINI_MODEL: str = "gemini-2.0-flash"

    MISTRAL_API_KEY: str = ""
    MISTRAL_MODEL: str = "mistral-large-latest"

    OPENROUTER_API_KEY: str = ""
    OPENROUTER_MODEL: str = "openai/gpt-4o"

    PLUGINS_DIR: str = "/app/plugins"
    PDF_MAX_SIZE_MB: int = 30
    HISTORY_DB_PATH: str = "data/history.db"

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()
