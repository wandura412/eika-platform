import chromadb
from chromadb.config import Settings
from chromadb.utils import embedding_functions
from src.core.config import settings
from src.services.document_processor import ProcessedChunk
from typing import List
import uuid

class VectorDBService:
    def __init__(self):
        # 1. Initialize the Client (This stays persistent)
        self.client = chromadb.PersistentClient(
            path=settings.CHROMA_PERSIST_DIRECTORY,
            settings=Settings(anonymized_telemetry=False)
        )
        
        # 2. Define the embedding function
        self.embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name=settings.EMBEDDING_MODEL_NAME
        )

        # NOTE: self.collection is not stored here anymore.
        # This prevents the "stale reference" bug.

    @property
    def collection(self):
        """
        Dynamically fetch the collection every time we access .collection.
        This ensures we always get the valid, current version.
        """
        return self.client.get_or_create_collection(
            name="knowledge_base",
            embedding_function=self.embedding_fn
        )

    async def add_documents(self, chunks: List[ProcessedChunk]):
        if not chunks:
            return

        documents = [chunk.text for chunk in chunks]
        metadatas = [{"source": chunk.source, "page": chunk.page_number} for chunk in chunks]
        ids = [str(uuid.uuid4()) for _ in chunks]

        # access self.collection (which calls the property above)
        self.collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )
        print(f"Added {len(documents)} chunks to the database.")

    async def search(self, query_text: str, limit: int = 5):
        # access self.collection (gets the fresh handle)
        results = self.collection.query(
            query_texts=[query_text],
            n_results=limit
        )
        
        parsed_results = []
        if results['documents']:
            for i in range(len(results['documents'][0])):
                parsed_results.append({
                    "content": results['documents'][0][i],
                    "metadata": results['metadatas'][0][i],
                    "score": results['distances'][0][i] if 'distances' in results else None
                })
                
        return parsed_results

    def clear_database(self):
        try:
            self.client.delete_collection("knowledge_base")
            return True
        except Exception as e:
            print(f"Error clearing database: {e}")
            return False