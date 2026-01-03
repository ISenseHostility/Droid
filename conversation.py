import pyttsx3
import speech_recognition

from groq_client import GroqClient
from conversation_state import ConversationState


class Conversation:
    def __init__(self, mic_index=None):
        self.engine = None
        self.recognizer = speech_recognition.Recognizer()
        self.groq_client = GroqClient()
        self.mic_index = mic_index
        
        system_message = (
            "You are Droid, a highly advanced and helpful robotic companion. "
            "Your personality is robotic, straight-to-the-point, and slightly eccentric. "
            "Keep your responses concise and engaging, suitable for voice interaction. "
            "You can see and track people in your field of vision, which makes you feel more 'alive'. "
            "Always maintain the persona of a helpful droid."
        )
        self.state = ConversationState(system_message=system_message)

    def listen(self):
        print(f"Started listening (Mic index: {self.mic_index})...")

        if self.engine is None:
            self.engine = pyttsx3.init()

        try:
            mic = speech_recognition.Microphone(device_index=self.mic_index)
            print("Adjusting for ambient noise...")
            with mic as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
            print("Energy threshold after adjustment:", self.recognizer.energy_threshold)

            while True:
                try:
                    print("\nListening for input...")
                    with mic as source:
                        audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)

                    print("Recognizing...")
                    text = self.recognizer.recognize_google(audio)
                    text = text.lower()

                    print("User:" + text)

                    self.respond(text)

                except speech_recognition.WaitTimeoutError:
                    continue
                except speech_recognition.UnknownValueError:
                    print("Speech recognition could not understand your audio")
                except speech_recognition.RequestError as e:
                    print("Could not request results from Google Speech Recognition service; {0}".format(e))
                except Exception as e:
                    print(f"An unexpected error occurred in the loop: {e}")
        except Exception as e:
            print(f"Failed to initialize microphone or engine: {e}")


    def respond(self, text):
        print("DEBUG: respond() started")
        self.state.add_user_message(text)
        res = self.groq_client.get_text_response(self.state.get_messages())
        self.state.add_assistant_message(res)

        print("Droid:" + res)

        self.speak(res)
        print("DEBUG: respond() finished")

    def speak(self, text):
        print("DEBUG: speak() started")
        # Ensure engine is initialized (should be already, but for safety)
        if self.engine is None:
            self.engine = pyttsx3.init()
        self.engine.say(text)
        self.engine.runAndWait()
        print("DEBUG: speak() finished")