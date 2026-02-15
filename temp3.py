









from fish_for_cards import game_screenshot




import time



while True:
    im = game_screenshot()
    im.save(f"screenshots/test_screenshot_{str(time.time())[:12].replace('.', '_')}.png")
    time.sleep(1.0)







