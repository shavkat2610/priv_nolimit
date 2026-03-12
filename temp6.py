from PIL import Image

from fish_for_cards import crop_wh










im = Image.open('datasets/shmol_watgoinon/no_decision_to_be_made/game_screenshot1764672122.png')


im1 = crop_wh(im, 595, 0, 200, 200)

pixels = im1.load()

print(pixels[0, 0])



im1.show()







