
from PIL import Image, ImageChops
import pyautogui
import pytesseract
from  fish_for_cards import prepare_fishing_deck_cards, prepare_fishing_own_cards, red_own_cards, game_screenshot, fish_for_own_cards, fish_for_deck_cards, red_deck_cards
from scripts.shavkats_functions import is_red, read_D
import numpy as np
import time
import cv2
from joblib import dump, load
from chatGPT_XGBRegressor import extract_flop_features
import pickle



 # read positions taken and dancing man  and wins or calls #  that is maybe or / and later |||| not now, maybe small model for this later
  # simulating game_screenshot function


def crop_wh(img, left, top, width, height):
    return img.crop((left, top, left + width, top + height))



# from fish_for_cards import fish_for_deck_cards, fish_for_own_cards


filename="As.png"

def comp_imgs(im, im2,  max_ = 60, max_diff = 15, num_max_diff = 5, max_diff_0 = 35, num_max_diff_0 = 35, max_diff_1 = 45, num_max_diff_1 = 35, max_diff_2 = 58, debug = False, debug_2 = False):
    width, height = im.size
    # secs = time.time()
    msrmntrrr = 5 # measurement error
    # im2.show()
    tolerance = 200
    for i in range(2, min(width-1, max_)):
        for j in range(2, min(height-1, max_)):
            if abs(im.getpixel((i,j))[0] - im2.getpixel((i,j))[0])>max_diff or abs(im.getpixel((i,j))[1] - im2.getpixel((i,j))[1])>max_diff or abs(im.getpixel((i,j))[2] - im2.getpixel((i,j))[2])>max_diff:
                if debug: 
                    pass
                    # print("COMPARE IMG HAVING A MID TIME")
                num_max_diff-=1
                if num_max_diff < 1:
                    num_max_diff+=45
                    if debug: print("COMPARE IMG HAVING A HARD TIME")
                    tolerance-=1
                    if tolerance <= 0:
                        return False
                if abs(im.getpixel((i,j))[0] - im2.getpixel((i,j))[0])>max_diff_0 or abs(im.getpixel((i,j))[1] - im2.getpixel((i,j))[1])>max_diff_0 or abs(im.getpixel((i,j))[2] - im2.getpixel((i,j))[2])>max_diff_0:
                    num_max_diff_0-=1
                    if num_max_diff_0 < 1:
                        num_max_diff_0+=25
                        if debug: print("COMPARE IMG HAVING A HARDER TIME")
                        tolerance-=2
                        if tolerance <= 0:
                            return False
                    if abs(im.getpixel((i,j))[0] - im2.getpixel((i,j))[0])>max_diff_1 or abs(im.getpixel((i,j))[1] - im2.getpixel((i,j))[1])>max_diff_1 or abs(im.getpixel((i,j))[2] - im2.getpixel((i,j))[2])>max_diff_1:
                        num_max_diff_1-=1
                        if num_max_diff_1 < 1:
                            num_max_diff_1+=10
                            num_max_diff_0+=25
                            num_max_diff+=35
                            if debug: 
                                print("----------------------------------------------")
                                print("NO!")
                                print("----------------------------------------------")
                            tolerance-=3
                            if tolerance <= 0:
                                return False      
                        if abs(im.getpixel((i,j))[0] - im2.getpixel((i,j))[0])>max_diff_2 or abs(im.getpixel((i,j))[1] - im2.getpixel((i,j))[1])>max_diff_2 or abs(im.getpixel((i,j))[2] - im2.getpixel((i,j))[2])>max_diff_2:
                            if debug: print("NO!")
                            if msrmntrrr < 1:
                                if debug: 
                                    print("----------------------------------------------")
                                    print("NO!!!!!!!!!!!!")
                                    print("----i, j-----")
                                    print(i, j)
                                    print("----------------------------------------------")
                                if debug_2:
                                    secs = time.time()
                                    print("saving files")
                                    im.save(f'temp_compImgs_{secs}_1.png')
                                    im2.save(f'temp_compImgs_{secs}_2.png')
                                    print("----------------------------------------------")
                                tolerance-=8
                                if tolerance <= 0:
                                    return False
                            msrmntrrr -= 1
    if debug:
        print('compare_img_screenshot successful')
    return True



def check_if_check(im2=None, im=None, debug = False): # probably nned to check to not hover or hover to compare images here , doesnt work properly
    
    if im2 == None:
        if im == None:
            im = Image.open('gss_pos2_sitting.png') #should be a screenshot
        im2 = crop_wh(im, 630, 513, 100, 25) #check_button
    
    im3 = Image.open('images/check_button.png') 
    result = comp_imgs(im2, im3, debug=False, debug_2=False)
    if debug:
        print("check_if_check result: "+str(result))
    return result
    # img1 = img1.reshape(100, 200) #  todo read holdemners active and with card and possibly winning, calling, etc. , possibly by model
    # img2 = img2.reshape(100, 200)






def check_holders(im=None, example_img_path_for_card_holder = "card_holders_examples/crop_plaer_1.png", num_plaers = 6): # counterclockwise from me who is holding cards still, me not considered
    
    if num_plaers == 6:
        if im == None:
            im = game_screenshot() # game-screenshot

        im5 = crop_wh(im, 42, 314, 101, 64)
        im4 = crop_wh(im, 68, 67, 101, 64) # position 4, counting counterclockwise from my position as 0
        im3 = crop_wh(im, 374, 7, 101, 64)  # position 4, counting counterclockwise from my position as 0
        im2 = crop_wh(im, 679, 67, 101, 64) # position 2, counting counterclockwise from my position as 0
        im1 = crop_wh(im, 706, 314, 101, 64)# position 1, counting counterclockwise from my position as 0
        # im0 = crop_wh(im, 372, 399, 101, 64)

        # example_0 = Image.open(example_img_path_for_card_holder)


        def check_if_holder(im_n):
            data2 = np.asarray(im_n)
            val_1 = 112.0
            val_2 = float(data2[4,17,0])
            # print("debug check_if_holder")
            # print(val_1)
            # print(val_2)
            data_diff = abs(val_1-val_2)
            if data_diff<10:
                return True
            return False
        
        return [check_if_holder(im1), check_if_holder(im2), check_if_holder(im3), check_if_holder(im4), check_if_holder(im5), False, False, False]

    elif num_plaers == 9:
        pass # todo





def check_if_we_holdin_yet(im): # im = game-screenshot
    # print("checking if we holding cards")
    im0 = crop_wh(im, 372, 399, 101, 64)
    # im0.show()
    data1 = np.asarray(im0)
    # print(data1.shape)
    # print(data1[4,21,0])
    if data1[4,17,0] > 62 and data1[4,17,0]<70:
        if data1[4,18,0] > 140 and data1[4,21,0]<42:
            return False
    return True









def read_game(im = None): # todo: produce input for first model
    holders = [False, False, False, False, False, False, False, False]






def how_much(im = None): 
    pyautogui.moveTo(25, 25)
    if im == None:
        im = game_screenshot() #should be a screenshot
    im2 = crop_wh(im, 640, 508, 74, 22) #check_button
    if check_if_check(im=im, debug=True):
        return 0.0
    im1 = im2
    pixels = im2.load() # create the pixel map
    for i in range(im2.size[0]): # for every pixel:
        for j in range(im2.size[1]):
            # print(pixels[i, j])
            if pixels[i, j][1] >= 180:
                pixels[i, j] = (10, 10, 10, 255)
            else:
                pixels[i,j] = (255, 255, 255, 255)
    # secs = time.time()
    
    raw_data = pytesseract.image_to_string(im2)
    print("raw_data how much: "+raw_data)
    data = raw_data.strip()
    if data == "5SBB":
        print("It must have been 5 BB to call ?!?! please ?!?!")
        return 5.0
    # print(data)
    data = raw_data.split("BB")[0]
    data = data.replace("B", "8")
    data = data.replace("A", "4")
    data = data.replace("S", "5")
    data = data.replace(",", ".")
    data = data.replace("a", "8")
    # im2.save("debug_to_call_"+data+"_"+str(secs).split(".")[0]+".png")
    if data != "":
        try:
            return float(data)
        except Exception as e:
            if data == "O":
                print("it was probably 9 to call ?")
                return 9.0
            else:
                print("raw_data: "+raw_data)
                im1.save("new_check_button_probbaly.png")
                im2.save("new_check_button_probbaly_edited.png")
                raw_data = raw_data.strip()
                if raw_data == "Check":
                    return 0.0
                print("NON STRING FOUND IN how_much , please help")
                exit()
    else:
        print("probably emty button still")
        return 0.0



def check_if_w8_for_blinds(im):
    im1 = crop_wh(im, 525, 499, 102, 30)
    im0 = Image.open("images/w8_for_blinds_checked.png")
    return comp_imgs(im0, im1, debug=True, debug_2=True)



def read_player_info(im = None):
    if im == None:
        im = game_screenshot()
    # im.show()
    im1 = crop_wh(im, 380, 47, 30, 23) # pytesseract, read all 5 values, transfor into 0-1 range and return array of 5
    data = pytesseract.image_to_string(im1)
    position = data.find("%")
    if position == -1:
        # print("no percent-sign found, data:")
        # print(data)
        value_1 = 0
    elif position == 1:
        if data[0]=="0":
            value_1 = 0
        else:
            value_1 = 0.1
    elif position == 2:
        data = data.replace("A", "4")
        data = data.replace("B", "8")
        data = data[:2]
        try:
            value_1 = float(data) / 100.
        except Exception as e:
            print()
            print("read_player_info read something weird:"+str(data))
            print()
            print(e)
            exit()
    elif position == 3:
        value_1 = 1.
    else: 
        print("something went wrong reading value 1 of player info: "+str(data))        
    im1 = crop_wh(im, 438, 47, 30, 23) # pytesseract, read all 5 values, transfor into 0-1 range and return array of 5
    data = pytesseract.image_to_string(im1)
    position = data.find("%")
    if position == -1:
        # print("no percent-sign found, data:")
        # print(data)
        value_2 = 0
    elif position == 1:
        if data[0]=="0":
            value_2 = 0
        else:
            value_2 = 0.1
    elif position == 2:
        data = data.replace("A", "4")
        data = data.replace("B", "8")
        data = data[:2]
        try:
            value_2 = float(data) / 100.
        except Exception as e:
            print()
            print("read_player_info read something weird:"+str(data))
            print()
            print(e)
            exit()
    elif position == 3:
        value_2 = 1.
    else: 
        print("something went wrong reading value 2 of player info: "+str(data))        
    im1 = crop_wh(im, 496, 47, 30, 23) # pytesseract, read all 5 values, transfor into 0-1 range and return array of 5
    data = pytesseract.image_to_string(im1)
    position = data.find("%")
    if position == -1:
        # print("no percent-sign found, data:")
        # print(data)
        value_3 = 0
    elif position == 1:
        if data[0]=="0":
            value_3 = 0
        else:
            value_3 = 0.1
    elif position == 2:
        data = data.replace("A", "4")
        data = data.replace("B", "8")
        data = data[:2]
        try:
            value_3 = float(data) / 100.
        except Exception as e:
            print()
            print("read_player_info read something weird:"+str(data))
            print()
            print(e)
            exit()
    elif position == 3:
        value_3 = 1.
    else: 
        print("something went wrong reading value 3 of player info: "+str(data))
    im1 = crop_wh(im, 554, 47, 30, 23) # pytesseract, read all 5 values, transfor into 0-1 range and return array of 5
    data = pytesseract.image_to_string(im1)
    position = data.find("%")
    if position == -1:
        # print("no percent-sign found, data:")
        # print(data)
        value_4 = 0
    elif position == 1:
        if data[0]=="0":
            value_4 = 0
        else:
            value_4 = 0.1
    elif position == 2:
        data = data.replace("A", "4")
        data = data.replace("B", "8")
        data = data[:2]
        try:
            value_4 = float(data) / 100.
        except Exception as e:
            print()
            print("read_player_info read something weird:"+str(data))
            print()
            print(e)
            exit()
    elif position == 3:
        value_4 = 1.
    else: 
        print("something went wrong reading value 4 of player info: "+str(data))
    try:
        return [ value_1, value_2, value_3, value_4]
    except Exception as e:
        return [ 0, 0, 0, 0]



def read_own_cards(im=None): # may not be ready to read yet, may need to retake screenshot
    if im == None:
        im = game_screenshot()
    result = red_own_cards(im=im)
    if result[0] == "nn" or result[1] == "nn":
        raise Exception("Sorry, no hand cards could be read")
    return result




def read_deck_cards(im = None):
    if im == None:
        im = game_screenshot()
    result = red_deck_cards(im=im)
    if result[0] == "nn" or result[1] == "nn" or result[2] == "nn":
        raise Exception("Sorry, no deck cards could be read")    
    return result
    
    


def read_total_pot_money(im = None):
    if im == None:
        im = game_screenshot()
    im1 = crop_wh(im, 280, 154, 270, 40) # pytesseract, read all 5 values, transfor into 0-1 range and return array of 5
    # im1.show()
    pixels = im1.load() # create the pixel map
    for i in range(im1.size[0]): # for every pixel:
            for j in range(im1.size[1]):
                # print(pixels[i, j])
                if pixels[i, j][1] >= 180:
                    pixels[i, j] = (10, 10, 10, 255)
                else:
                    pixels[i,j] = (255, 255, 255, 255)
    # im1.show()
    raw_data = pytesseract.image_to_string(im1)
    data = raw_data.strip()
    print("total_pot_money raw_data: "+raw_data)
    res = {
        "result": 0.001, 
        "im": im
    }
    if data == "":
        return res

    # position = data.find("Pot")
    if not ":" in data:
        try:
            data = data[:-2]
            data = data.strip()
            data = data.replace("S", "5")
            data = data.replace("A", "4")
            data = data.replace("B", "8")
            data = data.replace(",", ".")
            while True:
                if not data[0].isdigit():
                    data = data[1:]
                else:
                    break
        except:
            print("could not read total pot money, probably nothing there  1, raw_data: "+str(raw_data))
            return res            
    else:
        try:
            data = data[:-2]
            data = data.split(":")[1]
            data = data.strip()
            data = data.replace("S", "5")
            data = data.replace("A", "4")
            data = data.replace("B", "8")
            data = data.replace(",", ".")
            while True:
                if not data[0].isdigit():
                    data = data[1:]
                else:
                    break
        except:
            print("could not read total pot money, probably nothing there 2, raw_data: "+str(raw_data))
            return res
    try:
        # print("read_total_pot_money data: ")
        # print(data)
        res_temp = float(data)
        if res_temp != None and res_temp > 0.1:
            res["result"] = float(data)
        else:
            pass       
    except:
        print("could not read total pot money, returning 0")
        print("data: "+str(data))
        return res
    return res




def read_old_pot_money(im = None):
    if im == None:
        im = game_screenshot()
    im1 = crop_wh(im, 385, 290, 80, 25) # pytesseract, read all 5 values, transfor into 0-1 range and return array of 5 # crop_wh(im, 385, 290, 80, 25) 
    # im1.show()

    pixels = im1.load() # create the pixel map
    for i in range(im1.size[0]): # for every pixel:
            for j in range(im1.size[1]):
                # print(pixels[i, j])
                if pixels[i, j][1] >= 180:
                    pixels[i, j] = (10, 10, 10, 255)
                else:
                    pixels[i,j] = (255, 255, 255, 255)
    # im1.show()
    data = pytesseract.image_to_string(im1)
    # position = data.find("Pot")
    try:
        data = data.strip()
        # data = data[:-2]
        data = data.replace("B", "8")
        if "." in data:
            data.split(".")[1]
            if data.split(".")[1].endswith("8"):
                data = data[:-1]
            if data.split(".")[1].endswith("8"):
                data = data[:-1]
        else:
            if data.endswith("8"):
                data = data[:-1]
            if data.endswith("8"):
                data = data[:-1]            
        data = data.replace("A", "4")
        data = data.replace("S", "5")
        data = data.replace(",", ".")
        while True:
            if not data[0].isdigit():
                data = data[1:]
            else:
                break        
        if data == "":
            print("found nothing in old pot")
            return 0.0
    except:
        # print("could not read old pot money, probably nothing there")
        return 0.1
    try:
        # print("read_old_pot_money data: "+str(data))
        result = float(data)
    except:
        # print("could not read old pot money, returning 0")
        print("data: "+str(data))
        return 0.1
    return result
    




def read_own_money_valid(im = None, should_be = 0.0):
    if im == None:
        im = game_screenshot()
    value = read_own_money(im=im)
    if value < should_be - 2.0 or value > should_be + 2.0:
        return False
    if value == -10:
        return False
    return True





def read_own_money(im = None):
    if im == None:
        im = game_screenshot()
    im1 = crop_wh(im, 378, 495, 95, 25) # pytesseract, read all 5 values, transfor into 0-1 range and return array of 5
    im2 = im1
    # im1.show()
    # exit()
    pixels = im1.load() # create the pixel map
    for i in range(im1.size[0]): # for every pixel:
        for j in range(im1.size[1]):
            # print(pixels[i, j])
            if pixels[i, j][1] >= 135: # 140 initially , trying 130 now
                pixels[i, j] = (10, 10, 10, 255)
            else:
                if pixels[i,j][0] >= 150:
                    pixels[i, j] = (10, 10, 10, 255)
                else:
                    pixels[i,j] = (255, 255, 255, 255)
    # im1.show()
    raw_data = pytesseract.image_to_string(im1)
    # print("own_money raw_data: "+raw_data)
    data = raw_data.strip()
    if data == "All-In":
        return -1.0
    if len(data)<=2:
        print("COULD NOT READ OWN MONEY 24 - data :"+str(data))
        im2.save(f"sus_own_money_reading{time.time()}.png")
        return -10
    if len(data)<=3:
        # print("!!!!!!!!!!!!!!!!   SUS READ OWN MONEY 24 - data :"+str(data))
        pass
    else:
        data = data[:-2]
    data = data.strip()
    data = data.replace("BB", "")
    data = data.replace("8B", "")
    data = data.replace("B8", "")
    data = data.replace(" 88", "")
    data = data.replace("A", "4")
    data = data.replace("S", "5")
    data = data.replace("?", "2")
    data = data.replace("G", "6")
    data = data.strip()
    if len(data)<1:
        print("COULD NOT READ OWN MONEY 28 - raw_data :"+str(raw_data))
        exit()
    i = 0
    while True:
        if i > 5:
            print("! could not read own money - raw_data 123: "+str(raw_data))
            return -10            
        try:
            if not data[0].isdigit():
                data = data[1:]
            else:
                break
            i+=1
        except:
            print("! could not read own money 56 - raw_data: "+str(raw_data))
            return -10
    # print("read own money data: "+data)

    #todo: check if value maybe sus, re-read if so ... if still sus, save image maybe ...
    
    try:
        data = float(data)
        if data > 100.0:
            print("read_own_money data: "+str(data))
            print("maybe sus value read, ...")
            data = str(data)
            data_0 = data.split(".")[0]
            if data_0.endswith("7"):
                data_0 = data_0[:-1]
            data = data_0 + "." + data.split(".")[1]
            print("removed that seven from data: "+str(data))
            return float(data)
        return data
    except Exception as e:
        if " " in data:
            data = data.split(" ")[1]
        else:
            # print("SOMETHING WENT WRONG READING OWN MONEY 99 ; data : "+str(data))
            # print(e)
            while True: 
                try:
                    if not data[-1].isdigit():
                        data = data[:-1]
                    else:
                        break
                except:
                    print("! could not read own money 69 - raw_data: "+str(raw_data))
                    return -10                    
            try:
                data = float(data)
                if data > 100.0:
                    print("read_own_money data: "+str(data))
                    print("maybe sus value read, ...")
                    data = str(data)
                    data_0 = data.split(".")[0]
                    if data_0.endswith("7"):
                        data_0 = data_0[:-1]
                    data = data_0 + "." + data.split(".")[1]
                    print("removed that seven from data: "+str(data))
                    return float(data)
                return data
            except Exception as e:
                print("reading own money failed")
                print(e)
                exit            

        try:
            return float(data)
        except Exception as e:
            print("reading own money failed")
            print(e)
            exit




        

smol_watsgoingon_model = None
import keras


def load_smol_watsgoingon_model():
    global smol_watsgoingon_model
    if smol_watsgoingon_model == None:
        smol_watsgoingon_model = keras.saving.load_model("model.keras", custom_objects=None, compile=True, safe_mode=True)
        return True
    else:
        print("model already loaded")
        return False
    




def general_whats_going_on_model(im = None):
    if im == None:
        im = game_screenshot()
    nim = im.convert("RGB")
    nim = np.array(nim)
    nim = cv2.resize(nim, dsize=(150, 150))
    # print(im.shape)
    # print(str(im))
    # exit
    model_output = smol_watsgoingon_model.predict(np.array([nim]))[0]
    # print("model_output.argmax(): "+str(model_output.argmax()))
    arg_max = model_output.argmax()
    prob = model_output[arg_max]
    class_names = ["preflop", "flop", "river", "turn", "no_decision_to_be_made", "connectivity_issues"]
    result = class_names[arg_max]
    model_output[arg_max] = 0
    sec_max = model_output.argmax()
    sec_prob = model_output[sec_max]
    if (prob/(sec_prob+0.01))<=5.0:
        # print(str(model_output))
        print(f"saving example (general_whats_going_on_model : {result}) confidence-score: "+str(prob/(sec_prob+0.01)))
        secs = time.time()
        second = class_names[sec_max]
        im.save(f"shmol_model_not_sure/if_{result[:7]}_or_{second[:7]}_{str(prob/(sec_prob+0.001))}.png")
    return result







flop_equity_model = None

def load_flop_equity_model():
    global flop_equity_model
    if flop_equity_model == None:
        flop_equity_model = load("flop_equity_xgb_1.joblib")
        return True
    else:
        print("model already loaded")
        return False    




def flop_equity_model_predict(features): 
    return flop_equity_model.predict([features])[0]







def handle_all_in(im = None):
    if im == None:
        im = game_screenshot()
    # print(im.size)
    pixels = im.load() # create the pixel map
    if pixels[760, 490][1] >= 80:
        print("\nrun three times clicked (need to switch to two I think, they dont play three around here ...)")
        pyautogui.click(760, 590)
        return False
    else:
        if pixels[340, 460][1]> 100 and pixels[342, 460][0] > 200:
            print("\nimma try clicking ok here")
            time.sleep(1)
            secs = time.time()
            im.save(f"shmol_model_not_sure/all_in/connectivity_issues_{str(secs).split(".")[0]}.png")
            pyautogui.click(340, 560)
            return True
        else:
            if pixels[576, 320][1] > 250:
                pyautogui.moveTo(576, 420, duration=0.3)
                time.sleep(0.5)
                pyautogui.click(576, 420) # hehe :D
                print("\nclick open fourth ...")
                return False
            else:
                # im0 = crop_wh(im, 320, 420, 100, 100)
                # im0.show()
                pix_0 = pixels[320, 420]
                # print(pix_0)
                if pix_0[0]<32 and pix_0[1]>95:
                    print("getting more chips")
                    pyautogui.click(320, 420)
                    return True
                else:
                    return False
                # pix_1 = pixels[573, 320]
                # print(pix_1)
                # pix_2 = pixels[574, 320]
                # print(pix_2)
                # pix_3 = pixels[575, 320]
                # print(pix_3)
                # pix_4 = pixels[576, 320]
                # print(pix_4)
                # pix_5 = pixels[577, 320]
                # print(pix_5)


    # exit()
    # todo: 
        # check pixels for run it three times or open last card stuff ... idk the game mechanics like that exactly yet
        # check if buy_in ...












flop_model = None
flop_model_scaler = None

def load_flop_model():
    import pickle
    global flop_model_scaler
    with open("flop_model_scaler", "rb") as fp:   # Unpickling
        flop_model_scaler = pickle.load(fp)  
    global flop_model
    if flop_model == None:
        flop_model = load("flop_xgb.joblib")
        return True
    else:
        print("flop model already loaded")
        return False

def flop_model_predict_multiple(input_array):
    new_data_scaled = flop_model_scaler.transform(input_array)
    predictions = flop_model.predict(new_data_scaled)
    return predictions














river_model = None
river_model_scaler = None

def load_river_model():
    import pickle
    global river_model_scaler
    with open("river_model_scaler", "rb") as fp:   # Unpickling
        river_model_scaler = pickle.load(fp)  
    global river_model
    if river_model == None:
        river_model = load("river_xgb.joblib")
        return True
    else:
        print("river model already loaded")
        return False

def river_model_predict_multiple(input_array):
    new_data_scaled = river_model_scaler.transform(input_array)
    predictions = river_model.predict(new_data_scaled)
    return predictions


    

turn_model = None
turn_model_scaler = None

def load_turn_model():
    import pickle
    global turn_model_scaler
    with open("turn_model_scaler", "rb") as fp:   # Unpickling
        turn_model_scaler = pickle.load(fp)  
    global turn_model
    if turn_model == None:
        turn_model = load("turn_xgb.joblib")
        return True
    else:
        print("turn model already loaded")
        return False


def turn_model_predict_multiple(input_array):
    new_data_scaled = turn_model_scaler.transform(input_array)
    predictions = turn_model.predict(new_data_scaled)
    return predictions







def simulate_gss(im=None):
    if im == None:
        im = Image.open('shmol_new_data/connectivity_issues_1766017203.png') #should be a screenshot

    handle_all_in(im=im)



    # print(general_whats_going_on_model(im))

    return False

 
    could_be_red_pix = im.getpixel((530, 500)) # there should be a red button here, when it is our turn 
    print("pix (where red button might be): "+ str(could_be_red_pix))

    # d_position = read_D(im)
        


    if is_red(could_be_red_pix):
        # fish_for_own_cards(im = im)
        # fish_for_deck_cards(im = im)

        decision = "None_yet"


        print("self.decision: "+str(self.decision))
        # print("self.d_position: "+str(self.d_position))

        dec = self.decision
        if dec == "None_yet":
            #acting (ToDo) check if all values have been read, read everything necessary (number on the middle button) and make decision
            self.decision = def_dec
            dec = self.decision
        if dec == "fold":
            # print("fold was clicked")
            pyautogui.click(540, 610)
            self.decision = "fold"
        if dec.startswith("call"):
            # print("call was clicked")
            if len(dec)>4:
                if dec[4] == "0":
                    self.decision = "call"
                else:
                    self.decision = "call"+str(int(dec[4])-1)
            else:
                self.decision = "fold"
            pyautogui.click(670, 610)
        elif dec.startswith("r"):
            print("raise1 was clicked")
            pyautogui.click(800, 610)
            self.decision = "call7"
        elif dec.startswith("2"):
            print("raise2 was clicked")
            # pyautogui.click(659, 557) # works
            # pyautogui.click(800, 610)
            self.decision = "call8"
    else:
        pass
        # print("no red buttons ...")





import glob

if __name__ == "__main__":
    # prepare_fishing_own_cards()
    # prepare_fishing_deck_cards()
    # load_smol_watsgoingon_model()
    # path = glob.glob("datasets/shmol_watgoinon/**/*.png", recursive=True)
    # for pth in path :
    #     if pth.endswith(".png"):
    #         im = Image.open(pth)
    #         # im = Image.open("gsss/game_screenshot1764690404.png")
    #         if simulate_gss(im=im):
    #             print("found one ! "+str(pth))
    #         time.sleep(0.1)
    # print(path)
    simulate_gss()

    # load_flop_equity_model()
    # print("start")
    # print(flop_equity_model_predict(["As", "Ac"], ["Kd", "Qc", "Tc"]))
    # print("stop")

    