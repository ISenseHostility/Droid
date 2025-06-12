import cv2
from collections import deque

class Vision:
    def __init__(self, cam_index=0, frame_width=320, frame_height=240):
        self.cam_index = cam_index
        self.frame_width = frame_width
        self.frame_height = frame_height

        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.cap = cv2.VideoCapture(self.cam_index)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.frame_width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.frame_height)

        self.tracker = None
        self.tracking = False
        self.frame_count = 0
        self.bbox_history = deque(maxlen=5)

    # 1. Helper: Calculate Average Bounding Box for Smoother Tracking
    def average_bbox(self):
        n = len(self.bbox_history)
        avg = [sum(coord[i] for coord in self.bbox_history) / n for i in range(4)]
        return tuple(map(int, avg))

    # 2. Main Entry Point: Vision Loop
    def detect_and_track(self):
        if not self.cap.isOpened():
            print("Could not open camera")
            return

        print("Vision system started...")
        while self.cap.isOpened():
            ret, frame = self.cap.read()
            if not ret:
                break

            frame_display = frame.copy()

            if self.tracking:
                self._process_tracking(frame, frame_display)
            else:
                self._detect_face(frame)

            self._display_frame(frame_display)

            cv2.waitKey(1)

        self._release_resources()

    # 3. Handle Face Tracking Logic
    def _process_tracking(self, frame, frame_display):
        success, bbox = self.tracker.update(frame)
        self.frame_count += 1

        if success:
            self._update_bbox_history(bbox)
            smoothed_bbox = self.average_bbox()
            self._draw_bbox(frame_display, smoothed_bbox)
            position = self._determine_position(frame, smoothed_bbox)
            self._draw_position_text(frame_display, position)
            if self.frame_count % 30 == 0:
                self._reset_tracker()
        else:
            print("Tracking lost. Re-detecting...")
            self._reset_tracker()

    # 4. Handle Face Detection and Tracker Initialization
    def _detect_face(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        small_gray = cv2.resize(gray, (0, 0), fx=0.5, fy=0.5)
        faces = self.face_cascade.detectMultiScale(
            small_gray, scaleFactor=1.1, minNeighbors=5, minSize=(15, 15)
        )

        if len(faces) > 0:
            bbox = self._scale_bbox(faces[0])
            self._init_tracker(frame, bbox)

    # 5. Draw Bounding Box on Frame
    def _draw_bbox(self, frame_display, bbox):
        x, y, w, h = bbox
        cv2.rectangle(frame_display, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # 6. Display Position Text on Frame
    def _draw_position_text(self, frame_display, position):
        cv2.putText(frame_display, f"Position: {position} Frame: {self.frame_count}", (10, 230),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

    # 7. Determine Face Position in Frame
    def _determine_position(self, frame, bbox):
        frame_width = frame.shape[1]
        x, y, w, h = bbox
        center_x = x + w // 2
        if center_x < frame_width / 3:
            return "LEFT"
        elif center_x < 2 * frame_width / 3:
            return "CENTER"
        else:
            return "RIGHT"

    # 8. Show Frame
    def _display_frame(self, frame_display):
        cv2.imshow("Smart Face Tracker", frame_display)

    # 9. Update Bounding Box History for Smoothing
    def _update_bbox_history(self, bbox):
        self.bbox_history.append(bbox)

    # 10. Scale Bounding Box Back to Original Size
    def _scale_bbox(self, bbox):
        x, y, w, h = bbox
        return (x * 2, y * 2, w * 2, h * 2)

    # 11. Initialize the Face Tracker
    def _init_tracker(self, frame, bbox):
        self.tracker = cv2.TrackerCSRT_create()
        self.tracker.init(frame, bbox)
        self.tracking = True
        self.frame_count = 0
        self.bbox_history.clear()
        self.bbox_history.append(bbox)

    # 12. Reset Tracker State
    def _reset_tracker(self):
        self.tracking = False
        self.tracker = None

    # 13. Release Resources at End
    def _release_resources(self):
        self.cap.release()
        cv2.destroyAllWindows()
