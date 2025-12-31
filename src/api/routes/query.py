from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from src.services.vector_store import VectorDBService
from src.services.llm_service import LLMService  

router = APIRouter()
vector_service = VectorDBService()
llm_service = LLMService()  

class QueryRequest(BaseModel):
    text: str
    limit: int = 5

@router.post("/chat")  
async def chat_with_document(request: QueryRequest):
    """
    Full RAG Pipeline: Retrieve -> Generate
    """
    if not request.text.strip():
        raise HTTPException(status_code=400, detail="Query text cannot be empty")
        
    
    results = await vector_service.search(request.text, request.limit)
    
    
    ai_answer = llm_service.generate_response(request.text, results)
    
    return {
        "user_query": request.text,
        "ai_response": ai_answer,
        "source_documents": results 
    }