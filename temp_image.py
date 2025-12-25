from scripts.shavkats_functions import screenshot_area
import pyautogui

# im = screenshot_area(point = (0, 0), size = [700, 530], file_name=f"temp_screenshot.png")
im = pyautogui.screenshot()

width, height = im.size

print(width)

pixels = im.load()

pixel_value = pixels[499, 329]
print(pixel_value)

pix = pyautogui.pixel(499, 329)

print(pix)
