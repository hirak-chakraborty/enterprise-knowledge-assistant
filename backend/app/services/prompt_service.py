class PromptService:
    """
    Builds prompts for the LLM using retrieved context.
    """

    @staticmethod
    def build_prompt(question: str, context_chunks: list[str]) -> str:

        context = "\n\n".join(context_chunks)

        return f"""
You are an Enterprise Knowledge Assistant.

Instructions:
- Answer strictly using only the information provided in the context.
- Do not use outside knowledge, assumptions, or unstated relationships.
- Do not combine separate facts from the context to create a new claim unless that relationship is explicitly stated.
- If the context contains related information but does not directly answer the question, reply:
  "I couldn't find that information in the provided documents."
- When in doubt, refuse rather than infer.
- Keep answers clear and concise.
- If appropriate, summarize information instead of copying it verbatim.

Context:
------------------------
{context}
------------------------

Question:
{question}

Answer:
"""