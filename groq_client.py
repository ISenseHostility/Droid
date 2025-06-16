"""Wrapper around the Groq SDK used to generate chat responses."""

import logging
import os
from groq import Groq

logger = logging.getLogger(__name__)


class GroqClient:
    """Simple client used to request completions from Groq."""

    def __init__(self, model: str = "llama-3.1-8b-instant"):
        """Instantiate the underlying Groq client.

        Parameters
        ----------
        model : str, optional
            Name of the Groq model to use for completions. Defaults to
            "llama-3.1-8b-instant".
        """
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            logger.error(
                "GROQ_API_KEY environment variable is not set. "
                "API requests will fail."
            )
        self.client = Groq(api_key=api_key) if api_key else Groq()
        self.model = model

    def get_text_response(self, system_message, user_message):
        """Return Groq's response for a given user message."""
        chat_completion = self.client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": system_message
                },
                {
                    "role": "user",
                    "content": user_message,
                }
            ],
            model=self.model,
        )

        return chat_completion.choices[0].message.content
