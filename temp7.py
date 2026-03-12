





from PIL import Image

from fish_for_cards import crop_wh










im = Image.open('shmol_model_not_sure/if_turn_or_no_dec_2.627464.png')

# click(749, 622)

# pixel[782, 527] # is white
im1 = crop_wh(im, 782, 527, 40, 25)

pixels = im1.load()

print(pixels[0, 0])



im1.show()


























