from backend.app.services.embedding_service import EmbeddingService
from backend.app.services.vector_store_service import VectorStoreService


MAX_DISTANCE = 0.7


class RetrievalService:
    def __init__(self):
        self.embedding_service = EmbeddingService()
        self.vector_store = VectorStoreService()

    def search(self, question: str, top_k: int = 2):
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

        # Keep only sufficiently relevant results
        filtered_indices = [
            i
            for i, distance in enumerate(distances)
            if distance <= MAX_DISTANCE
        ]

        filtered_results = {
            "documents": [
                [results["documents"][0][i] for i in filtered_indices]
            ],
            "metadatas": [
                [results["metadatas"][0][i] for i in filtered_indices]
            ],
            "distances": [
                [results["distances"][0][i] for i in filtered_indices]
            ]
        }

        print(
            f"Retrieved {len(distances)} results, "
            f"kept {len(filtered_indices)} results "
            f"(max distance: {MAX_DISTANCE})"
        )

        return filtered_results