import os
import pyautogui
import time
import numpy as np
# import cv2
# import random
# import glob
from PIL import Image

# big_blind = "200"


# remove_debug_imgs()


# run_it_up(big_blind = big_blind)


def screenshot_area(point = (50, 50), size = [250, 250], file_name = None):
    im = pyautogui.screenshot(region=(point[0], point[1], size[0], size[1]))
    # secs = time.time()
    # im2 = pyautogui.screenshot(region=(8, 32, 50, 50))
    if file_name != None:
        im.save(file_name)
    return im



def game_screenshot(save = False):
    if not save:
        im = screenshot_area(point = (0, 95), size = [830, 540], file_name=None)
    else:
        secs = time.time()
        im = screenshot_area(point = (0, 95), size = [830, 540], file_name=f"screenshots/game_screenshot{str(secs).split(".")[0]}.png")
    return im






def compare_num(im,im2, max_ = 500, max_diff_one = 4.5, max_diff_two = 7., max_diff_three = 25., max_diff_four = 40., points_allowed = 500., debug = True): # must be numpy arrays
    # comparing numpy images
    if (im.shape!=im2.shape):
        if debug:
            print("compare numpy unsuccessful due to different shapes")
        return False
    im = im.flatten()[:max_]
    im2 = im2.flatten()[:max_]
    diffs = im-im2
    for diff in diffs:
        if points_allowed < 0.0:
            # print("compare_num uns")
            return False
        if abs(diff)>=max_diff_one:
            points_allowed-=2.
            if abs(diff)>=max_diff_two:
                points_allowed-=abs(diff)
                if abs(diff)>=max_diff_three:
                    points_allowed-=abs(diff)*1.2
                    if abs(diff)>=max_diff_four:
                        points_allowed-=abs(diff)*1.5
    if points_allowed < 0.0:
        # print("compare_num uns")
        return False                        

    if debug:
        if points_allowed<300:
            print("\n !!!!!!!!!!!!!!!!!!!!!!!!  compare numpy points left: "+str(points_allowed) +"!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! \n")
    return True




def crop_wh(game_img, left, top, width, height):
    return game_img.crop((left, top, left + width, top + height))


def own_value_left(im, save = False): # im = game screenshot
    if not save:
        return crop_wh(im, 377, 399, 20, 20)
    im = crop_wh(im, 377, 399, 20, 20)
    im.save(f"screenshots/own_value_left_{str(time.time()).split('.')[0]}.png")
    return im

def own_suit_left(im, save = False):
    if not save:
        return crop_wh(im, 378, 427, 20, 20)
    im = crop_wh(im, 378, 427, 20, 20)
    im.save(f"screenshots/own_suit_left_{str(time.time()).split('.')[0]}.png")
    return im

def own_value_right(im, save = False):
    if not save:
        return crop_wh(im, 423, 397, 20, 20)
    im = crop_wh(im, 423, 397, 20, 20)
    im.save(f"screenshots/own_value_right_{str(time.time()).split('.')[0]}.png")
    return im

def own_suit_right(im, save = False):
    if not save:
        return crop_wh(im, 417, 421, 20, 20)
    im = crop_wh(im, 417, 421, 20, 20)
    im.save(f"screenshots/own_suit_right_{str(time.time()).split('.')[0]}.png")
    return im



# if not os.path.exists("fish/deck1/value/"):
#     os.makedirs("fish/deck1/value/")
# if not os.path.exists("fish/deck1/suit/"):
#     os.makedirs("fish/deck1/suit/")
# if not os.path.exists("fish/deck2/value/"):
#     os.makedirs("fish/deck2/value/")
# if not os.path.exists("fish/deck2/suit/"):
#     os.makedirs("fish/deck2/suit/")

# if not os.path.exists("fish/deck3/value/"):
#     os.makedirs("fish/deck3/value/")
# if not os.path.exists("fish/deck3/suit/"):
#     os.makedirs("fish/deck3/suit/")

# if not os.path.exists("fish/deck4/value/"):
#     os.makedirs("fish/deck4/value/")
# if not os.path.exists("fish/deck4/suit/"):
#     os.makedirs("fish/deck4/suit/")

# if not os.path.exists("fish/deck5/value/"):
#     os.makedirs("fish/deck5/value/")
# if not os.path.exists("fish/deck5/suit/"):
#     os.makedirs("fish/deck5/suit/")









own_suits_right = []
own_suits_left = []
own_values_left = []
own_values_right = []

own_card_left_filenames = []
own_card_right_filenames = []





def check_if_included(new_img_array, existing_arrays, debug = False):
    for arr in existing_arrays:
        if np.array_equal(new_img_array, arr):
            return True
        elif compare_num(new_img_array, arr, debug=debug):
            return True
    return False



def prepare_fishing_own_cards():

    global own_values_left
    global own_suits_left
    global own_values_right
    global own_suits_right

    global own_card_left_filenames 
    global own_card_right_filenames

    # load here if any collected yet
    directory = os.fsencode("fish/own_left/value/")
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if filename.endswith(".png"): 
            im = Image.open(f"fish/own_left/value/{filename}")
            im_array = np.array(im)
            own_values_left.append(im_array)
            own_card_left_filenames.append(filename)
        else:
            print(f"found some non png file in fish/own_left/value/, {filename}, skipping...")


    directory = os.fsencode("fish/own_left/suit/")
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if filename.endswith(".png"): 
            im = Image.open(f"fish/own_left/suit/{filename}")
            im_array = np.array(im)
            own_suits_left.append(im_array)
        else:
            print(f"found some non png file in fish/own_left/suit/, {filename}, skipping...")


    directory = os.fsencode("fish/own_right/value/")
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if filename.endswith(".png"): 
            im = Image.open(f"fish/own_right/value/{filename}")
            im_array = np.array(im)
            own_values_right.append(im_array)
            own_card_right_filenames.append(filename)
        else:
            print(f"found some non png file in fish/own_right/value/, {filename}, skipping...")


    directory = os.fsencode("fish/own_right/suit/")
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if filename.endswith(".png"): 
            im = Image.open(f"fish/own_right/suit/{filename}")
            im_array = np.array(im)
            own_suits_right.append(im_array)
        else:
            print(f"found some non png file in fish/own_right/suit/, {filename}, skipping...")




def fish_for_own_cards(im = None):

    print("############------------------fish--------------------##############")

    global own_values_left
    global own_suits_left
    global own_values_right
    global own_suits_right

    # keep a array of all previous reads to compare and avoid duplicates
    # save unique reads only
    # pyautogui.moveTo(1100, 950, duration=0.01)
    # time.sleep(3) 
    # print("read_D(): "+str(read_D()))

    # reading cards
    # open_cards()
    if im == None:
        im = game_screenshot(save = True)
    ovl = np.array(own_value_left(im, save = False))
    osl = np.array(own_suit_left(im, save = False))
    ovr = np.array(own_value_right(im, save = False))
    osr = np.array(own_suit_right(im, save = False))

    # compare with previous reads
    if check_if_included(ovl, own_values_left):
        pass
        # print("own value left duplicate read, {filename}, skipping...")
    else:
        own_values_left.append(ovl)
        Image.fromarray(ovl).save(f"fish/own_left/value/0_{str(time.time()).split('.')[0]}.png")
        print("own value left new read, saved.")

    if check_if_included(osl, own_suits_left):
        pass
        # print("own value left duplicate read, {filename}, skipping...")
    else:
        own_suits_left.append(osl)
        Image.fromarray(osl).save(f"fish/own_left/suit/1_{str(time.time()).split('.')[0]}.png")
        print("own suit left new read, saved.")

    if check_if_included(ovr, own_values_right):
        pass
        # print("own value left duplicate read, {filename}, skipping...")
    else:
        own_values_right.append(ovr)
        Image.fromarray(ovr).save(f"fish/own_right/value/2_{str(time.time()).split('.')[0]}.png")
        print("own value right new read, saved.")

    if check_if_included(osr, own_suits_right):
        pass
        # print("own value left duplicate read, {filename}, skipping...")
    else:
        own_suits_right.append(osr)
        Image.fromarray(osr).save(f"fish/own_right/suit/3_{str(time.time()).split('.')[0]}.png")
        print("own suit right new read, saved.")


    
def red_own_cards(im = None):
    if im == None:
        im = game_screenshot()
    ovl = np.array(own_value_left(im, save = False))
    osl = np.array(own_suit_left(im, save = False))
    ovr = np.array(own_value_right(im, save = False))
    osr = np.array(own_suit_right(im, save = False))

    # for i in range(own_values_left):
    #     if own_values_left[i]

    result = [ "nn", "nn"]
    i = 0
    for current in own_values_left:
        if np.array_equal(ovl, current):
            if own_card_left_filenames[i][1]=="_":
                print(" I HAVE FOUND AN UNDERSCORE IMAGE THING")
                result[0] = "nn"
            else:
                result[0]=own_card_left_filenames[i][:2]
                break
        elif compare_num(ovl, current, debug=False):
            if own_card_left_filenames[i][1]=="_":
                print(" I HAVE FOUND AN UNDERSCORE IMAGE THING")
                result[0] = "nn"
            else:
                result[0]=own_card_left_filenames[i][:2]
                break
        i+=1
    i = 0
    for current in own_values_right:
        if np.array_equal(ovr, current):
            if own_card_right_filenames[i][1]=="_":
                print(" I HAVE FOUND AN UNDERSCORE IMAGE THING")
                result[1] = "nn"
            else:
                result[1]=own_card_right_filenames[i][:2]
                break
        elif compare_num(ovr, current, debug=False):
            if own_card_right_filenames[i][1]=="_":
                print(" I HAVE FOUND AN UNDERSCORE IMAGE THING")
                result[1] = "nn"
            else:
                result[1]=own_card_right_filenames[i][:2]
                break
        i+=1
    # print("read own cards result: "+str(result))
    
    return result





deck_cards = []
deck_card_filenames = []





def prepare_fishing_deck_cards():

    global deck_cards
    global deck_card_filenames


    directory = os.fsencode("fish/deck_cards/")
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if filename.endswith(".png"): 
            im = Image.open(f"fish/deck_cards/{filename}")
            im_array = np.array(im)
            deck_cards.append(im_array)
            deck_card_filenames.append(filename)
        else:
            print(f"found some non png file in fish/deck_cards/, {filename}, skipping...")







def deck_card(im, num, save = False):
    num = num-1
    card_positions = [255, 327, 399, 471, 543] 
    if not save:
        return crop_wh(im, card_positions[num], 195, 25, 25)
    im = crop_wh(im, card_positions[num], 195, 25, 25)
    im.save(f"screenshots/deck_card_one_{str(time.time()).split('.')[0]}.png")
    return im





def fish_for_deck_cards(im = None):

    print("############------------------fish--------------------##############")

    global deck_cards

    # keep a array of all previous reads to compare and avoid duplicates
    # save unique reads only
    # pyautogui.moveTo(1100, 950, duration=0.01)
    # time.sleep(3) 
    # print("read_D(): "+str(read_D()))

    # reading cards
    # open_cards()
    if im == None:
        im = game_screenshot(save = False)

    dc1 = np.array(deck_card(im, num=1))
    dc2 = np.array(deck_card(im, num=2))
    dc3 = np.array(deck_card(im, num=3))
    dc4 = np.array(deck_card(im, num=4))
    dc5 = np.array(deck_card(im, num=5))

    # compare with previous reads
    if check_if_included(dc1, deck_cards):
        pass
        # print("own value left duplicate read, {filename}, skipping...")
    else:
        deck_cards.append(dc1)
        Image.fromarray(dc1).save(f"fish/deck_cards/1_{str(time.time()).split('.')[0]}.png")
        print("deck card one new read, saved.")

    if check_if_included(dc2, deck_cards):
        pass
        # print("own value left duplicate read, {filename}, skipping...")
    else:
        deck_cards.append(dc2)
        Image.fromarray(dc2).save(f"fish/deck_cards/2_{str(time.time()).split('.')[0]}.png")
        print("deck card two new read, saved.")

    if check_if_included(dc3, deck_cards):
        pass
        # print("own value left duplicate read, {filename}, skipping...")
    else:
        deck_cards.append(dc3)
        Image.fromarray(dc3).save(f"fish/deck_cards/3_{str(time.time()).split('.')[0]}.png")
        print("deck card three new read, saved.")

    if check_if_included(dc4, deck_cards):
        pass
        # print("own value left duplicate read, {filename}, skipping...")
    else:
        deck_cards.append(dc4)
        Image.fromarray(dc4).save(f"fish/deck_cards/4_{str(time.time()).split('.')[0]}.png")
        print("deck card four new read, saved.")

    if check_if_included(dc5, deck_cards):
        pass
        # print("own value left duplicate read, {filename}, skipping...")
    else:
        deck_cards.append(dc5)
        Image.fromarray(dc5).save(f"fish/deck_cards/5_{str(time.time()).split('.')[0]}.png")
        print("deck card five new read, saved.")

from matplotlib import pyplot as plt

def red_deck_cards(im = None):
    if im == None:
        im = game_screenshot()
    dc1 = np.array(deck_card(im, num=1))
    dc2 = np.array(deck_card(im, num=2))
    dc3 = np.array(deck_card(im, num=3))
    dc4 = np.array(deck_card(im, num=4))
    dc5 = np.array(deck_card(im, num=5))
    # plt.imshow(dc1, interpolation='nearest')
    # plt.show()
    # exit()
    result = [ "nn", "nn", "nn", "nn", "nn"]
    i = 0
    global deck_card_filenames
    for current in deck_cards:
        if np.array_equal(dc1, current):
            if deck_card_filenames[i][1]=="_":
                # print(" I HAVE FOUND AN UNDERSCORE IMAGE THING")
                return result
            else:
                result[0]=deck_card_filenames[i][:2]
                break
        elif compare_num(dc1, current):
            if deck_card_filenames[i][1]=="_":
                return result
            else:
                result[0]=deck_card_filenames[i][:2]
                break
        i+=1
    i = 0
    for current in deck_cards:
        if np.array_equal(dc2, current):
            if deck_card_filenames[i][1]=="_":
                return result
            else:
                result[1]=deck_card_filenames[i][:2]
                break
        elif compare_num(dc2, current):
            if deck_card_filenames[i][1]=="_":
                return result
            else:
                result[1]=deck_card_filenames[i][:2]
                break
        i+=1
    i = 0
    for current in deck_cards:
        if np.array_equal(dc3, current):
            if deck_card_filenames[i][1]=="_":
                return result
            else:
                result[2]=deck_card_filenames[i][:2]
                break
        elif compare_num(dc3, current):
            if deck_card_filenames[i][1]=="_":
                return result
            else:
                result[2]=deck_card_filenames[i][:2]
                break
        i+=1
    i = 0
    for current in deck_cards:
        if np.array_equal(dc4, current):
            if deck_card_filenames[i][1]=="_":
                # print("read deck cards result: "+str(result))
                return result
            else:
                result[3]=deck_card_filenames[i][:2]
                break
        elif compare_num(dc4, current):
            if deck_card_filenames[i][1]=="_":
                # print("read deck cards result: "+str(result))
                return result
            else:
                result[3]=deck_card_filenames[i][:2]
                break
        i+=1
    i=0
    for current in deck_cards:
        if np.array_equal(dc5, current):
            if deck_card_filenames[i][1]=="_":
                # print("read deck cards result: "+str(result))
                return result
            else:
                result[4]=deck_card_filenames[i][:2]
                break
        elif compare_num(dc5, current):
            if deck_card_filenames[i][1]=="_":
                # print("read deck cards result: "+str(result))
                return result
            else:
                result[4]=deck_card_filenames[i][:2]
                break
        i+=1
    
    # print("read deck cards result: "+str(result))
    return result
# fish_for_own_cards()


