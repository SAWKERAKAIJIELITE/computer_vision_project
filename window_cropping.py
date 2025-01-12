from typing import Any
import numpy as np
import cv2 as cv


def find_the_object(image5, gray_image5, imageTemplate, gray_template, detector, min_matches: int):

    key_points_template, descriptors_template = detector.detectAndCompute(
        gray_template,
        None
    )
    key_points_scene, descriptors_scene = detector.detectAndCompute(
        gray_image5,
        None
    )

    if descriptors_template is None or descriptors_scene is None:
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
    if len(good_matches) >= min_matches:
        print(f"Accepted number of good matches: {len(good_matches)}")

        # Extract locations of good matches
        src_pts = np.float32(
            [key_points_template[m.queryIdx].pt for m in good_matches]
        ).reshape(-1, 1, 2)

        dst_pts = np.float32(
            [key_points_scene[m.trainIdx].pt for m in good_matches]
        ).reshape(-1, 1, 2)

        # Compute the homography matrix
        H, mask = cv.findHomography(src_pts, dst_pts, cv.RANSAC, 5.0)

        if H is not None:
            # Transform template corners to scene image
            h, w = gray_template.shape
            template_corners = np.float32(
                [[0, 0], [w, 0], [w, h], [0, h]]
            ).reshape(-1, 1, 2)
            scene_corners = cv.perspectiveTransform(template_corners, H)

            # Calculate the bounding box in the scene image
            x_coords = scene_corners[:, 0, 0]
            y_coords = scene_corners[:, 0, 1]
            x_min, x_max = int(x_coords.min()), int(x_coords.max())
            y_min, y_max = int(y_coords.min()), int(y_coords.max())

            # Ensure coordinates are within image bounds
            x_min, x_max = max(0, x_min), min(image5.shape[1], x_max)
            y_min, y_max = max(0, y_min), min(image5.shape[0], y_max)

            return (x_min, x_max, y_min, y_max)

        return None

    print(f"Found {len(good_matches)} matches, need at least {min_matches}")

    return None
