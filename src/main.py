from fastapi import FastAPI
from src.api.routes import ingestion, query  # <--- Import the new module
from src.core.config import settings

app = FastAPI(title=settings.PROJECT_NAME)

# Include Routers
app.include_router(ingestion.router, prefix=settings.API_V1_STR + "/documents", tags=["documents"])
app.include_router(query.router, prefix=settings.API_V1_STR + "/query", tags=["search"]) # <--- Add this line

@app.get("/health")
def health_check():
    return {"status": "healthy", "version": "1.0.0"}