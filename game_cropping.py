import numpy as np 
# import cv2

def get_game_height_ratio(cropped_game):
    # Crop the game area
    orginal_game_height , orginal_game_width = (885, 674)
    game_height , game_width = cropped_game.shape[0:2]
    game_height_ratio = game_height / orginal_game_height

    return game_height_ratio

# def get_img_slice(image,h , slice_number=0,ratio = 1,min=190,max=290) :
#     min *= ratio
#     max *= ratio
#     offset = slice_number * 100 * ratio
#     return image[int(h - (max + offset)) : int(h - (min + offset))]

def get_img_slice(image,h , slice_number=0,ratio = 1,min=180,max=280) :
    min *= ratio
    max *= ratio
    offset = slice_number * 100 * ratio
    return image[int(h - (max + offset)) : int(h - (min + offset))]