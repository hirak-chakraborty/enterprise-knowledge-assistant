from openai import OpenAI


class QueryRewriterService:
    """
    Rewrites follow-up questions into standalone questions
    using the conversation history.
    """

    def __init__(self):
        self.client = OpenAI(
            base_url="http://localhost:11434/v1",
            api_key="ollama"
        )

        self.model = "qwen3:8b"

    def rewrite(self, question: str, history: list):

        # If there is no previous conversation,
        # use the original question.
        if not history:
            return question

        messages = [
            {
                "role": "system",
                "content": (
                    "You are a query rewriting assistant.\n\n"
                    "Your ONLY task is to rewrite follow-up questions "
                    "into standalone search queries.\n\n"
                    "Rules:\n"
                    "1. Do NOT answer the question.\n"
                    "2. Do NOT explain anything.\n"
                    "3. Return ONLY the rewritten question.\n"
                    "4. Preserve the original meaning.\n"
                    "5. If the question is already standalone, "
                    "return it unchanged."
                )
            }
        ]

        messages.extend(history)

        messages.append(
            {
                "role": "user",
                "content": question
            }
        )

        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0
        )

        rewritten_question = (
            response.choices[0]
            .message
            .content
            .strip()
        )

        return rewritten_question