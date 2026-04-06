from PIL import Image

from fish_for_cards import crop_wh










im = Image.open('big_screenshot.png')


im1 = crop_wh(im, 20, 250, 200, 200)

pixels = im1.load()

print(pixels[0, 0])



im1.show()







