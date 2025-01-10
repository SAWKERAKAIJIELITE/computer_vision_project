import cv2 as cv
import numpy as np

def detect_branch(hsv_image) -> bool:

    lower_gray = np.array([140, 26, 80])
    upper_gray = np.array([170, 55, 194])

    lower_brown = np.array([9, 65, 102])
    upper_brown = np.array([14, 220, 220])

    lower_blue = np.array([100, 20, 20])
    upper_blue = np.array([115, 255, 200])

    mask_gray = cv.inRange(hsv_image, lower_gray, upper_gray)
    mask_brown = cv.inRange(hsv_image, lower_brown, upper_brown)
    mask_blue = cv.inRange(hsv_image, lower_blue, upper_blue)

    combined_mask = cv.bitwise_or(mask_gray, mask_brown)
    combined_mask = cv.bitwise_or(combined_mask, mask_blue)

    # Apply the combined mask to the hsv image
    masked_image = cv.bitwise_and(hsv_image, hsv_image, mask=combined_mask)

    contours, _ = cv.findContours(combined_mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        approx = cv.approxPolyDP(contour, 0.01 * cv.arcLength(contour, True), True)

        if len(approx) == 4 or len(approx) == 5:
            # Draw bounding around the contour
            x, y, w, h = cv.boundingRect(contour)
            aspect_ratio = w / h
            # if aspect_ratio > 2.61 and cv.contourArea(contour) > 300:
            if aspect_ratio > 2.5 and cv.contourArea(contour) > 250:
                return True

    return False
