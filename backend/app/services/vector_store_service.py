import os

import chromadb


class VectorStoreService:

    def __init__(self):

        self.client = chromadb.PersistentClient(
            path="backend/chroma_db"
        )

        self.collection = self.client.get_or_create_collection(
            name="enterprise_documents"
        )

    def store(self, document_name: str, chunks, embeddings):

        # Generate a clean document ID
        document_id = (
            os.path.splitext(document_name)[0]
            .replace(" ", "_")
            .lower()
        )

        # Remove existing chunks for this document
        existing = self.collection.get(
            where={"document": document_name}
        )

        if existing["ids"]:
            self.collection.delete(ids=existing["ids"])

        # Create readable chunk IDs
        ids = [
            f"{document_id}_chunk_{i + 1}"
            for i in range(len(chunks))
        ]

        # Store vectors
        self.collection.add(
            ids=ids,
            documents=chunks,
            embeddings=embeddings.tolist(),
            metadatas=[
                {
                    "document": document_name,
                    "chunk_number": i + 1
                }
                for i in range(len(chunks))
            ]
        )