import cv2 
import numpy as np

def detect_the_object(gray_image, gray_template, detector, min_matches):
    # Detect keypoints and compute descriptors
    keypoints_template, descriptors_template = detector.detectAndCompute(gray_template, None)
    keypoints_scene, descriptors_scene = detector.detectAndCompute(gray_image, None)

    # if descriptors_template is None or descriptors_scene is None:
    #     print("Descriptors could not be computed.")
    #     return None
    
    if descriptors_template is None or descriptors_scene is None or len(descriptors_template) == 0 or len(descriptors_scene) == 0:
        print("Descriptors could not be computed.")
        return None

    # FLANN-based matcher parameters
    index_params = dict(algorithm=1, trees=5)  # KDTree-based search
    search_params = dict(checks=50)           # Number of checks
    flann = cv2.FlannBasedMatcher(index_params, search_params)

    # Match descriptors using k-Nearest Neighbors
    matches = flann.knnMatch(descriptors_template, descriptors_scene, k=2)

    # Apply Lowe's ratio test
    good_matches = []
    for m, n in matches:
        if m.distance < 0.75 * n.distance:  # Lowe's ratio test
            good_matches.append(m)

    # Check if enough matches are found
    if len(good_matches) >= min_matches:
        return True
    else:
        return False
    
def detect_number_color_range(hsv):
    lower_yellow = np.array([25, 110, 225])
    upper_yellow = np.array([28, 150, 252])

    mask_yellow = cv2.inRange(hsv, lower_yellow, upper_yellow)

    if cv2.countNonZero(mask_yellow) > 100:
        return True 
    return False

def detect_pure_black_gray(gray_image, min_black_pixels=10):
    mask_black = (gray_image == 0)

    black_pixel_count = np.sum(mask_black)
    return black_pixel_count >= min_black_pixels


# keypoints_template, descriptors_template = detector.detectAndCompute(gray_template, None)
# keypoints_template , keypoints_template