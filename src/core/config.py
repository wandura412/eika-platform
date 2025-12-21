from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "EIKA Platform"
    API_V1_STR: str = "/api/v1"

    # Vector DB Settings
    CHROMA_PERSIST_DIRECTORY: str = "./chroma_db_data"
    EMBEDDING_MODEL_NAME: str = "sentence-transformers/all-MiniLM-L6-v2"

    class Config:
        env_file = ".env"

settings = Settings()