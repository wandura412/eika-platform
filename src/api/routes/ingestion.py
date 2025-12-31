from fastapi import APIRouter, UploadFile, File, BackgroundTasks, HTTPException
from src.services.document_processor import DocumentProcessor
from src.services.vector_store import VectorDBService
import os
import uuid

router = APIRouter()
doc_processor = DocumentProcessor()
vector_service = VectorDBService()


@router.delete("/reset")
def reset_knowledge_base():
    """
    DANGER: Wipes the entire vector database.
    This is used to clear old documents before uploading new ones.
    """
    success = vector_service.clear_database()
    if not success:
        raise HTTPException(status_code=500, detail="Failed to clear database")
    
    return {"message": "Knowledge base has been successfully cleared."}

async def bg_process_document(file_path: str, original_filename: str):
    try:
        chunks = await doc_processor.process_pdf(file_path, original_filename)
        await vector_service.add_documents(chunks)
        print(f"Successfully processed {original_filename}")
    except Exception as e:
        print(f"Error processing {original_filename}: {e}")
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)

@router.post("/ingest")
async def ingest_document(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...)
):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDFs are supported")

    temp_filename = f"temp_{uuid.uuid4()}_{file.filename}"
    doc_processor.save_temp_file(file, temp_filename)

    background_tasks.add_task(bg_process_document, temp_filename, file.filename)

    return {"message": "Document received. Processing in background.", "filename": file.filename}