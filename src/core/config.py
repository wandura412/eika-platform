from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "EIKA Platform"
    API_V1_STR: str = "/api/v1"
    
    # Vector DB Settings
    CHROMA_PERSIST_DIRECTORY: str = "/app/chroma_db_data" # Updated for Docker path
    EMBEDDING_MODEL_NAME: str = "sentence-transformers/all-MiniLM-L6-v2"

    # External Service URLs (Defaults are for Local Localhost)
    OLLAMA_BASE_URL: str = "http://localhost:11434/api/generate"

    class Config:
        env_file = ".env"

settings = Settings()