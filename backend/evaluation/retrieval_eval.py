import json
import os
from datetime import datetime

from backend.app.services.retrieval_service import RetrievalService
from backend.app.services.prompt_service import PromptService
from backend.app.services.llm_service import LLMService


TEST_CASES_FILE = os.path.join(
    os.path.dirname(__file__),
    "test_cases.json"
)

RESULTS_DIR = os.path.join(
    os.path.dirname(__file__),
    "results"
)


def load_test_cases():
    with open(TEST_CASES_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def run_evaluation():
    os.makedirs(RESULTS_DIR, exist_ok=True)

    test_cases = load_test_cases()

    retrieval_service = RetrievalService()
    prompt_service = PromptService()
    llm_service = LLMService()

    results = []

    for test_case in test_cases:
        question = test_case["question"]

        print("\n" + "=" * 80)
        print(f"TEST {test_case['id']}: {question}")
        print("=" * 80)

        # 1. Retrieval
        retrieved = retrieval_service.search(question)

        documents = retrieved.get("documents", [[]])[0]
        metadatas = retrieved.get("metadatas", [[]])[0]
        distances = retrieved.get("distances", [[]])[0]

        retrieval_results = []

        for index, document in enumerate(documents):
            metadata = metadatas[index]
            distance = distances[index]

            retrieval_results.append({
                "rank": index + 1,
                "distance": distance,
                "chunk_number": metadata.get("chunk_number"),
                "document": metadata.get("document"),
                "text": document
            })

            print(
                f"Rank {index + 1} | "
                f"Distance: {distance:.4f} | "
                f"Chunk: {metadata.get('chunk_number')}"
            )

        # 2. Build prompt using retrieved context
        prompt = prompt_service.build_prompt(
            question,
            documents
        )

        # 3. Generate answer
        answer = llm_service.generate_response(prompt)

        print(f"\nAnswer:\n{answer}")

        # 4. Store complete result
        results.append({
            "id": test_case["id"],
            "question": question,
            "category": test_case["category"],
            "expected_topic": test_case["expected_topic"],
            "retrieval": {
                "top_k": 2,
                "results": retrieval_results
            },
            "generation": {
                "answer": answer
            }
        })

    # 5. Store complete evaluation run
    timestamp = datetime.now().astimezone()

    evaluation = {
        "timestamp": timestamp.isoformat(),
        "configuration": {
            "top_k": 2,
            "max_distance": 0.7,
            "embedding_model": "BAAI/bge-small-en-v1.5",
            "llm_model": "qwen3:8b"
        },
        "tests": results
    }

    filename = timestamp.strftime("%Y-%m-%d_%H-%M-%S") + ".json"
    output_path = os.path.join(RESULTS_DIR, filename)

    with open(output_path, "w", encoding="utf-8") as file:
        json.dump(evaluation, file, indent=2, ensure_ascii=False)

    print("\n" + "=" * 80)
    print(f"Evaluation saved to: {output_path}")
    print("=" * 80)


if __name__ == "__main__":
    run_evaluation()