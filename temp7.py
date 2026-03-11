





from PIL import Image

from fish_for_cards import crop_wh










im = Image.open('clicking_images/run_three_times_135.png')


im1 = crop_wh(im, 627, 480, 100, 25)

pixels = im1.load()

print(pixels[0, 0])



im1.show()


























