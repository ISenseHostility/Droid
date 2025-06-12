from threading import Thread
from conversation import Conversation
from vision import Vision

class Droid:
    def __init__(self):
        self.threads = []
        self.conversation = Conversation()
        self.vision = Vision()

    def start(self):
        conversation_thread = Thread(target=self.conversation.listen)
        vision_thread = Thread(target=self.vision.detect_and_track)

        conversation_thread.daemon = True
        vision_thread.daemon = True

        self.threads.extend([conversation_thread, vision_thread])

        for thread in self.threads:
            thread.start()

        for thread in self.threads:
            thread.join()

if __name__ == '__main__':
    Droid().start()
