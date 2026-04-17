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

if pixels[340, 460][1]> 100 and pixels[342, 460][0] > 200:
    print("\nimma try clicking ok here")

    
































