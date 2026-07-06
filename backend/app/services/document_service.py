from backend.app.services.chunk_service import ChunkService
from backend.app.utils.pdf_reader import extract_text_from_pdf


class DocumentService:

    def __init__(self):
        self.chunk_service = ChunkService()

    def process_document(self, file_path: str):

        # Step 1: Extract text
        text = extract_text_from_pdf(file_path)

        # Step 2: Split into chunks
        chunks = self.chunk_service.split(text)

        return chunks