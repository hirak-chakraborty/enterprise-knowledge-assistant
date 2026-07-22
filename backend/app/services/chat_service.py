from backend.app.services.retrieval_service import RetrievalService
from backend.app.services.prompt_service import PromptService
from backend.app.services.llm_service import LLMService


class ChatService:

    def __init__(self):
        self.retrieval_service = RetrievalService()
        self.prompt_service = PromptService()
        self.llm_service = LLMService()

    def chat(self, question: str):

        # Retrieve relevant document chunks
        results = self.retrieval_service.search(question)

        documents = results.get("documents", [[]])[0]
        metadatas = results.get("metadatas", [[]])[0]

        # Build prompt
        prompt = self.prompt_service.build_prompt(
            question=question,
            context_chunks=documents
        )

        # Generate answer
        answer = self.llm_service.generate_response(prompt)

        return {
            "answer": answer,
            "sources": metadatas
        }