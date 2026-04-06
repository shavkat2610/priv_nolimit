import time

from PIL import Image

from fish_for_cards import crop_wh
from small_shwatsgoingon import tess_read










im = Image.open('own_money_no_read_1775429294.png')


im1 = crop_wh(im, 378, 495, 95, 25) 

pixels = im1.load() # create the pixel map
for i in range(im1.size[0]): # for every pixel:
    for j in range(im1.size[1]):
        # print(pixels[i, j])
        if pixels[i, j][1] >= 140: # 140 initially 
            pixels[i, j] = (0, 0, 0, 255)
        else:
            if pixels[i,j][0] >= 90 or pixels[i,j][1] >= 90 or pixels[i,j][2] >= 90:
                print(pixels[i,j])
                pixels[i, j] = (0, 0, 0, 255)
            else:
                pixels[i,j] = (255, 255, 255, 255)
im1.save(f"own_money_no_read_{str(time.time())[:10]}_processed.png")
# exit()
read_3 = tess_read(im1)
print("read_own_money tess_read result: "+str(read_3))

























































