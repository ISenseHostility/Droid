import importlib
import sys
from types import ModuleType, SimpleNamespace
from unittest.mock import MagicMock


def test_custom_model(monkeypatch):
    """GroqClient should use the provided model when requesting completions."""
    dummy_response = SimpleNamespace(
        choices=[SimpleNamespace(message=SimpleNamespace(content="hi"))]
    )

    fake_groq = ModuleType("groq")

    class DummyChat:
        def __init__(self):
            self.completions = SimpleNamespace(
                create=MagicMock(return_value=dummy_response)
            )

    class DummyGroq:
        def __init__(self, api_key=None):
            self.chat = DummyChat()

    fake_groq.Groq = DummyGroq
    monkeypatch.setitem(sys.modules, "groq", fake_groq)

    import groq_client
    importlib.reload(groq_client)

    client = groq_client.GroqClient(model="test-model")
    client.get_text_response("sys", "user")

    client.client.chat.completions.create.assert_called_with(
        messages=[
            {"role": "system", "content": "sys"},
            {"role": "user", "content": "user"},
        ],
        model="test-model",
    )
