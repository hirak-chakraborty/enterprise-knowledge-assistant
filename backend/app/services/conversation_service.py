class ConversationService:
    """
    Stores conversation history by session.
    """

    def __init__(self):
        self.sessions = {}

    def get_history(self, session_id: str):

        return self.sessions.get(session_id, [])

    def add_user_message(self, session_id: str, message: str):

        self.sessions.setdefault(session_id, []).append(
            {
                "role": "user",
                "content": message
            }
        )

    def add_assistant_message(self, session_id: str, message: str):

        self.sessions.setdefault(session_id, []).append(
            {
                "role": "assistant",
                "content": message
            }
        )

    def clear(self, session_id: str):

        self.sessions.pop(session_id, None)

    def trim_history(
        self,
        session_id: str,
        max_messages: int = 10
    ):

        history = self.sessions.get(session_id, [])

        if len(history) > max_messages:
            self.sessions[session_id] = history[-max_messages:]