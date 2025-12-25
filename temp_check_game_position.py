import time
from scripts.shavkats_functions import screenshot_area, position_the_game


time.sleep(3)


position_the_game()


# screenshot_area((765, 40), (80, 40), "images/poker_rules_1.png") # game-rules

screenshot_area((150, 150), size=(450, 450), file_name="temp.png")



