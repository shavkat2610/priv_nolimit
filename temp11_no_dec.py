import time
from PIL import Image

from fish_for_cards import crop_wh
import pyautogui
import cv2
import numpy as np


im = Image.open('own_money_no_read_1776383365.png')


pixels = im.load()

# print(pixels[0, 0])


im.show()

if pixels[627, 475][1] >= 80:
    print("\nrun three times clicked (need to switch to two I think, they dont play three around here ...)")
    # click(x=627, y=570, im = im, debug = True, calling_function = "handle_all_in")
    # return False

    
































