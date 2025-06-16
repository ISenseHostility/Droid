from vision import Vision

def test_average_bbox():
    vision = Vision()
    vision.bbox_history.extend([
        (0, 0, 10, 10),
        (2, 2, 12, 12),
        (4, 4, 14, 14),
    ])
    assert vision.average_bbox() == (2, 2, 12, 12)
