import pyautogui 
import time
from scripts.shavkats_functions import position_the_game


time.sleep(1.5)

# position_the_game()
time.sleep(1.5)
# time.sleep(5)
print(pyautogui.position())
im = pyautogui.screenshot(region=(0, 0, 1000, 900))
pixels = im.load()
print(pixels[904, 362])
# im.save("temp_screenshot.png")






