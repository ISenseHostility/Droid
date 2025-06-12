import sys
from threading import Thread

from conversation import init_conversation
from vision import init_vision

threads = []


def main():
    vision_thread = Thread(target=init_vision)
    conversation_thread = Thread(target=init_conversation)

    vision_thread.daemon = True
    # conversation_thread.daemon = True

    threads.append(vision_thread)
    # threads.append(conversation_thread)

    for thread in threads:
        thread.start()

    while True:
        if 0xFF == ord('q'):
            sys.exit(0)


if __name__ == "__main__":
    main()
