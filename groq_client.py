from dotenv import load_dotenv
from groq import Groq

load_dotenv()

class GroqClient:
    def __init__(self):
        self.client = Groq()

    def get_text_response(self, messages):
        chat_completion = self.client.chat.completions.create(
            messages=messages,
            model="llama-3.3-70b-versatile",
        )

        return chat_completion.choices[0].message.content