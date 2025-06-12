import pyttsx3
import speech_recognition

from groq_client import GroqClient


class Conversation:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.recognizer = speech_recognition.Recognizer()
        self.groq_client = GroqClient()

        self.listen()

    def listen(self):
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

                print(text)

    def respond(self, text):
        res = self.groq_client.get_text_response("You are a conversational droid.", text)

        print("Droid:" + res)

        self.speak(res)

    def speak(self, text):
        self.engine.say(text)
        self.engine.runAndWait()