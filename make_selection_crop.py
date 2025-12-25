from PIL import Image
import pyautogui
import time
from scripts.shavkats_functions import game_screenshot, screenshot_area






# im = Image.open('ace_1.png') # point = (0, 100), size = [900, 540]

# print('im.size: '+str(im.size))

# im = im.crop((300, 300, 450, 400))


time.sleep(3)

# im = Image.open('screenshot_1763726573.png')
im = screenshot_area(point = (50, 395), size = [300, 70], file_name=None)

def crop_wh(im, left, top, width, height):
    return im.crop((left, top, left + width, top + height))

im.show()

im2 = crop_wh(im, 0, 0, 300, 70)



im2.save("images/new_selection.png")


# print(pyautogui.locate(im2, im, confidence=.9))



# print(pyautogui.locate(im2, im, confidence=.9))


# im2.show()

exit()

im3 = crop_wh(im, 399, 195, 25, 25)

# im3.show()

# im3.save("A2.png")


# card1 = crop_wh(im, 370, 400, 35, 45)
# card1.show()
# card2 = crop_wh(im, 415, 395, 35, 45)
# card2.show()

# value_left = crop_wh(im, 377, 399, 20, 20)
# value_left.show()

# suit_left = crop_wh(im, 378, 427, 20, 20)
# suit_left.show()

# value_right = crop_wh(im, 423, 397, 20, 20)
# value_right.show()

# suit_right = crop_wh(im, 417, 421, 20, 20)
# suit_right.show()