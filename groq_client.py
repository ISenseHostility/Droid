from groq import Groq

client = Groq()


def get_text_response(systemMessage, userMessage):
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": systemMessage
            },
            {
                "role": "user",
                "content": userMessage,
            }
        ],
        model="meta-llama/llama-4-maverick-17b-128e-instruct",
    )

    return chat_completion.choices[0].message.content
