






import time

import numpy as np

from fish_for_cards import game_screenshot
from small_shwatsgoingon import check_if_included, compare_num, crop_wh
from PIL import Image









import os
pot_digits = []
pot_digits_filenames = []
def prepare_pot_digits():
    global pot_digits
    global pot_digits_filenames
    directory = os.fsencode("tesseract_training/digits")
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if filename.endswith(".png"): 
            im = Image.open(f"tesseract_training/digits/{filename}")
            im_array = np.array(im)
            pot_digits.append(im_array)
            pot_digits_filenames.append(filename)
        else:
            print(f"found some non png file in tesseract_training/digits, {filename}, skipping...")


prepare_pot_digits()






def read_total_pot_money_manually(im = None, im2 = None):

    if im2 == None:
        if im == None:
            im = game_screenshot()
        im1 = crop_wh(im, 280, 154, 290, 40) # pytesseract, read all 5 values, transfor into 0-1 range and return array of 5
        # im1.show()
        pixels = im1.load()
        for i_i in range(im1.size[0]): # width
            if pixels[i_i, 16][1] >= 160:
                # print("pixel i "+str(i_i))
                break    
        i_1 = i_i

        if i_i > 100:
            print("i over 100")
            im2 = crop_wh(im1, i_i+67, 16, 60, 10) 
            im2.save(f"tesseract_training/raw_data/over_100_{str(time.time())[:12]}.png")    
            return (i_1, 0.001)    

        pixels = im2.load()
        for i in range(im2.size[0]): # width
            for j in range(im2.size[1]): # height
                if pixels[i, j][1] >= 160:
                    pixels[i, j] = (10, 10, 10, 255)
                else:
                    pixels[i,j] = (255, 255, 255, 255)    
        
                    
    
    
    im2_1 = crop_wh(im2, 2, 0, 6, 10) # first digit
    global pot_digits 
  
    dig1 = np.array(im2_1)
    if not check_if_included(dig1, pot_digits):
        im2_1.save(f"tesseract_training/digits/no_read_{str(time.time())[:12]}.png")    
        return (i_1, 0.001)

    result = ""
    i = 0
    for current in pot_digits:
        if np.array_equal(dig1, current):    # I wonder if the one up here works, then we can remove the other maybe ?             
            if pot_digits_filenames[i][0].isdigit() == False:
                    return (i_1, 0.001)  
            result += pot_digits_filenames[i][0]
            break
        elif compare_num(dig1, current, debug=False):                
            if pot_digits_filenames[i][0].isdigit() == False:
                    return (i_1, 0.001)  
            result += pot_digits_filenames[i][0]
            break
        i+=1 
    
    if result == "m" or result == "":
        print("could not read total pot money first digit")
        if result == "":
            im2.save(f"tesseract_training/digits/no_read_{str(time.time())[:12]}.png")    
        return (i_1, 0.001)
    

    im3 = crop_wh(im1, i_i+77, 16, 6, 10) # second digit
    pixels = im3.load() # create the pixel map
    for i in range(im3.size[0]): # width
        for j in range(im3.size[1]): # height
            if pixels[i, j][1] >= 160:
                pixels[i, j] = (10, 10, 10, 255)
            else:
                pixels[i,j] = (255, 255, 255, 255)

    # check for dot or BB

    if pixels[2, 8][1] > 160 and pixels[1, 8][1] > 160 and pixels[0, 8][1] > 160 and pixels[0, 9][1] < 160 and pixels[1, 9][1] < 160: # dot found
        result += "."
        # print("we have a dot 1")
        im4 = crop_wh(im1, i_i+81, 16, 6, 10) # digit after dot
        pixels = im4.load() # create the pixel map
        for i in range(im4.size[0]): # width
            for j in range(im4.size[1]): # height
                if pixels[i, j][1] >= 160:
                    pixels[i, j] = (10, 10, 10, 255)
                else:
                    pixels[i,j] = (255, 255, 255, 255)
        dig2 = np.array(im4)
        if not check_if_included(dig2, pot_digits):
            im4.save(f"tesseract_training/digits/after_dot_no_read_{str(time.time())[:12]}.png")    
            return (i_1, 0.001)
        i = 0
        for current in pot_digits:
            if np.array_equal(dig2, current):
                result += pot_digits_filenames[i][0]
                break
            elif compare_num(dig2, current, debug=False):
                result += pot_digits_filenames[i][0]
                break

            i+=1
        # print("read_total_pot_money result (after dot 1): "+str(result))
        return (i_1, float(result))
    
    # no dot found yet
    dig1 = np.array(im3)
    if not check_if_included(dig1, pot_digits):
        im3.save(f"tesseract_training/digits/second_digit_no_read_{str(time.time())[:12]}.png")    
        return (i_1, 0.001)
    
    i = 0
    for current in pot_digits:
        if np.array_equal(dig1, current):
            if  pot_digits_filenames[i][0] != "B":
                result += pot_digits_filenames[i][0]
                break
            else:
                return (i_1, float(result))         
        elif compare_num(dig1, current, debug=False):
            if  pot_digits_filenames[i][0] != "B":
                result += pot_digits_filenames[i][0]
                break
            else:
                return (i_1, float(result))
        i+=1   



    im3 = crop_wh(im1, i_i+85, 16, 6, 10) # third digit
    pixels = im3.load() # create the pixel map
    for i in range(im3.size[0]): # width
        for j in range(im3.size[1]): # height
            if pixels[i, j][1] >= 160:
                pixels[i, j] = (10, 10, 10, 255)
            else:
                pixels[i,j] = (255, 255, 255, 255)

    # check for dot or BB

    if pixels[2, 8][1] > 160 and pixels[1, 8][1] > 160 and pixels[0, 8][1] > 160 and pixels[0, 9][1] < 160 and pixels[1, 9][1] < 160: # dot found
        result += "."
        # print("we have a dot 3rd digit")
        im4 = crop_wh(im1, i_i+89, 16, 6, 10) # digit after dot
        pixels = im4.load() # create the pixel map
        for i in range(im4.size[0]): # width
            for j in range(im4.size[1]): # height
                if pixels[i, j][1] >= 160:
                    pixels[i, j] = (10, 10, 10, 255)
                else:
                    pixels[i,j] = (255, 255, 255, 255)
        # im4.save("debug_third_digit_after_dot.png")
        dig2 = np.array(im4)
        if not check_if_included(dig2, pot_digits):
            im4.save(f"tesseract_training/digits/after_dot_no_read_{str(time.time())[:12]}.png")    
            return (i_1, 0.001)
        i = 0
        for current in pot_digits:
            if np.array_equal(dig2, current):
                result += pot_digits_filenames[i][0]
                break
            elif compare_num(dig2, current, debug=False):
                result += pot_digits_filenames[i][0]
                break
            i+=1
        # print("read_total_pot_money result (after dot 2): "+str(result))
        return (i_1, float(result))
    

    dig1 = np.array(im3)
    if not check_if_included(dig1, pot_digits):
        im3.save(f"tesseract_training/digits/third_digit_no_read_{str(time.time())[:12]}.png")    
        return (i_1, 0.001)
    
    i = 0
    for current in pot_digits:
        if np.array_equal(dig1, current):
            if  pot_digits_filenames[i][0] != "B":
                result += pot_digits_filenames[i][0]
                break
            else:
                # print("read_total_pot_money result 2: "+str(result))
                return (i_1, float(result))            
        elif compare_num(dig1, current, debug=False):
            if  pot_digits_filenames[i][0] != "B":
                result += pot_digits_filenames[i][0]
                break
            else:
                # print("read_total_pot_money result 2: "+str(result))
                return (i_1, float(result))
        i+=1   






    im3 = crop_wh(im1, i_i+93, 16, 6, 10) # fourth digit
    pixels = im3.load() # create the pixel map
    for i in range(im3.size[0]): # width
        for j in range(im3.size[1]): # height
            if pixels[i, j][1] >= 160:
                pixels[i, j] = (10, 10, 10, 255)
            else:
                pixels[i,j] = (255, 255, 255, 255)

    # check for dot or BB

    if pixels[2, 8][1] > 160 and pixels[1, 8][1] > 160 and pixels[0, 8][1] > 160 and pixels[0, 9][1] < 160: # dot found
        result += "."
        # print("we have a dot")
        im4 = crop_wh(im1, i_i+97, 16, 6, 10) # digit after dot
        pixels = im4.load() # create the pixel map
        for i in range(im4.size[0]): # width
            for j in range(im4.size[1]): # height
                if pixels[i, j][1] >= 160:
                    pixels[i, j] = (10, 10, 10, 255)
                else:
                    pixels[i,j] = (255, 255, 255, 255)
        dig2 = np.array(im4)
        if not check_if_included(dig2, pot_digits):
            im4.save(f"tesseract_training/digits/after_dot_no_read_{str(time.time())[:12]}.png")    
            return (i_1, 0.001)
        i = 0
        for current in pot_digits:
            if np.array_equal(dig2, current):
                result += pot_digits_filenames[i][0]
                break
            elif compare_num(dig2, current, debug=False):
                result += pot_digits_filenames[i][0]
                break
            i+=1
        # print("read_total_pot_money result (after dot 3): "+str(result))
        return (i_1, float(result))
    
    dig1 = np.array(im3)
    if not check_if_included(dig1, pot_digits):
        im3.save(f"tesseract_training/digits/fourth_digit_no_read_{str(time.time())[:12]}.png")    
        return (i_1, 0.001)
    
    i = 0
    for current in pot_digits:
        if np.array_equal(dig1, current):
            if  pot_digits_filenames[i][0] != "B":
                result += pot_digits_filenames[i][0]
                break
            else:
                # print("read_total_pot_money result 3: "+str(result))
                return (i_1, float(result))            
        elif compare_num(dig1, current, debug=False):
            if  pot_digits_filenames[i][0] != "B":
                result += pot_digits_filenames[i][0]
                break
            else:
                # print("read_total_pot_money result 3: "+str(result))
                return (i_1, float(result))
        i+=1   


      
    

    print("read_total_pot_money result: "+str(result))

    
    return (i_1, float(result)) # for now, only training images are being saved
    # print("\n read_total_pot_money debug 1 \n")






im2 = Image.open("n_2.0_0.001_ct.png")

im2_1 = crop_wh(im2, 2, 4, 6, 10) # first digit

# im2_1.show()


dig1 = np.array(im2_1)
im2_1.save(f"first_digit_{str(time.time())[:12]}.png") 


result = ""
i = 0
for current in pot_digits:
    if np.array_equal(dig1, current):    # I wonder if the one up here works, then we can remove the other maybe ?             
        if pot_digits_filenames[i][0].isdigit() == False:
                print("could not read first digit") 
        result += pot_digits_filenames[i][0]
        break
    elif compare_num(dig1, current, debug=False):                
        if pot_digits_filenames[i][0].isdigit() == False:
                print("could not read first digit 2")
        result += pot_digits_filenames[i][0]
        break
    i+=1 

if result == "m" or result == "":
    print("could not read total pot money first digit")
    if result == "":
        im2_1.save(f"tesseract_training/digits/no_read_{str(time.time())[:12]}.png")    

print(result)
