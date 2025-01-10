import time
from typing import Any
import cv2 as cv
import numpy as np
import keyboard
import pyautogui
from game_cropping import get_img_slice, get_game_height_ratio
from branch_detection import detect_branch
from press_keys import press_key_on_window, find_all_windows, press_key_multiple
from detect_objects import detect_the_object, detect_number_color_range, detect_pure_black_gray
from detect_glass import detect_glass
from window_cropping import find_the_object


WINDOW_NAME = "Play games, WIN REAL REWARDS! | GAMEE - Personal - Microsoft​ Edge"
window_handler: list[Any] = find_all_windows(WINDOW_NAME)
gray_2template = cv.imread("2template.png", cv.IMREAD_GRAYSCALE)
gray_3template = cv.imread("3template.png", cv.IMREAD_GRAYSCALE)
gray_4template = cv.imread("4template.png", cv.IMREAD_GRAYSCALE)
gray_energy_template = cv.imread("energy.png", cv.IMREAD_GRAYSCALE)


person_side = 'right'
move_direction = ''
num_move = 0
lock_glass_Detection = False
x_min = x_max = y_min = y_max = 0

while True:
    screenshot = pyautogui.screenshot()
    screenshot = np.array(screenshot)
    gray_screenshot = cv.cvtColor(screenshot, cv.COLOR_BGR2GRAY)
    game_template = cv.imread("game-template.png")
    gray_game_template = cv.cvtColor(game_template, cv.COLOR_BGR2GRAY)

    coordinates = find_the_object(
        screenshot,
        gray_screenshot,
        game_template,
        gray_game_template,
        cv.SIFT_create(),
        100
    )
    if coordinates is not None:  # Replace '!= None' with 'is not None'
        x_min, x_max, y_min, y_max = coordinates
        break

press_key_on_window(window_handler, 'right')

sleep_time = 0.8

while True:
    if keyboard.is_pressed('q'):
        break

    time.sleep(sleep_time)
    sleep_time = 0.8

    screenshot = pyautogui.screenshot()
    screenshot = np.array(screenshot)
    screenshot = cv.cvtColor(screenshot, cv.COLOR_BGR2RGB)

    game_image: np.ndarray[
        Any,
        np.dtype[np.integer[Any] | np.floating[Any]]
    ] = screenshot[y_min:y_max, x_min:x_max]

    h, w, c = game_image.shape

    game_height_ratio = get_game_height_ratio(game_image)

    for i in range(1, 5):

        cropped_game_img = get_img_slice(
            game_image,
            h,
            i,
            game_height_ratio
        )
        cropped_game_img_pre = get_img_slice(
            game_image,
            h,
            i-1,
            game_height_ratio
        )
        center_cropped_image = cropped_game_img_pre[
            :,
            int(cropped_game_img_pre.shape[1] * 0.44):int(cropped_game_img_pre.shape[1] * 0.55),
            :
        ]
        center_cropped_image1 = cropped_game_img_pre[
            :,
            int(cropped_game_img_pre.shape[1] / 3):int(cropped_game_img_pre.shape[1] * 2 / 3),
            :
        ]

        gray_center_cropped_image = cv.cvtColor(
            center_cropped_image,
            cv.COLOR_BGR2GRAY
        )
        gray_center_cropped_image1 = cv.cvtColor(
            center_cropped_image1,
            cv.COLOR_BGR2GRAY
        )
        hsv_center_cropped_image = cv.cvtColor(
            center_cropped_image,
            cv.COLOR_BGR2HSV
        )

        if person_side == 'left':
            cropped_game_img1 = cropped_game_img[
                :,
                :int(cropped_game_img.shape[1] / 2),
                :
            ]
            cropped_game_img2 = cropped_game_img[
                :,
                int(cropped_game_img.shape[1] / 2):,
                :
            ]

            gray_cropped_game_img2 = cv.cvtColor(
                cropped_game_img2,
                cv.COLOR_BGR2GRAY
            )
            hsv_img = cv.cvtColor(cropped_game_img1, cv.COLOR_BGR2HSV)

            if detect_pure_black_gray(gray_cropped_game_img2) and detect_the_object(gray_cropped_game_img2, gray_energy_template, cv.SIFT_create(), 4):
                sleep_time = 2.5
                person_side = 'right'
                move_direction = 'right'

            else:
                if detect_branch(hsv_img):
                    print('left wood', 'move right', i)
                    person_side = 'right'
                    move_direction = 'right'
                else:
                    move_direction = 'left'

        elif person_side == 'right':
            cropped_game_img1 = cropped_game_img[
                :,
                :int(cropped_game_img.shape[1] / 2),
                :
            ]
            cropped_game_img2 = cropped_game_img[
                :,
                int(cropped_game_img.shape[1] / 2):,
                :
            ]

            gray_cropped_game_img1 = cv.cvtColor(
                cropped_game_img1,
                cv.COLOR_BGR2GRAY
            )
            hsv_img = cv.cvtColor(cropped_game_img2, cv.COLOR_BGR2HSV)

            if detect_pure_black_gray(gray_cropped_game_img1) and detect_the_object(gray_cropped_game_img1, gray_energy_template, cv.SIFT_create(), 4):
                sleep_time = 2.5
                person_side = 'left'
                move_direction = 'left'
            else:
                if detect_branch(hsv_img):
                    print('right wood', 'move left', i)
                    person_side = 'left'
                    move_direction = 'left'
                else:
                    move_direction = 'right'

        if detect_number_color_range(hsv_center_cropped_image):

            if detect_the_object(gray_center_cropped_image, gray_3template, cv.SIFT_create(), 4):
                num_move = 3

            elif detect_the_object(gray_center_cropped_image, gray_4template, cv.SIFT_create(), 4):
                num_move = 4

            elif detect_the_object(gray_center_cropped_image, gray_2template, cv.SIFT_create(), 7):
                num_move = 2
            else:
                num_move = 1
                press_key_on_window(window_handler, move_direction)

        else:
            num_move = 1

        if lock_glass_Detection is True:
            lock_glass_Detection = False

            press_key_multiple(move_direction, num_move)
            continue

        if detect_glass(gray_center_cropped_image):
            lock_glass_Detection = True
            num_move = num_move + 1

        press_key_multiple(move_direction, num_move)
