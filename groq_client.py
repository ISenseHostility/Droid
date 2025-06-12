from groq import Groq


class GroqClient:
    def __init__(self):
        self.client = Groq()

    def get_text_response(self, system_message, user_message):
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
            model="llama-3.1-8b-instant",
        )

        return chat_completion.choices[0].message.content