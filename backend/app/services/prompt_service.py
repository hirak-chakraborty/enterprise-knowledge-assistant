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
- Answer ONLY using the information provided in the context.
- Do not use outside knowledge.
- If the answer cannot be found in the context, reply:
  "I couldn't find that information in the provided documents."
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