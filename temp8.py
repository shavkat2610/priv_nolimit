


from PIL import Image
from small_shwatsgoingon import tess_read_playerinfo 











im = Image.open('read_p_i_no_read_1774851290.png')

pixels = im.load()

# invert image
for i in range(im.size[0]):
    for j in range(im.size[1]):
        r, g, b, _ = pixels[i, j]
        pixels[i, j] = (255 - r, 255 - g, 255 - b)


# binary thresholding
for i in range(im.size[0]):
    for j in range(im.size[1]):
        r, g, b, _ = pixels[i, j]
        if r > 130:
            pixels[i, j] = (255, 255, 255)
        else:
            # pixels[i, j] = (0, 0, 0)
            pass

# im.show()

# im.save('read_p_i_no_read_1774851290_inverted_thresholded.png')


print(tess_read_playerinfo(im))



























