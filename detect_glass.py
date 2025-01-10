from typing import Any
import cv2 as cv
import numpy as np


def detect_glass(image) -> bool:

    edges: Any = cv.Canny(image, 130, 200)
    lines: Any = cv.HoughLinesP(
        edges,
        rho=1,
        theta=np.pi / 180,
        threshold=50,
        minLineLength=10,
        maxLineGap=6
    )

    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            image_length: Any = image.shape[1]

            if abs(y2 - y1) < abs(x2 - x1):
                length = np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
                if 12 < length < image_length + 3:
                    return True
    return False
