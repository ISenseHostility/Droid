class ConversationState:
    def __init__(self, system_message="You are a helpful assistant."):
        self.messages = []
        self.system_message = system_message
        self.reset()

    def add_user_message(self, message):
        self.messages.append({"role": "user", "content": message})

    def add_assistant_message(self, message):
        self.messages.append({"role": "assistant", "content": message})

    def get_messages(self):
        return [{"role": "system", "content": self.system_message}] + self.messages

    def reset(self):
        self.messages = []
