"""Speech-based conversation interface for interacting with the Groq API."""

import logging
import pyttsx3
import speech_recognition

from groq_client import GroqClient

logger = logging.getLogger(__name__)


class Conversation:
    """Handle voice input and output for chatting with the user."""

    def __init__(
        self,
        stop_event=None,
        system_prompt="You are a conversational droid.",
        groq_model="llama-3.1-8b-instant",
    ):
        """Initialize the text-to-speech engine, recognizer and Groq client.

        Parameters
        ----------
        stop_event : threading.Event, optional
            Event used to signal when the listening loop should terminate.
        system_prompt : str, optional
            Custom system prompt to pass to the model. Defaults to
            "You are a conversational droid.".
        groq_model : str, optional
            Name of the Groq model to use. Defaults to
            "llama-3.1-8b-instant".
        """
        self.engine = pyttsx3.init()
        self.recognizer = speech_recognition.Recognizer()
        self.groq_client = GroqClient(model=groq_model)
        # Prompt used when requesting completions
        self.system_prompt = system_prompt
        # Shared stop event allows external callers to shut down the loop
        self.stop_event = stop_event

    def listen(self):
        """Continuously listen to the microphone and respond."""
        logger.info("Started listening...")

        # Run until an external shutdown signal is received
        while self.stop_event is None or not self.stop_event.is_set():
            with speech_recognition.Microphone() as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = self.recognizer.listen(source)

                try:
                    logger.info("Recognizing...")
                    text = self.recognizer.recognize_google(audio)
                    text = text.lower()

                    logger.info("User: %s", text)

                    self.respond(text)

                except speech_recognition.UnknownValueError:
                    logger.error(
                        "Speech recognition could not understand your audio"
                    )
                except speech_recognition.RequestError as e:
                    logger.error(
                        "Could not request results from Google Speech "
                        "Recognition service; %s",
                        e,
                    )

        logger.info("Stopped listening")

    def respond(self, text):
        """Get a text response from the Groq model and speak it."""
        res = self.groq_client.get_text_response(self.system_prompt, text)

        logger.info("Droid: %s", res)

        self.speak(res)

    def speak(self, text):
        """Output synthesized speech for the supplied text."""
        self.engine.say(text)
        self.engine.runAndWait()
