import chromadb
from chromadb.config import Settings # Import Settings explicitly
from chromadb.utils import embedding_functions
from src.core.config import settings
from src.services.document_processor import ProcessedChunk
from typing import List
import uuid

class VectorDBService:
    def __init__(self):
        # Initialize direct Chroma Client with telemetry disabled
        self.client = chromadb.PersistentClient(
            path=settings.CHROMA_PERSIST_DIRECTORY,
            settings=Settings(anonymized_telemetry=False)
        )
        
        # Use standard Sentence Transformers directly
        self.embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name=settings.EMBEDDING_MODEL_NAME
        )
        
        # Create or get collection
        self.collection = self.client.get_or_create_collection(
            name="knowledge_base",
            embedding_function=self.embedding_fn
        )

    async def add_documents(self, chunks: List[ProcessedChunk]):
        """Adds processed chunks to ChromaDB."""
        if not chunks:
            return

        # Prepare data for Chroma API
        documents = [chunk.text for chunk in chunks]
        metadatas = [{"source": chunk.source, "page": chunk.page_number} for chunk in chunks]
        ids = [str(uuid.uuid4()) for _ in chunks]

        # Add to DB
        self.collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )
        print(f"Added {len(documents)} chunks to the database.")
    
    async def search(self, query_text: str, limit: int = 5):
        """
        Performs a semantic search on the vector database.
        """
        results = self.collection.query(
            query_texts=[query_text],
            n_results=limit
        )
        
        # Chroma returns a complex dictionary of lists. We need to parse it cleanly.
        # Structure: {'documents': [[text1, text2]], 'metadatas': [[meta1, meta2]], ...}
        
        parsed_results = []
        if results['documents']:
            for i in range(len(results['documents'][0])):
                parsed_results.append({
                    "content": results['documents'][0][i],
                    "metadata": results['metadatas'][0][i],
                    "score": results['distances'][0][i] if 'distances' in results else None
                })
                
        return parsed_results