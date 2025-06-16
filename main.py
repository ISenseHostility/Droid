"""Entry point for running the droid's conversation and vision threads."""

import logging
from threading import Thread, Event
from conversation import Conversation
from vision import Vision

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Droid:
    """Coordinates the conversation and vision subsystems."""

    def __init__(self):
        """Create subsystem instances and storage for threads."""
        self.threads = []
        # Shared event that signals all threads to shut down gracefully
        self.stop_event = Event()
        self.conversation = Conversation(stop_event=self.stop_event)
        self.vision = Vision(stop_event=self.stop_event)

    def start(self):
        """Launch conversation and vision threads."""
        logger.info("Starting droid")
        conversation_thread = Thread(target=self.conversation.listen)
        vision_thread = Thread(target=self.vision.detect_and_track)

        conversation_thread.daemon = True
        vision_thread.daemon = True

        self.threads.extend([conversation_thread, vision_thread])

        for thread in self.threads:
            thread.start()

        try:
            for thread in self.threads:
                thread.join()
        except KeyboardInterrupt:
            logger.info("Shutdown requested by user")
            self.stop_event.set()
            for thread in self.threads:
                thread.join()
        finally:
            logger.info("Droid stopped")

if __name__ == '__main__':
    Droid().start()
