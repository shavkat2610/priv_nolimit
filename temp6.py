from PIL import Image

from fish_for_cards import crop_wh










im = Image.open('temp_screenshot/plyerdata/game_screenshot1764980788.png')


im1 = crop_wh(im, 327, 20, 200, 200)

pixels = im1.load()

print(pixels[0, 0])



im1.show()







