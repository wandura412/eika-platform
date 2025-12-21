from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from src.services.vector_store import VectorDBService

router = APIRouter()
vector_service = VectorDBService()

# Define the request model (What the user sends)
class QueryRequest(BaseModel):
    text: str
    limit: int = 5

@router.post("/search")
async def search_knowledge_base(request: QueryRequest):
    """
    Semantic search endpoint.
    Accepts a query text and returns the most relevant document chunks.
    """
    if not request.text.strip():
        raise HTTPException(status_code=400, detail="Query text cannot be empty")
        
    results = await vector_service.search(request.text, request.limit)
    
    return {
        "query": request.text,
        "results": results
    }