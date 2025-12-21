from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from src.services.vector_store import VectorDBService
from src.services.llm_service import LLMService  # <--- Import this

router = APIRouter()
vector_service = VectorDBService()
llm_service = LLMService()  # <--- Initialize this

class QueryRequest(BaseModel):
    text: str
    limit: int = 5

@router.post("/chat")  # <--- Renamed endpoint
async def chat_with_document(request: QueryRequest):
    """
    Full RAG Pipeline: Retrieve -> Generate
    """
    if not request.text.strip():
        raise HTTPException(status_code=400, detail="Query text cannot be empty")
        
    # 1. Retrieve relevant chunks (The "R" in RAG)
    results = await vector_service.search(request.text, request.limit)
    
    # 2. Generate answer (The "G" in RAG)
    ai_answer = llm_service.generate_response(request.text, results)
    
    return {
        "user_query": request.text,
        "ai_response": ai_answer,
        "source_documents": results # Returning sources is a best practice!
    }