from PIL import Image
from scripts.shavkats_functions import check_if_w8_for_blinds




im = Image.open("temp_screenshot/check_boxes.png")
print(check_if_w8_for_blinds(im))

