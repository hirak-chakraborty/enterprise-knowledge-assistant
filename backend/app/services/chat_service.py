from backend.app.services.retrieval_service import RetrievalService
from backend.app.services.prompt_service import PromptService
from backend.app.services.llm_service import LLMService
from backend.app.services.conversation_service import ConversationService
from backend.app.services.query_rewriter_service import QueryRewriterService


class ChatService:

    def __init__(self):
        self.conversation_service = ConversationService()
        self.query_rewriter_service = QueryRewriterService()
        self.retrieval_service = RetrievalService()
        self.prompt_service = PromptService()
        self.llm_service = LLMService()

    def chat(self, session_id: str, question: str):

        # Load previous conversation
        history = self.conversation_service.get_history(session_id)

        # Rewrite follow-up questions
        rewritten_question = self.query_rewriter_service.rewrite(
            question,
            history
        )

        print("\n========== QUERY REWRITER ==========")
        print(f"Original Question : {question}")
        print(f"Rewritten Question: {rewritten_question}")
        print("====================================\n")

        # Retrieve relevant document chunks
        results = self.retrieval_service.search(rewritten_question)

        documents = results.get("documents", [[]])[0]
        print("\n========== RETRIEVAL ==========")

        for i, doc in enumerate(documents, 1):
            print(f"\nChunk {i}:")
            print(doc[:200])

        print("================================\n")
        metadatas = results.get("metadatas", [[]])[0]

        # Build RAG prompt
        prompt = self.prompt_service.build_prompt(
            question=rewritten_question,
            context_chunks=documents
        )

        # Generate answer
        answer = self.llm_service.generate_response(prompt)

        # Store conversation
        self.conversation_service.add_user_message(
            session_id,
            question
        )

        self.conversation_service.add_assistant_message(
            session_id,
            answer
        )

        # Keep only recent history
        self.conversation_service.trim_history(session_id)

        return {
            "answer": answer,
            "sources": metadatas
        }