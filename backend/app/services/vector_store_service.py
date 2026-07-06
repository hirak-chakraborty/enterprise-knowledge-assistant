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

        print("\n========== VECTOR STORE ==========")
        print(f"Document : {document_name}")
        print(f"Chunks   : {len(chunks)}")
        print(f"Vectors  : {len(embeddings)}")

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
            print(f"Deleting {len(existing['ids'])} existing chunks...")
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

        print("Vectors stored successfully!")

        count = self.collection.count()
        print(f"Collection contains {count} vectors.")
        print("==================================\n")

    def search(self, embedding, top_k=5):

        print("\n========== SEARCH ==========")

        count = self.collection.count()
        print(f"Vectors in collection : {count}")

        results = self.collection.query(
            query_embeddings=[embedding.tolist()],
            n_results=top_k,
            include=["documents", "metadatas", "distances"]
        )

        print("Search completed.")
        print("============================\n")

        return results