from pypdf import PdfReader
import shutil
from dataclasses import dataclass
from typing import List, Generator

@dataclass
class ProcessedChunk:
    text: str
    source: str
    page_number: int

class DocumentProcessor:
    def __init__(self, chunk_size: int = 1000, overlap: int = 200):
        self.chunk_size = chunk_size
        self.overlap = overlap

    def _chunk_text(self, text: str) -> Generator[str, None, None]:
        """
        Splits text into chunks with overlap.
        """
        if not text:
            return

        start = 0
        text_len = len(text)

        while start < text_len:
            end = start + self.chunk_size
            yield text[start:end]
            # Move forward, but step back by overlap amount
            start += (self.chunk_size - self.overlap)

    async def process_pdf(self, file_path: str, filename: str) -> List[ProcessedChunk]:
        """Reads PDF and converts to chunks."""
        chunks = []

        # Synchronous reading (standard for pypdf)
        reader = PdfReader(file_path)

        for i, page in enumerate(reader.pages):
            text = page.extract_text()
            if text:
                for chunk_text in self._chunk_text(text):
                    chunks.append(ProcessedChunk(
                        text=chunk_text,
                        source=filename,
                        page_number=i + 1
                    ))

        return chunks

    def save_temp_file(self, upload_file, destination: str):
        with open(destination, "wb") as buffer:
            shutil.copyfileobj(upload_file.file, buffer)