





from PIL import Image

from fish_for_cards import crop_wh
import pyautogui
import cv2
import numpy as np







im = Image.open('datasets/shmol_watgoinon/connectivity_issues/all_in_1765564357.png')

img_rgb = np.array(im)

# im = Image.open('images/ok.png')

template = cv2.imread('images/ok.png', 1)
template = cv2.cvtColor(template, cv2.COLOR_BGR2RGB)

coordinates = pyautogui.locate(template, img_rgb, confidence=0.9)

print("coordinates: "+str(coordinates.left))

# click(749, 622)

# pixel[782, 527] # is white
im1 = crop_wh(im, coordinates.left, coordinates.top-160, 270, 160)



pixels = im1.load()

print(pixels[0, 0])



im1.show()


























