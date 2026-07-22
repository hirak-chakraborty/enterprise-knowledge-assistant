import os
from backend.app.services.chunk_service import ChunkService
from backend.app.utils.pdf_parser import extract_text_from_pdf
from backend.app.services.embedding_service import EmbeddingService
from backend.app.services.vector_store_service import VectorStoreService

class DocumentService:

    def __init__(self):
        self.chunk_service = ChunkService()
        self.vector_store_service = VectorStoreService()
        self.embedding_service = EmbeddingService()

    def process_document(self, file_path: str):

        # Step 1: Extract text
        text = extract_text_from_pdf(file_path)

        # Step 2: Split into chunks
        chunks = self.chunk_service.split(text)

        # Step 3: Generate embeddings
        embeddings = self.embedding_service.generate_embeddings(chunks)

        # Step 4: Store in vector store
        document_name = os.path.basename(file_path)
        
        self.vector_store_service.store(document_name, chunks, embeddings)

        return {
            "chunks": chunks,
            "embeddings": embeddings
        }