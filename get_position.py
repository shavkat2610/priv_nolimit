import pyautogui 
import time
from scripts.shavkats_functions import position_the_game


time.sleep(1)

position_the_game()
time.sleep(1.5)
# time.sleep(5)
print(pyautogui.position())






