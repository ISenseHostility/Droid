import importlib
import sys
from types import ModuleType
from unittest.mock import MagicMock

import pytest


def setup_fake_modules(monkeypatch):
    fake_pyttsx3 = ModuleType("pyttsx3")
    fake_pyttsx3.init = MagicMock(return_value=MagicMock())

    fake_sr = ModuleType("speech_recognition")
    fake_sr.Recognizer = MagicMock()
    fake_sr.Microphone = MagicMock()

    fake_gc_mod = ModuleType("groq_client")
    class DummyGroqClient:
        def get_text_response(self, system_message, user_message):
            return "dummy"
    fake_gc_mod.GroqClient = DummyGroqClient

    monkeypatch.setitem(sys.modules, "pyttsx3", fake_pyttsx3)
    monkeypatch.setitem(sys.modules, "speech_recognition", fake_sr)
    monkeypatch.setitem(sys.modules, "groq_client", fake_gc_mod)


def test_respond_invokes_groq_and_speak(monkeypatch):
    setup_fake_modules(monkeypatch)

    import conversation
    importlib.reload(conversation)

    conv = conversation.Conversation()
    conv.groq_client = MagicMock()
    conv.groq_client.get_text_response.return_value = "hello"
    conv.speak = MagicMock()

    conv.respond("hi")

    conv.groq_client.get_text_response.assert_called_with(
        "You are a conversational droid.", "hi"
    )
    conv.speak.assert_called_with("hello")
