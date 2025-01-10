from typing import Any
import cv2 as cv
import numpy as np


def detect_the_object(gray_image, gray_template, detector, min_matches: int):
    # Detect key points and compute descriptors
    _, descriptors_template = detector.detectAndCompute(gray_template, None)
    _, descriptors_scene = detector.detectAndCompute(gray_image, None)

    if descriptors_template is None or descriptors_scene is None or len(descriptors_template) == 0 or len(descriptors_scene) == 0:
        print("Descriptors could not be computed.")
        return None

    # FLANN-based matcher parameters
    index_params = {'algorithm': 1, 'trees': 5}  # KDTree-based search
    search_params = {'checks': 50}

    flann = cv.FlannBasedMatcher(index_params, search_params)

    # Match descriptors using k-Nearest Neighbors
    matches = flann.knnMatch(descriptors_template, descriptors_scene, k=2)

    # Apply Lowe's ratio test
    good_matches: list[Any] = []
    for m, n in matches:
        if m.distance < 0.75 * n.distance:  # Lowe's ratio test
            good_matches.append(m)

    # Check if enough matches are found

    return len(good_matches) >= min_matches


def detect_number_color_range(hsv) -> bool:

    lower_yellow = np.array([25, 110, 225])
    upper_yellow = np.array([28, 150, 252])

    mask_yellow = cv.inRange(hsv, lower_yellow, upper_yellow)

    return cv.countNonZero(mask_yellow) > 100


def detect_pure_black_gray(gray_image, min_black_pixels: int = 10):

    mask_black = (gray_image == 0)

    black_pixel_count: Any = np.sum(mask_black)

    return black_pixel_count >= min_black_pixels
