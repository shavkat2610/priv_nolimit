















import time

import pytesseract
from fish_for_cards import crop_wh, game_screenshot
from PIL import Image


im2 = Image.open("8BB_non_readable.png")
pixels = im2.load() # create the pixel map
for i in range(im2.size[0]): # for every pixel:
    for j in range(im2.size[1]):
        # print(pixels[i, j])
        if pixels[i, j][1] >= 180:
            pixels[i, j] = (10, 10, 10, 255)
        else:
            pixels[i,j] = (185, 185, 185, 255)
secs = time.time()
im2.show()
# exit()
data = pytesseract.image_to_string(im2)
# print(data)
data = data.split("BB")[0]
data = data.replace("B", "8")
data = data.replace("A", "4")
# im2.save("debug_to_call_"+data+"_"+str(secs).split(".")[0]+".png")
if data != "":
    try:
        print( str(float(data)))
    except Exception as e:
        print("to call: "+data)
        print("NON STRING FOUND IN how_much , please help")
        exit()
else:
    print("probably emty button still")








