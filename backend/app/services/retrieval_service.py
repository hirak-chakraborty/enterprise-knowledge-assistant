from backend.app.services.embedding_service import EmbeddingService
from backend.app.services.vector_store_service import VectorStoreService


class RetrievalService:

    def __init__(self):
        self.embedding_service = EmbeddingService()
        self.vector_store = VectorStoreService()

    def search(self, question: str, top_k: int = 5):

        question_embedding = self.embedding_service.generate_embeddings(
            [question]
        )[0]

        results = self.vector_store.search(
            question_embedding,
            top_k
        )

        distances = results.get("distances", [[]])[0]

        print("\n========== RETRIEVAL SCORES ==========")

        for index, distance in enumerate(distances, start=1):
            print(
                f"Rank {index} | "
                f"Distance: {distance:.4f}"
            )

        print("======================================\n")

        return results