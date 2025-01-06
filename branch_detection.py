import cv2
import numpy as np

def detect_branch(hsv_image):
    # Gray color range
    lower_gray = np.array([140, 26, 80])
    upper_gray = np.array([170, 55, 194])

    # Brown color range
    lower_brown = np.array([9, 65, 102])
    upper_brown = np.array([14, 220, 220])

    # Blue color range
    lower_blue = np.array([100, 20, 20])
    upper_blue = np.array([115, 255, 200])

    # Create masks for each range
    mask_gray = cv2.inRange(hsv_image, lower_gray, upper_gray)
    mask_brown = cv2.inRange(hsv_image, lower_brown, upper_brown)
    mask_blue = cv2.inRange(hsv_image, lower_blue, upper_blue)

    # Combine the masks using bitwise OR
    combined_mask = cv2.bitwise_or(mask_gray, mask_brown)
    combined_mask = cv2.bitwise_or(combined_mask, mask_blue)

    # Apply the combined mask to the hsv image
    masked_image = cv2.bitwise_and(hsv_image, hsv_image, mask=combined_mask)

    # Find contours
    contours, _ = cv2.findContours(combined_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Loop through contours
    for contour in contours:
        # Approximate the contour to a polygon
        approx = cv2.approxPolyDP(contour, 0.01 * cv2.arcLength(contour, True), True)

        # Check if the approximated polygon has 4 or 5 vertices (rectangle)
        if len(approx) == 4 or len(approx) == 5:
            # Draw bounding around the contour
            x, y, w, h = cv2.boundingRect(contour)
            aspect_ratio = w / h
            if aspect_ratio > 2.61 and cv2.contourArea(contour) > 300:
                return True

    return False
