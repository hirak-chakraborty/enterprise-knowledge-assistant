from openai import OpenAI


class LLMService:
    """
    Handles all interactions with the LLM.
    Uses Ollama through its OpenAI-compatible API.
    """

    def __init__(self):
        self.client = OpenAI(
            base_url="http://localhost:11434/v1",
            api_key="ollama"  # Required by SDK but ignored by Ollama
        )

        self.model = "qwen3:8b"

    def generate_response(self, prompt: str) -> str:

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an enterprise AI knowledge assistant. "
                        "Answer ONLY using the provided context. "
                        "If the answer is not available, say you don't know."
                    )
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.2
        )

        return response.choices[0].message.content.strip()