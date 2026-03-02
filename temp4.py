from PIL import Image


im1 = Image.open("images/global_sit_checked.png")

pixels = im1.load()

i = 2
j = 10
print(pixels[i, j])
pixels[i, j] = (255, 0, 0)
im1.show()
















































