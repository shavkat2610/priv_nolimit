import numpy as np
from scripts.shavkats_functions import game_screenshot
import cv2
from PIL import Image

# arr = np.empty()
# print(arr)


im = game_screenshot()

print("type(im) =", type(im))

im_array = np.array(im)
print("im_array.shape: "+str(im_array.shape))
exit()


print("type(im_array) =", type(im_array))
print("im_array.shape =", im_array.shape)
print("im_array.dtype =", im_array.dtype)
# print("im_array =", im_array)
cv2.imshow("screenshot", im_array)
cv2.waitKey(0)


cv2.destroyAllWindows()


pil_ = Image.fromarray(im_array)
pil_.show()
print("type(pil_) =", type(pil_))
print("pil_.size =", pil_.size)
print("pil_.mode =", pil_.mode)

