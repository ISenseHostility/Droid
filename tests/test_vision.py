import numpy as np
from collections import deque
from unittest.mock import MagicMock

import cv2
from vision import Vision


class DummyCapture:
    def __init__(self, *args, **kwargs):
        self.opened = True

    def set(self, *args, **kwargs):
        pass

    def isOpened(self):
        return self.opened


def test_average_bbox(monkeypatch):
    monkeypatch.setattr(cv2, "VideoCapture", lambda *a, **k: DummyCapture())
    v = Vision()
    v.bbox_history = deque([(0, 0, 10, 10), (2, 2, 10, 10), (4, 4, 10, 10)], maxlen=5)
    assert v.average_bbox() == (2, 2, 10, 10)


def test_scale_bbox(monkeypatch):
    monkeypatch.setattr(cv2, "VideoCapture", lambda *a, **k: DummyCapture())
    v = Vision()
    assert v._scale_bbox((10, 20, 15, 25)) == (20, 40, 30, 50)


def test_determine_position(monkeypatch):
    monkeypatch.setattr(cv2, "VideoCapture", lambda *a, **k: DummyCapture())
    v = Vision()
    frame = np.zeros((100, 300, 3), dtype=np.uint8)
    assert v._determine_position(frame, (10, 0, 10, 10)) == "LEFT"
    assert v._determine_position(frame, (110, 0, 10, 10)) == "CENTER"
    assert v._determine_position(frame, (210, 0, 10, 10)) == "RIGHT"
