# Droid

A simple prototype for a conversational and vision-enabled droid.

## Overview
This project combines speech recognition, text-to-speech, and computer vision
capabilities to create an interactive "droid" that can listen, respond and
track faces using a webcam. Responses are generated through the Groq API.

## Setup
1. Ensure you have Python 3 installed.
2. Install the required packages:
   ```bash
   pip install pyttsx3 speech_recognition opencv-python groq
   ```

## Usage
Run the droid with:
```bash
python main.py
```

### Customizing prompts and models

`Conversation` allows overriding the system prompt and the Groq model used for
completions. Defaults match the previous behaviour:

```python
from conversation import Conversation

# Use a custom prompt and model
conv = Conversation(
    system_prompt="You are a helpful robot.",
    groq_model="llama-3.1-8b-instant",
)
```

`GroqClient` can also be instantiated directly with a custom model:

```python
from groq_client import GroqClient

client = GroqClient(model="llama-3.1-8b-instant")
```
