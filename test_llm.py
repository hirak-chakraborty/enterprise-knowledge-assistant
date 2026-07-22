from backend.app.services.llm_service import LLMService

llm = LLMService()

answer = llm.generate_response(
    "Explain Retrieval-Augmented Generation in two sentences."
)

print(answer)