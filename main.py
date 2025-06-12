from threading import Thread

from conversation import Conversation


class Droid:
    def __init__(self):
        self.threads = []
        self.conversation = Conversation()

    def start(self):
        # vision_thread = Thread(target=init_vision)
        conversation_thread = Thread(target=self.conversation)

        # vision_thread.daemon = True
        conversation_thread.daemon = True

        # threads.append(vision_thread)
        self.threads.append(conversation_thread)

        for thread in self.threads:
            thread.start()

if __name__ == '__main__':
    Droid()
