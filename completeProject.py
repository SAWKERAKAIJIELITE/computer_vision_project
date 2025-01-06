

import cv2 
import numpy as np 
import keyboard 
from game_cropping import  get_img_slice
from branch_detection import detect_branch
from press_keys import press_key_on_window , find_all_windows,press_key_multiple
from detect_objects import detect_the_object , detect_number_color_range,detect_pure_black_gray
from detect_glass import detect_glass
import time 
from window_cropping import find_the_object
import pyautogui
from game_cropping import get_game_height_ratio


window_name = "Play games, WIN REAL REWARDS! | GAMEE - Personal - Microsoft​ Edge"
window_handler = find_all_windows(window_name)
gray_2template=cv2.imread("2template.png", cv2.IMREAD_GRAYSCALE)
gray_3template=cv2.imread("3template.png", cv2.IMREAD_GRAYSCALE)
gray_4template=cv2.imread("4template.png", cv2.IMREAD_GRAYSCALE)
gray_energy_template=cv2.imread("energy.png", cv2.IMREAD_GRAYSCALE)


person_side = 'right'
move_direction = ''
num_move = 0 
lock_glass_Detection = False
x_min=x_max=y_min=y_max =0 
while True:
    screenshot = pyautogui.screenshot()
    screenshot = np.array(screenshot)
    gray_screenshot = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
    game_template=cv2.imread("gametemplate.png")
    gray_game_template = cv2.cvtColor(game_template, cv2.COLOR_BGR2GRAY)

    cordinates=find_the_object(screenshot,gray_screenshot,game_template,gray_game_template,cv2.SIFT_create(),100)
    if cordinates is not None:  # Replace '!= None' with 'is not None'
        x_min,x_max,y_min,y_max = cordinates
        break;
press_key_on_window(window_handler,'right')
while True:
    if keyboard.is_pressed('q'):
        break
    time.sleep(0.7)
    screenshot = pyautogui.screenshot()
    screenshot = np.array(screenshot)
    screenshot = cv2.cvtColor(screenshot, cv2.COLOR_BGR2RGB)
    game_image = screenshot[y_min:y_max, x_min:x_max]
    game_height_ratio = get_game_height_ratio(game_image)
    # print('hi')
    h , w, c = game_image.shape
    # cropped_game_img = get_img_slice(game_image,h,2,game_height_ratio)
    # cv2.imwrite('ss.png',cropped_game_img)
    # cv2.waitKey(0)
    # # print(person_side,"hahahaha")

    for i in range(1,5) :

        cropped_game_img = get_img_slice(game_image,h,i,game_height_ratio)
        cropped_game_img_pre = get_img_slice(game_image,h,i-1,game_height_ratio)
        center_cropped_image = cropped_game_img_pre[:,int(cropped_game_img_pre.shape[1] * 0.44 ):int(cropped_game_img_pre.shape[1] * 0.55),:]
        # center_cropped_image = cropped_game_img_pre[:,int(cropped_game_img_pre.shape[1] * 7 / 16):int(cropped_game_img_pre.shape[1] * 8 / 15), :]


        center_cropped_image1 = cropped_game_img_pre[:,int(cropped_game_img_pre.shape[1] / 3 ):int(cropped_game_img_pre.shape[1] * 2  / 3 ),:]
        gray_center_cropped_image = cv2.cvtColor(center_cropped_image, cv2.COLOR_BGR2GRAY)
        gray_center_cropped_image1 = cv2.cvtColor(center_cropped_image1, cv2.COLOR_BGR2GRAY)
        hsv_center_cropped_image = cv2.cvtColor(center_cropped_image, cv2.COLOR_BGR2HSV)
        # cv2.imshow('result',center_cropped_image)
        # cv2.waitKey(0)
        if person_side == 'left':
            cropped_game_img1 = cropped_game_img[:,:int(cropped_game_img.shape[1] / 2 ),:]
            cropped_game_img2 = cropped_game_img[:,int(cropped_game_img.shape[1] / 2 ):,:]
            gray_cropped_game_img2 = cv2.cvtColor(cropped_game_img2, cv2.COLOR_BGR2GRAY)
            hsv_img = cv2.cvtColor(cropped_game_img1, cv2.COLOR_BGR2HSV)
            # cv2.imshow('result',cropped_game_img)
            # cv2.waitKey(0)
            # if detect_pure_black_gray()
            if detect_pure_black_gray(gray_cropped_game_img2) and detect_the_object(gray_cropped_game_img2,gray_energy_template,cv2.SIFT_create(),4):
                # print('energy on right _________________________')
                person_side = 'right'
                move_direction = 'right'
                
            else :
                if detect_branch(hsv_img) : 
                    print('left wood','move right',i)
                    person_side = 'right'
                    move_direction = 'right'
                    # print('leftwood',)
                else :
                    move_direction = 'left'
                # pass

        elif  person_side == 'right':
            cropped_game_img1 = cropped_game_img[:,:int(cropped_game_img.shape[1] / 2 ),:]
            cropped_game_img2 = cropped_game_img[:,int(cropped_game_img.shape[1] / 2 ):,:]
            gray_cropped_game_img1 = cv2.cvtColor(cropped_game_img1, cv2.COLOR_BGR2GRAY)
            hsv_img = cv2.cvtColor(cropped_game_img2, cv2.COLOR_BGR2HSV)
            # print("right")
            # cv2.imshow('result',cropped_game_img)
            # cv2.waitKey(0)
            # cv2.imshow('result',cropped_game_img2)
            # cv2.waitKey(0)
            if detect_pure_black_gray(gray_cropped_game_img1) and detect_the_object(gray_cropped_game_img1,gray_energy_template,cv2.SIFT_create(),4):
                    # print('energy on left _________________')
                    person_side = 'left'
                    move_direction = 'left'                
            else :
                if detect_branch(hsv_img) : 
                    # print('right wood')
                    print('right wood','move left',i)
                    person_side = 'left'
                    move_direction = 'left'
                else :
                    move_direction = 'right'
        if detect_number_color_range(hsv_center_cropped_image):
            # print('color range detected')
            if detect_the_object(gray_center_cropped_image,gray_3template,cv2.SIFT_create(),4):
                # press_key_multiple(move_direction,3)
                num_move=3
                # print("3 is detected")

            elif detect_the_object(gray_center_cropped_image,gray_4template,cv2.SIFT_create(),4):
                num_move=4
                # press_key_multiple(move_direction,4)
                # print("4 is detected")
            
            elif detect_the_object(gray_center_cropped_image,gray_2template,cv2.SIFT_create(),7):
                num_move=2
                # press_key_multiple(move_direction,2)
                # print("2 is detected")
            else :
                num_move=1
                press_key_on_window(window_handler,move_direction)
                # cv2.imshow('result',game_image)
                # cv2.waitKey(0)

        else:
            num_move=1
        if  lock_glass_Detection == True :
            lock_glass_Detection = False
            # print('I enter lock_glass_detection',i)
            press_key_multiple(move_direction,num_move)
            # cv2.imshow('lock glass',game_image)
            # cv2.waitKey(0)
            continue
        if detect_glass(gray_center_cropped_image):
            lock_glass_Detection = True
            # if detect_branch(hsv_img) :
            #     print('there is branch above')
                # cv2.imshow('brach detect glass',gray_center_cropped_image)
                # cv2.waitKey(0)
            # print("glass detected",i)
            # cv2.imshow('detect glass',gray_center_cropped_image)
            # cv2.waitKey(0)
            num_move=num_move + 1
            # print("I DETECTED A GLASS FDFD ")
            # print(move_direction,num_move)
        press_key_multiple(move_direction,num_move)


