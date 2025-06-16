"""Speech-based conversation interface for interacting with the Groq API."""

import pyttsx3
import speech_recognition

from groq_client import GroqClient


class Conversation:
    """Handle voice input and output for chatting with the user."""

    def __init__(self):
        """Initialize the text-to-speech engine, recognizer and Groq client."""
        self.engine = pyttsx3.init()
        self.recognizer = speech_recognition.Recognizer()
        self.groq_client = GroqClient()

    def listen(self):
        """Continuously listen to the microphone and respond."""
        print("Started listening...")

        while True:
            with speech_recognition.Microphone() as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = self.recognizer.listen(source)

                try:
                    print("Recognizing...")
                    text = self.recognizer.recognize_google(audio)
                    text = text.lower()

                    print("User:" + text)

                    self.respond(text)

                except speech_recognition.UnknownValueError:
                    print("Speech recognition could not understand your audio")
                except speech_recognition.RequestError as e:
                    print("Could not request results from Google Speech Recognition service; {0}".format(e))


    def respond(self, text):
        """Get a text response from the Groq model and speak it."""
        res = self.groq_client.get_text_response("You are a conversational droid.", text)

        print("Droid:" + res)

        self.speak(res)

    def speak(self, text):
        """Output synthesized speech for the supplied text."""
        self.engine.say(text)
        self.engine.runAndWait()
