from fish_for_cards import game_screenshot
import time
from scripts.shavkats_functions import position_the_game

time.sleep(5.0)

position_the_game()

while True:
    im = game_screenshot()
    im.save(f"screenshots/test_screenshot_{str(time.time())[:12].replace('.', '_')}.png")
    time.sleep(1.0)







