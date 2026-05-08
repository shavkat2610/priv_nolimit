import pyautogui 
import time
from scripts.shavkats_functions import position_the_game


time.sleep(2.5)

# position_the_game()
time.sleep(2.5)
# time.sleep(5)
# print(pyautogui.position())
position = pyautogui.position()
print(position)
im = pyautogui.screenshot(region=(position[0], position[1], 75, 75))
# pixels = im.load()
# print(pixels[904, 362])
im.save("get_position_screenshot.png")






