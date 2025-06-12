import speech_recognition
from groq_client import get_text_response
import pyttsx3

recognizer = speech_recognition.Recognizer()


def speak_text(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()
    engine.stop()
    print("Speak Text:", text)


def init_conversation():
    print("Initializing conversation...")

    while True:
        with speech_recognition.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio = recognizer.listen(source)

            try:
                print("Listening...")
                text = recognizer.recognize_sphinx(audio)
                text = text.lower()

                print("User:" + text)

                res = get_text_response("You are a conversational droid.", text)

                print("Droid:" + res)

                speak_text(res)

            except speech_recognition.UnknownValueError:
                print("Speech recognition could not understand your audio")
            except speech_recognition.RequestError as e:
                print("Could not request results from Google Speech Recognition service; {0}".format(e))

            print(text)
