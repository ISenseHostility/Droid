import cv2
import time
from collections import deque

def average_bbox(bbox_history):
    """Compute the average bounding box from recent history."""
    n = len(bbox_history)
    avg = [sum(coord[i] for coord in bbox_history) / n for i in range(4)]
    return tuple(map(int, avg))

def init_vision():
    print("Initializing vision...")

    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

    if not cap.isOpened():
        print("Could not open camera")
        return

    tracker = None
    tracking = False
    frame_count = 0
    bbox_history = deque(maxlen=5)  # Store last 5 boxes for smoothing

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame_display = frame.copy()

        if tracking:
            success, bbox = tracker.update(frame)
            frame_count += 1

            if success:
                bbox_history.append(bbox)

                smoothed_bbox = average_bbox(bbox_history)
                x, y, w, h = smoothed_bbox
                cv2.rectangle(frame_display, (x, y), (x + w, y + h), (0, 255, 0), 2)

                # 🧭 Determine horizontal position
                frame_width = frame.shape[1]
                center_x = x + w // 2

                if center_x < frame_width / 3:
                    position = "LEFT"
                elif center_x < 2 * frame_width / 3:
                    position = "CENTER"
                else:
                    position = "RIGHT"

                cv2.putText(frame_display, f"Position: {position} Frame: {frame_count}", (10, 230),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

                # Re-detect every 30 frames
                if frame_count % 30 == 0:
                    tracking = False
                    tracker = None
            else:
                print("Tracking lost. Re-detecting...")
                tracking = False
                tracker = None

        else:
            # Face detection
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            small_gray = cv2.resize(gray, (0, 0), fx=0.5, fy=0.5)
            faces = face_cascade.detectMultiScale(small_gray, scaleFactor=1.1, minNeighbors=5, minSize=(15, 15))

            if len(faces) > 0:
                x, y, w, h = faces[0]
                x *= 2
                y *= 2
                w *= 2
                h *= 2
                bbox = (x, y, w, h)

                tracker = cv2.TrackerCSRT_create()  # Accurate tracker
                tracker.init(frame, bbox)
                tracking = True
                frame_count = 0
                bbox_history.clear()
                bbox_history.append(bbox)

        cv2.imshow("Smart Face Tracker", frame_display)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
