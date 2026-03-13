import os
import pyautogui
import time
import numpy as np
import cv2
import random
# from matplotlib.pyplot import imshow
# import matplotlib
# matplotlib.use('agg')
from secrets1.secret import password, email
# import pyperclip
import glob
from PIL import Image
from playsound3 import playsound



pull_to = [10, 45]
def_clint = [12, 46] #69, 70
l_info_read = False



def click(x, y, im = None, debug = False, calling_function = None): # done - needs integration and testing
    print("click , debug: "+str(debug))
    if debug:
        # make screenshot, mark where we clicking, save image
        if im == None:
            im = game_screenshot()
        point_on_image = (x, y-95)
        pixels = im.load()
        try:
            pixels[point_on_image[0]+1,point_on_image[1]] = (255, 0, 0, 255)
            pixels[point_on_image[0],point_on_image[1]+1] = (255, 0, 0, 255)
            pixels[point_on_image[0]-1,point_on_image[1]] = (255, 0, 0, 255)
            pixels[point_on_image[0],point_on_image[1]-1] = (255, 0, 0, 255)
            try:
                pixels[point_on_image[0]+2,point_on_image[1]] = (255, 0, 0, 255)
                pixels[point_on_image[0]-2,point_on_image[1]] = (255, 0, 0, 255)
                pixels[point_on_image[0],point_on_image[1]-2] = (255, 0, 0, 255)
                pixels[point_on_image[0],point_on_image[1]+2] = (255, 0, 0, 255)
                try:
                    pixels[point_on_image[0]+3,point_on_image[1]] = (255, 0, 0, 255)
                    pixels[point_on_image[0]-3,point_on_image[1]] = (255, 0, 0, 255)
                    pixels[point_on_image[0],point_on_image[1]+3] = (255, 0, 0, 255)
                    pixels[point_on_image[0],point_on_image[1]-3] = (255, 0, 0, 255)
                    pixels[point_on_image[0]+4,point_on_image[1]] = (255, 0, 0, 255)
                    pixels[point_on_image[0]-4,point_on_image[1]] = (255, 0, 0, 255)
                    pixels[point_on_image[0],point_on_image[1]+4] = (255, 0, 0, 255)
                    pixels[point_on_image[0],point_on_image[1]-4] = (255, 0, 0, 255)
                except Exception as e:
                    print("error in click: "+str(e))
                    if calling_function == None:
                        im.save(f"clicking_images/click_failed_{str(pixels[760, 490][0])}_{str(pixels[760, 490][1])}_{str(pixels[760, 490][2])}_{str(time.time())[:10]}.png")
                    else:
                        im.save(f"clicking_images/click_failed_{calling_function}_{str(pixels[760, 490][0])}_{str(pixels[760, 490][1])}_{str(pixels[760, 490][2])}_{str(time.time())[:10]}.png")                
            except Exception as e:
                print("error in click: "+str(e))
                if calling_function == None:
                    im.save(f"clicking_images/click_failed_{str(pixels[760, 490][0])}_{str(pixels[760, 490][1])}_{str(pixels[760, 490][2])}_{str(time.time())[:10]}.png")
                else:
                    im.save(f"clicking_images/click_failed_{calling_function}_{str(pixels[760, 490][0])}_{str(pixels[760, 490][1])}_{str(pixels[760, 490][2])}_{str(time.time())[:10]}.png")
                    
        except Exception as e:
            print("error in click: "+str(e))
            if calling_function == None:
                im.save(f"clicking_images/click_failed_{str(pixels[760, 490][0])}_{str(pixels[760, 490][1])}_{str(pixels[760, 490][2])}_{str(time.time())[:10]}.png")
            else:
                im.save(f"clicking_images/click_failed_{calling_function}_{str(pixels[760, 490][0])}_{str(pixels[760, 490][1])}_{str(pixels[760, 490][2])}_{str(time.time())[:10]}.png")
        if calling_function == None:
            im.save(f"clicking_images/click_{str(pixels[760, 490][0])}_{str(pixels[760, 490][1])}_{str(pixels[760, 490][2])}_{str(time.time())[:10]}.png")
        else:
            im.save(f"clicking_images/click_{calling_function}_{str(pixels[760, 490][0])}_{str(pixels[760, 490][1])}_{str(pixels[760, 490][2])}_{str(time.time())[:10]}.png")

        pyautogui.click(x, y)
    else:
        pyautogui.click(x, y)




def remove_debug_imgs():
    removing_files = glob.glob('temp_*.png')
    # removing_files_0 = glob.glob('temp_*.png')
    for i in removing_files:
        os.remove(i)





def comp_imgs(im, im2,  max_ = 60, max_diff = 5, num_max_diff = 5, max_diff_0 = 30, num_max_diff_0 = 35, max_diff_1 = 45, num_max_diff_1 = 35, max_diff_2 = 58, debug = False, debug_2 = False):
    width, height = im.size
    # secs = time.time()
    msrmntrrr = 5 # measurement error
    # im2.show()
    for i in range(1, min(width-1, max_)):
        for j in range(1, min(height-1, max_)):
            if abs(im.getpixel((i,j))[0] - im2.getpixel((i,j))[0])>max_diff or abs(im.getpixel((i,j))[1] - im2.getpixel((i,j))[1])>max_diff or abs(im.getpixel((i,j))[2] - im2.getpixel((i,j))[2])>max_diff:
                if debug: 
                    pass
                    # print("COMPARE IMG HAVING A MID TIME")
                num_max_diff-=1
                if num_max_diff < 1:
                    num_max_diff+=5
                    if debug: print("COMPARE IMG HAVING A HARD TIME")
                    return False
                if abs(im.getpixel((i,j))[0] - im2.getpixel((i,j))[0])>max_diff_0 or abs(im.getpixel((i,j))[1] - im2.getpixel((i,j))[1])>max_diff_0 or abs(im.getpixel((i,j))[2] - im2.getpixel((i,j))[2])>max_diff_0:
                    num_max_diff_0-=1
                    if num_max_diff_0 < 1:
                        num_max_diff_0+=5000
                        if debug: print("COMPARE IMG HAVING A HARDER TIME")
                        return False
                    if abs(im.getpixel((i,j))[0] - im2.getpixel((i,j))[0])>max_diff_1 or abs(im.getpixel((i,j))[1] - im2.getpixel((i,j))[1])>max_diff_1 or abs(im.getpixel((i,j))[2] - im2.getpixel((i,j))[2])>max_diff_1:
                        num_max_diff_1-=1
                        if num_max_diff_1 < 1:
                            if debug: 
                                print("----------------------------------------------")
                                print("NO!")
                                print("num_max_diff: "+str(num_max_diff))
                                print("num_max_diff_0: "+str(num_max_diff_0))
                                print("num_max_diff_1: "+str(num_max_diff_1))
                                print("---------")
                                print(i, j)
                                print("----------------------------------------------")
                            if debug_2:
                                secs = time.time()
                                print("saving files")
                                im.save(f'temp_{secs}_1.png')
                                im2.save(f'temp_{secs}_2.png')
                                print("----------------------------------------------")
                            return False
                        if abs(im.getpixel((i,j))[0] - im2.getpixel((i,j))[0])>max_diff_2 or abs(im.getpixel((i,j))[1] - im2.getpixel((i,j))[1])>max_diff_2 or abs(im.getpixel((i,j))[2] - im2.getpixel((i,j))[2])>max_diff_2:
                            if debug: print("NO!")
                            if msrmntrrr < 1:
                                if debug: 
                                    print("----------------------------------------------")
                                    print("NO!")
                                    print("num_max_diff: "+str(num_max_diff))
                                    print("num_max_diff_0: "+str(num_max_diff_0))
                                    print("num_max_diff_1: "+str(num_max_diff_1))
                                    print("---------")
                                    print(i, j)
                                    print("----------------------------------------------")
                                if debug_2:
                                    secs = time.time()
                                    print("saving files")
                                    im.save(f'temp_{secs}_1.png')
                                    im2.save(f'temp_{secs}_2.png')
                                    print("----------------------------------------------")
                                return False
                            msrmntrrr -= 1
    if debug:
        print('compare_img_screenshot successful')
    return True












# up to am max of 50
def compare_img_screenshot(im,pos, max_ = 50, max_diff = 30, num_max_diff = 30, max_diff_0 = 40, num_max_diff_0 = 35, max_diff_1 = 45, num_max_diff_1 = 35, max_diff_2 = 58, debug = False, debug_2 = False):
    width, height = im.size
    # secs = time.time()
    im2 = pyautogui.screenshot(region=(pos[0], pos[1], width, height))
    msrmntrrr = 5
    # im2.show()
    for i in range(0, min(width-1, max_)):
        for j in range(0, min(height-1, max_)):
            if abs(im.getpixel((i,j))[0] - im2.getpixel((i,j))[0])>max_diff or abs(im.getpixel((i,j))[1] - im2.getpixel((i,j))[1])>max_diff or abs(im.getpixel((i,j))[2] - im2.getpixel((i,j))[2])>max_diff:
                # if debug: print("COMPARE IMG HAVING A MID TIME")
                num_max_diff-=1
                if num_max_diff < 1:
                    num_max_diff+=5
                    if debug: print("COMPARE IMG HAVING A mid TIME")
                if abs(im.getpixel((i,j))[0] - im2.getpixel((i,j))[0])>max_diff_0 or abs(im.getpixel((i,j))[1] - im2.getpixel((i,j))[1])>max_diff_0 or abs(im.getpixel((i,j))[2] - im2.getpixel((i,j))[2])>max_diff_0:
                    num_max_diff_0-=1
                    if num_max_diff_0 < 1:
                        num_max_diff_0 += 5
                        if debug: print("COMPARE IMG HAVING A hard TIME")
                    if abs(im.getpixel((i,j))[0] - im2.getpixel((i,j))[0])>max_diff_1 or abs(im.getpixel((i,j))[1] - im2.getpixel((i,j))[1])>max_diff_1 or abs(im.getpixel((i,j))[2] - im2.getpixel((i,j))[2])>max_diff_1:
                        num_max_diff_1-=1
                        if num_max_diff_1 < 1:
                            if debug: 
                                print("----------------------------------------------")
                                print("NO!")
                                print("num_max_diff: "+str(num_max_diff))
                                print("num_max_diff_0: "+str(num_max_diff_0))
                                print("num_max_diff_1: "+str(num_max_diff_1))
                                print("---------")
                                print(i, j)
                                print("----------------------------------------------")
                            if debug_2:
                                secs = time.time()
                                print("saving files")
                                im.save(f'temp_{secs}_1.png')
                                im2.save(f'temp_{secs}_2.png')
                                print("----------------------------------------------")
                            return False
                        if abs(im.getpixel((i,j))[0] - im2.getpixel((i,j))[0])>max_diff_2 or abs(im.getpixel((i,j))[1] - im2.getpixel((i,j))[1])>max_diff_2 or abs(im.getpixel((i,j))[2] - im2.getpixel((i,j))[2])>max_diff_2:
                            if debug: print("NO!")
                            if msrmntrrr < 1:
                                if debug: 
                                    print("----------------------------------------------")
                                    print("NO!")
                                    print("num_max_diff: "+str(num_max_diff))
                                    print("num_max_diff_0: "+str(num_max_diff_0))
                                    print("num_max_diff_1: "+str(num_max_diff_1))
                                    print("---------")
                                    print(i, j)
                                    print("----------------------------------------------")
                                if debug_2:
                                    secs = time.time()
                                    print("saving files")
                                    im.save(f'temp_{secs}_1.png')
                                    im2.save(f'temp_{secs}_2.png')
                                    print("----------------------------------------------")
                                return False
                            msrmntrrr -= 1
    if debug:
        print('compare_img_screenshot successful')
    return True





'''
Searchs for an image on the screen

input :

image : path to the image file (see opencv imread for supported types)
precision : the higher, the lesser tolerant and fewer false positives are found default is 0.8
im : a PIL image, usefull if you intend to search the same unchanging region for several elements

returns :
the top left corner coordinates of the element if found as an array [x,y] or [-1,-1] if not

'''
def imagesearch(image_path, precision=0.9, debug = False, debug_2 = False, calling_function = None):
    im = pyautogui.screenshot(region=(0, 0, 1400, 1000))
    secs = time.time()
    # im2.save('temp.png')
    # im.save(f'testarea7_{secs}.png') # useful for debugging purposes, this will save the captured region as "testarea.png"
    img_rgb = np.array(im)
    # img2_rgb = np.array(im2)
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2GRAY)
    template = cv2.imread(image_path, 1)
    template = cv2.cvtColor(template, cv2.COLOR_BGR2RGB)
    # if debug:
    #     img4_rgb = np.array(im)
    #     print("imagesearch - from : "+str(calling_function))
    #     print('screenshot')
    #     plt.imshow(img4_rgb, interpolation='nearest')
    #     plt.show()
    #     print('looking for: ')
    #     plt.imshow(template, interpolation='nearest')
    #     plt.show()
    try:
        coordinates = pyautogui.locate(template, img_rgb, confidence=0.9)
        if debug:
            print('pyautogui located '+image_path+' - proceeding anyways with cv.matchTemplate')
            print('coordinates found by pyautogui: '+str(coordinates))
        else:
            return [coordinates[0].__int__(), coordinates[1].__int__()]
    except:
        if debug:
            print(f'{image_path} not found at first glance')
    # plt.imshow(img2_rgb, interpolation='nearest')
    # plt.show()
    # plt.imshow(template, interpolation='nearest')
    # plt.show()
    template_gray = cv2.cvtColor(template, cv2.COLOR_RGB2GRAY)
    # img_rgb.shape[::-1]
    res = cv2.matchTemplate(img_gray, template_gray, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    if max_val < precision:
        if debug:
            print('not found')
        return [-1, -1]
    if debug:
        im2 = pyautogui.screenshot(region=(max_loc[0], max_loc[1], template_gray.shape[1],template_gray.shape[0]))
        print("found "+image_path+" - from : "+str(calling_function))
        print('found at '+str(max_loc) +" - at confidence: "+str(max_val))
        # if max_val > 0.999:
        #     return [max_loc[0], max_loc[1]]
        if debug_2:
            # print(f'saving this ({image_path}) to memory: ')
            # img2_rgb = np.array(im2)
            # plt.imshow(img2_rgb, interpolation='nearest')
            # plt.show()
            # print('instead of this: ')
            # plt.imshow(template, interpolation='nearest')
            # plt.show()
            im2.save(image_path[:-4]+"_new.png")
    return [max_loc[0], max_loc[1]]


def game_screenshot(save = False):
    if not save:
        im = screenshot_area(point = (0, 95), size = [830, 540], file_name=None)
        # time.sleep(.2)
    else:
        secs = time.time()
        im = screenshot_area(point = (0, 95), size = [830, 540], file_name=f"screenshots/game_screenshot{str(secs).split(".")[0]}.png")
        # time.sleep(.2)
    return im












def reset_client_window(debug = False):
    clint_pos = imagesearch('images/GGPoker_new.png', precision=0.85, debug=debug, calling_function= 'reset_client_window')
    if clint_pos != [-1, -1]:
        while True:
            if clint_pos == def_clint:
                return True
            time.sleep(.274) 
            pyautogui.moveTo(clint_pos[0]+3, clint_pos[1]+3)
            time.sleep(.274)
            pyautogui.mouseDown()
            time.sleep(.174) 
            pyautogui.dragTo(x=def_clint[0]+20, y=def_clint[1]+20, duration=.4444, button='left')
            time.sleep(.174) 
            pyautogui.dragTo(x=pull_to[0], y=pull_to[1], duration=.4444, button='left')
            pyautogui.mouseUp()
            time.sleep(.2) 
            clint_pos = imagesearch('images/GGPoker_new.png', precision=0.85, debug=debug, calling_function= 'reset_client_window')
            if clint_pos == def_clint:
                return True
            else:
                print("clint_pos: "+str(clint_pos))
            # time.sleep(2)
    else:
        # print("reset window failed to locate GG-icon")
        sespos = imagesearch('images/session.png', precision=0.85, debug=debug, calling_function= 'reset_client_window')
        if sespos != [-1, -1]:
            print("sespos = "+str(sespos))
            pyautogui.moveTo(sespos[0]+3, sespos[1]+3)
            time.sleep(.174) 
            pyautogui.mouseDown()
            time.sleep(.174) 
            pyautogui.dragTo(x=1200, y=145, duration=0.5, button='left')
            pyautogui.mouseUp()
            time.sleep(.3)
            return reset_client_window()
            # time.sleep(2)
        return False




def find_login_button_and_click():
    img2 = Image.open('images/login_button_2.png')
    if compare_img_screenshot(img2,(1114, 352)):
        pyautogui.click(1177 + random.randrange(1,20), 377 + random.randrange(1,20))
        # print("login clicked (2)")
        time.sleep(.5)
        return True
    img0 = Image.open('images/login_button_0.png')
    if compare_img_screenshot(img0,(1114, 352)):
        pyautogui.click(1177 + random.randrange(1,20), 377 + random.randrange(1,20))
        # print("login clicked (3)")
        time.sleep(.5)
        return True
    img3 = Image.open('images/login_button_3.png')
    if compare_img_screenshot(img3,(1114, 352)):
        pyautogui.click(1177 + random.randrange(1,20), 377 + random.randrange(1,20))
        # print("login clicked (4)")
        time.sleep(.5)
        return True
    time.sleep(.3)
    login_button_pos = imagesearch('images/login_button_2.png', precision=0.90, calling_function= 'find_login_button_and_click')
    print("Login button position: ", login_button_pos)
    if login_button_pos != [-1, -1]:
        pyautogui.click(login_button_pos[0] + random.randrange(1,20), login_button_pos[1] + random.randrange(1,20))
        # print("Login button clicked.")  
        time.sleep(.5)
        return True
    return False


def find_cashier(cshrimg="images/cashier_xmas.png"):
    img = Image.open(cshrimg)
    if compare_img_screenshot(img,(1114, 352), debug_2=False):
        print("already logged in ")
        return True
    img_pos = imagesearch(cshrimg, precision=0.95, debug=False, calling_function= 'find_cashier')
    if img_pos != [-1, -1]:
        return True
    return False



def login(debug = False):


    if find_cashier('images/cashier_insted.png'): # when it is not december
        return False

    if find_cashier(): # when it is december
        return False
    
    if find_cashier('images/chachier_new_year.png'): # when it is january
        return False    

    find_login_button_and_click()
    time.sleep(.3)
    #putting in credentials
    upper_corner = Image.open('images/login_popup_upper_corner.png')
    if compare_img_screenshot(upper_corner,(420, 167)):
        upper_corner_pos = (420, 167)
    else: 
        upper_corner_pos = [-1, -1]
        while upper_corner_pos == [-1, -1]:
            time.sleep(.2)
            upper_corner_pos = imagesearch('images/login_popup_upper_corner.png', precision=0.85, debug=debug, calling_function= 'login')
            time.sleep(.5)
            if upper_corner_pos == [-1, -1]:
                find_login_button_and_click()
    time.sleep(1)
    #credentials
    pyautogui.doubleClick(upper_corner_pos[0] + 236 , upper_corner_pos[1] + 120)
    mails = email.split('-at-')
    pyautogui.typewrite(mails[0], interval=0.01)
    # pyautogui.hotkey('altright','q') # typing @
    if os.name == 'posix':  # macOS 
        pyautogui.hotkey('option', 'l')
    elif os.name == 'nt':  # Windows
        pyautogui.hotkey('altright','q') # typing @
    pyautogui.typewrite(mails[1], interval=0.01)
    pyautogui.doubleClick(upper_corner_pos[0] + 236, upper_corner_pos[1] + 160)
    pyautogui.typewrite(password, interval=0.01)
    logging_in_button = Image.open('images/logging_in_button.png')
    if compare_img_screenshot(logging_in_button,(569, 455)):
        pyautogui.click(569 + random.randrange(1,100), 455 + random.randrange(1,10))
        time.sleep(.3)
        return False
    login_button_pos = imagesearch('images/logging_in_button.png', precision=0.9, debug=debug, calling_function= 'login')
    time.sleep(.1)
    if login_button_pos != [-1, -1]:
        pyautogui.click(login_button_pos[0] + random.randrange(1,100), login_button_pos[1] + random.randrange(1,10))
        time.sleep(.3)
        print("second login button clicked.")
        return False
    print("login did not work, exiting ...")
    exit()





def check_if_client_running(waiting = True, reset = True):
    # print("Checking if GGPoker client is running... waiting = "+str(waiting))
    gg_icon = Image.open('images/GGPoker.png')
    if compare_img_screenshot(gg_icon,(def_clint[0], def_clint[1])):
        time.sleep(.2)
        # best & normal case scenario, the client is already running and focused
        pyautogui.click(def_clint[0], def_clint[1])  
        # print("GGPoker client is running.")
        return True
    global clint_pos
    for _ in range(20 if waiting else 1):
        if compare_img_screenshot(gg_icon,(def_clint[0], def_clint[1])):
            # print("GGPoker client is running.")
            return True
        time.sleep(.1)
        clint_pos = imagesearch('images/GGPoker.png', precision=0.85, debug=False, calling_function= 'check_if_client_running')
        time.sleep(.2)
        if clint_pos != [-1, -1]:
            # print('Client position found at: ', clint_pos)
            if clint_pos != def_clint:
                print("resetting client position on desktop.")
                reset_client_window()
            else: pyautogui.click(clint_pos[0], clint_pos[1])
            return True   
        else:
            if reset:
                if reset_client_window():
                    return True
    print("GGPoker client is no where to be found on desktop screenshot ...")
    return False




def start_client_and_login():
    print("Starting GGPoker client...")
    if os.name == 'posix':  # macOS 
        os.system("open /Applications/GGPoker.app")
    elif os.name == 'nt':  # Windows
        os.system("start C:/Users/shavk/AppData/Roaming/GGPCOM/bin/launcher.exe")

    time.sleep(3)  # wait for the client to start

    if not check_if_client_running():
        print("Client is not running!")
        exit()

    reset_client_window()
    
    time.sleep(1)

    # login()

    return False







'''

grabs a region (topx, topy, bottomx, bottomy)
to the tuple (topx, topy, width, height)

input : a tuple containing the 4 coordinates of the region to capture

output : a PIL image of the area selected.

'''

def region_grabber(region):
    print("I was here at region graber #323")
    x1 = region[0]
    y1 = region[1]
    width = region[2] - x1
    height = region[3] - y1
    return pyautogui.screenshot(region=(x1, y1, width, height))






















'''

Searchs for an image within an area

input :

image : path to the image file (see opencv imread for supported types)
x1 : top left x value
y1 : top left y value
x2 : bottom right x value
y2 : bottom right y value
precision : the higher, the lesser tolerant and fewer false positives are found default is 0.8
im : a PIL image, usefull if you intend to search the same unchanging region for several elements

returns :
the top left corner coordinates of the element if found as an array [x,y] or [-1,-1] if not

'''


def imagesearcharea(image_path, x1, y1, width, height, precision=0.99, im=None):
    if im is None:
        im = pyautogui.screenshot(region=(x1, y1, width, height))
        # im = region_grabber(region=(x1, y1, x2, y2))
        # im.save('testarea2.png') # usefull for debugging purposes, this will save the captured region as "testarea.png"

    img_rgb = np.array(im)
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    template = cv2.imread(image_path, 0)

    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    if max_val < precision:
        return [-1, -1]
    return max_loc












def click_two_times_please(image_path, precision = 0.95, debug = False):
    button_pos = imagesearch(image_path, precision=precision, debug = False, debug_2=debug, calling_function="click_two_times_please")
    time.sleep(.2)
    # print(f"{image_path} position: ", button_pos)
    if button_pos != [-1, -1]:
        pyautogui.click(button_pos[0] + random.randrange(1,10), button_pos[1] + random.randrange(1,10))
        time.sleep(.1)
        pyautogui.click(button_pos[0] + random.randrange(1,10), button_pos[1] + random.randrange(1,10))
        time.sleep(.1)
        # print(f"{image_path} clicked 2x.")  
        return True
    return False


def click_one_times_please(image_path, precision=0.95,  debug = False):
    for _ in range(3):
        button_pos = imagesearch(image_path, precision=precision, debug = False, debug_2 = debug, calling_function="click_one_times_please")
        time.sleep(.53)
        # print(f"{image_path} position: ", button_pos)
        if button_pos != [-1, -1]:
            pyautogui.click(button_pos[0] + random.randrange(1,4), button_pos[1] + random.randrange(1,4))
            time.sleep(.5)
            # print(f"{image_path} clicked 1x.")
            return True
    return False



def see_if_there_is_l_info():
    global l_info_read
    img = Image.open('images/i_understand.png')
    if compare_img_screenshot(img,(630, 569)):
        pyautogui.click(630 + random.randrange(1,20), 569 + random.randrange(1,20))
        time.sleep(.4)
        l_info_read = True
        return True
    time.sleep(.1)
    result = click_one_times_please('images/i_understand.png', precision=0.85, debug = False)
    # print("I understand , I was here #2 , result: "+str(result))
    if result:
        l_info_read = True
        return True
    return False


def push_holdem():
    # click home here
    pyautogui.click(24 + random.randrange(0,5), 156 + random.randrange(0,5))
    time.sleep(.1)
    if not l_info_read:
        see_if_there_is_l_info()
    img = Image.open('images/holdem_clicked.png')
    if compare_img_screenshot(img,(350, 142)):
        print("Holdem already clicked.")
        return True
    pyautogui.click(24 + random.randrange(0,7), 156 + random.randrange(0,7))
    time.sleep(.1)
    if not l_info_read:
        see_if_there_is_l_info()
    img = Image.open('images/holdem.png')
    if compare_img_screenshot(img,(350, 142)):
        pyautogui.click(350 + random.randrange(3,10), 142 + random.randrange(3,10))
        print("Holdem clicked.")  
        time.sleep(.5)
        return True
    
    # print("Holdem position: ", push_holdem_pos)
    for _ in range(7):
        time.sleep(1.5)
        if not l_info_read:
            see_if_there_is_l_info()
        push_holdem_pos = imagesearch('images/holdem.png', precision=.83, debug = False, debug_2 = False, calling_function="push_holdem")
        print("push_holdem_pos: "+str(push_holdem_pos))
        if push_holdem_pos != [-1, -1]:
            pyautogui.click(push_holdem_pos[0] +3, push_holdem_pos[1] +3)
            # print("Holdem clicked. 2")
            time.sleep(.5)
            img = Image.open('images/holdem_clicked.png')
            if compare_img_screenshot(img,(350, 142), debug=False, debug_2=False):
                # print("Holdem confirmed clicked.")
                return True
            if imagesearch('images/holdem_clicked.png', precision=0.95, debug = False, debug_2 = False, calling_function="push_holdem") != [-1, -1]:
                # print("Holdem confirmed clicked. 2")
                return True
        else:
            print("something went wrong somehow idk dude ...")
            pyautogui.click(405, 150)
            # print(pyautogui.position())
            if imagesearch('images/holdem_clicked.png', precision=0.9, debug = False, calling_function="push_holdem") != [-1, -1]:
                print("Holdem already clicked. 5 (might be wrong tho!)")
                return True
            time.sleep(1)
            push_holdem_pos = imagesearch('images/holdem.png', precision=.90, debug = False, calling_function="push_holdem")
            print("push_holdem_pos: "+str(push_holdem_pos))
            if not l_info_read:
                see_if_there_is_l_info()
            if push_holdem_pos != [-1, -1]:
                pyautogui.click(push_holdem_pos[0] + random.randrange(3,10), push_holdem_pos[1] + random.randrange(3,10))
                print("Holdem clicked. 3")
                time.sleep(.5)
                img = Image.open('images/holdem_clicked.png')
                if compare_img_screenshot(img,(350, 142)):
                    print("Holdem confirmed clicked.")
                    return True
                if imagesearch('images/holdem_clicked.png', precision=0.90, debug = False, calling_function="push_holdem") != [-1, -1]:
                    print("Holdem confirmed clicked. 7")
                    return True
    return False


def scroll_to_bottom():
    pyautogui.moveTo(420 + random.randrange(3,10), 555 + random.randrange(3,10), duration=.5)
    pyautogui.scroll(-5)
    time.sleep(.02)
    pyautogui.scroll(-5)
    time.sleep(.02)
    pyautogui.scroll(-5)
    time.sleep(.02)
    pyautogui.scroll(-5)
    time.sleep(.02)
    pyautogui.scroll(-5)
    time.sleep(.02)
    pyautogui.scroll(-5)
    time.sleep(.02)
    pyautogui.scroll(-5)
    time.sleep(.02)
    pyautogui.scroll(-5)
    time.sleep(.02)
    pyautogui.scroll(-5)
    time.sleep(.02)
    pyautogui.scroll(-5)
    time.sleep(.02)
    pyautogui.scroll(-5)
    time.sleep(.02)
    pyautogui.scroll(-5)
    time.sleep(.02)
    pyautogui.scroll(-5)


def click2(x, y):
    pyautogui.moveTo(x, y)
    im = pyautogui.screenshot(region=(x-100, y-100, 200, 200))
    pixels= im.load()
    pixels[99, 99] = (255, 0, 0, 255)
    pixels[99, 100] = (255, 0, 0, 255)
    pixels[100, 99] = (255, 0, 0, 255)
    pixels[100, 100] = (255, 0, 0, 255)
    im.save("clicking_images/click2_"+str(time.time())[:10]+".png")
    pyautogui.click(x, y)



def click_ok(debug = False):
    time.sleep(0.5)
    image_path = 'images/ok.png'
    i = 0
    while True:
        if i > 200:
            close_game()
            exit()
        time.sleep(.25)
        button_pos = imagesearch(image_path, precision=0.95, debug = False, calling_function="click_one_times_please")
        
        # print(f"{image_path} position: ", button_pos)
        if button_pos != [-1, -1]:
            pyautogui.moveTo(button_pos[0] + 270, button_pos[1] - 160)
            time.sleep(.45)
            # click(button_pos[0] + 270, button_pos[1] - 160, debug=True, calling_function="click_ok")
            # pyautogui.click(button_pos[0] + 270, button_pos[1] - 160)
            click2(button_pos[0] + 269, button_pos[1] - 200)
            time.sleep(0.75)
            pyautogui.click(button_pos[0] + random.randrange(10,14), button_pos[1] + random.randrange(1,4))
            time.sleep(1.4)
            button_pos = imagesearch(image_path, precision=0.95, debug = False, calling_function="click_one_times_please")
            if button_pos == [-1, -1]:
                return True
        i += 1
            
    # return False



def open_cards(im = None, debug = False): # get efficiency to 100% (only look at one pixel) , # not needed anymore, due to change of settings in PokerGG-app
    if im == None:
        im = game_screenshot()
    pixels = im.load()
    pix = pixels[600, 500]
    # if debug:
    #     print("pix: "+str(pix))
    if pix[0]>=40 and pix[0]<=50 and pix[1]>=140 and pix[1]<=160 and pix[2]>=40 and pix[2]<=60:
        pyautogui.moveTo(600, 600)
        time.sleep(.2)
        pyautogui.click(600, 600)
        time.sleep(.2)
        pyautogui.click(600, 600)
        print("open cards clicked")
        return True
    if debug:
        print("pix: "+str(pix))
        print("pyautogui.pixel(600, 600): "+str(pyautogui.pixel(600, 600)))
        open_button_pos = imagesearch("images/open.png", debug = True, debug_2 = True, calling_function="open_cards")
        if open_button_pos != [-1, -1]:
            print(open_button_pos)
            pyautogui.click(open_button_pos[0]+10, open_button_pos[1]+5)
            return True
        # crop_ = im.crop((600, 500, 700, 539))
        # print('im.crop((600, 500, 700, 539))')
    # if pix[1] == 32:
    #     return False
    # if pix[1] >= 150:
    #     pyautogui.click(602, 602)

    # return True
    # if debug: print("no open cards")
    return False




def is_red(pixel):
    if pixel[0] < 150:
        return False
    r, g, b, a = pixel
    if r >= 150 and abs(g-60) <= 10 and abs(b-60) <= 10:
        return True
    return False



def fold(im = None, debug = False): #  that's the old fold
    if im == None:
        im = game_screenshot()
    # fold_pos = imagesearch('images/fold.png', precision=0.8, calling_function="fold", debug = debug, debug_2 = debug)
    # time.sleep(.3)
    fold_pos = [530, 600]
    pix = im.getpixel((fold_pos[0], fold_pos[1]-100))
    # pix = pixels[fold_pos[0], fold_pos[1]-100]
    # print("pix "+ str(pix))
    if is_red(pix):
        pyautogui.click(fold_pos[0], fold_pos[1])
        # print("Fold button clicked.")  
        time.sleep(.5)
        return True
    return False



def make_screenshot_of_area(x1, y1, x2, y2, file_name):
    im = region_grabber(region=(x1, y1, x2, y2))
    im.save(file_name)
    print(f"screenshot saved as {file_name}")



def screenshot_area(point = (50, 50), size = [250, 250], file_name = None):
    im = pyautogui.screenshot(region=(point[0], point[1], size[0], size[1]))
    # secs = time.time()
    # im2 = pyautogui.screenshot(region=(8, 32, 50, 50))
    if file_name != None:
        im.save(file_name)
    return im




dgrp = [399, 25] # default game region position



def position_the_game():
    rules = Image.open('images/poker_rules_new.png') # 770 44
    if compare_img_screenshot(rules, (759, 39)):
        return True
    
    time.sleep(.4)
    for _ in range(4):
        time.sleep(.4)
        game_rules_pos = imagesearch('images/poker_rules_new.png', precision=0.9, calling_function="read_game_rules", debug=False) # may need to adjust to a lower precision 
        if game_rules_pos == [759, 39]:
            return True
        print("Game Rules position: ", game_rules_pos)
        secs = time.time()
        # im4 = screenshot_area(point = (5, 45), size = [25, 25], file_name=f"logo_new_{str(secs).split(".")[0]}.png")

        if game_rules_pos != [-1, -1]:
            pyautogui.moveTo(game_rules_pos[0] - 360, game_rules_pos[1] + 15, duration=0.5)
            time.sleep(.3)
            pyautogui.click(game_rules_pos[0] - 360, game_rules_pos[1] + 15)
            time.sleep(.3)
            pyautogui.mouseDown()
            time.sleep(.2)
            pyautogui.dragTo(x=dgrp[0]+200, y=dgrp[1]+40, duration=1.5, button='left')
            time.sleep(.2)
            pyautogui.dragTo(x=dgrp[0], y=dgrp[1], duration=1.5, button='left')
            time.sleep(.2)
            pyautogui.mouseUp()
            time.sleep(.2)
            if compare_img_screenshot(rules, (759, 39)):
                return True
    return False








def close_game():
    print('closing game')
    game_rules_pos = imagesearch('images/poker_rules_new.png', precision=0.85, calling_function="read_game_rules")
    time.sleep(.53)
    if game_rules_pos == [-1, -1]:
        print("close_game faled to locate poker_rules")
        return False
    pyautogui.click(game_rules_pos[0]+65, game_rules_pos[1]+12)
    time.sleep(.53)
    click_one_times_please("images/leave_tab.png", precision=.8)
    return reset_client_window()




def login_check_agane():
    upper_corner = Image.open('images/login_popup_upper_corner.png')
    if compare_img_screenshot(upper_corner,(420, 167)):
        upper_corner_pos = (420, 167)
    else:
        upper_corner_pos = imagesearch('images/login_popup_upper_corner.png', precision=0.85, debug=False, calling_function= 'login')
        if upper_corner_pos == [-1, -1]:
            return False
    #credentials
    pyautogui.doubleClick(upper_corner_pos[0] + 236 , upper_corner_pos[1] + 120)
    mails = email.split('-at-')
    pyautogui.typewrite(mails[0], interval=0.01)
    # pyautogui.hotkey('altright','q') # typing @
    if os.name == 'posix':  # macOS 
        pyautogui.hotkey('option', 'l')
    elif os.name == 'nt':  # Windows
        pyautogui.hotkey('altright','q') # typing @
    pyautogui.typewrite(mails[1], interval=0.01)
    pyautogui.doubleClick(upper_corner_pos[0] + 236, upper_corner_pos[1] + 160)
    pyautogui.typewrite(password, interval=0.01)
    logging_in_button = Image.open('images/logging_in_button.png')
    if compare_img_screenshot(logging_in_button,(569, 455)):
        pyautogui.click(569 + random.randrange(1,100), 455 + random.randrange(1,10))
        time.sleep(.3)
        return True
    login_button_pos = imagesearch('images/logging_in_button.png', precision=0.9, debug=False, calling_function= 'login')
    time.sleep(.1)
    if login_button_pos != [-1, -1]:
        pyautogui.click(login_button_pos[0] + random.randrange(1,100), login_button_pos[1] + random.randrange(1,10))
        time.sleep(3.5)
        # print("second login button clicked.")
        return True
    exit()


def minimize_client():
    # print("minimizing client")
    pyautogui.click(1128, 54)
    time.sleep(.5)

def maximize_client(): # dont even use that I don't think ...
    # print("maximizing client")
    pyautogui.moveTo(1398, 944, duration=.5)
    time.sleep(1)
    pyautogui.click(1398, 944)
    time.sleep(.5)


def read_game_rules(big_blind = "200"):
    print("reading game rules, big blind: "+str(big_blind))
    def click_selection_or_exit(big_blind="200"): # development game
        if big_blind == "200": #todo : use tesseract to pick game from  big-blind and buy-in
            image_path = 'images/100_200.png'
            if not click_two_times_please(image_path, precision=.8, debug = False):
                print("Could not find selection once ...")
                if not click_two_times_please(image_path, precision=8, debug = False):
                    print("Could not find selection, exiting...")
                    exit()
        elif big_blind == "500":
            print("trying to click selection ... ")
            try:
                # image_path = 'images/200_500.png' # development game
                
                image_path = 'images/2c.png' # production game (big blind: 2c / 5c / ...)
                if not click_two_times_please(image_path, precision=.75, debug = True):
                    print("Could not find selection, exiting...")
                    exit()
            except Exception as e:
                print(e)
                exit()
            print("clicked selection")
        else:
            pass #todo
    
    click_selection_or_exit(big_blind)
    reset_client_window()
    if not l_info_read:
        if see_if_there_is_l_info():
            click_selection_or_exit(big_blind)
    
    while True:
        if click_one_times_please('images/join_table.png', debug=False):
            break
    time.sleep(1)
    reset_client_window()

    while True:
        if click_one_times_please('images/join_again.png', debug=False):
            break
    
    time.sleep(1)

    if login_check_agane():
            if not l_info_read:
                if see_if_there_is_l_info():
                    click_selection_or_exit(big_blind)
            if not l_info_read:
                if see_if_there_is_l_info():
                    click_selection_or_exit(big_blind)
            if not l_info_read:
                if see_if_there_is_l_info():
                    click_one_times_please('images/join_table.png', debug=False)
            if not l_info_read:
                if see_if_there_is_l_info():
                    click_one_times_please('images/join_again.png', debug=False)
    
    time.sleep(1)

    im = screenshot_area(point = (0, 0), size = [1000, 540], file_name=None)

    pixels = im.load()
    if pixels[904, 267] == (92, 92, 92, 255): #receive chips
        print("receiving chips ...")
        click(904, 267, im = im, calling_function="read_game_rules", debug=True)
        return run_it_up(big_blind=big_blind)

    

    click_ok(debug = False)  

    time.sleep(1.0)

    minimize_client()

    # pyautogui.click()
    time.sleep(2)
    # print("positioning the game")
    if position_the_game():
        
        pyautogui.moveTo(25, 25)
        time.sleep(0.25)
        if not check_if_we_holdin_yet():
            # if not global_cash_game_sit_out():
            #     print("!!!! NOT GLOBAL SIT SOMEHOW")
            #     return True
            # time.sleep(1)
            # if check_if_sitting() and check_if_really_seated():
            #     print("read_game_rules returning yes")
            #     return "yes"   
            return True
        else:
            print("#already big blind and holding cards")
            return True #already big blind and holding cards
    print("closing the game")
    if close_game(): # close game brings client back up 
        time.sleep(4)
        reset_client_window()
        # maximize_client()
        time.sleep(3)
        return read_game_rules(big_blind=big_blind) 
    return False

def crop_wh(img, left, top, width, height):
    return img.crop((left, top, left + width, top + height))



def check_if_really_seated(im = None):
    print("checking if we really seated")
    if im == None:
        im = game_screenshot()
    im0 = crop_wh(im, 372, 399, 101, 64)
    # im0.show()
    data1 = np.asarray(im0)
    # print(data1.shape)
    print("data1[4,16,0]: "+str(data1[4,16,0])) # 20
    print("data1[4,17,0]: "+str(data1[4,17,0])) # 22
    print("data1[4,18,0]: "+str(data1[4,18,0])) # 29
    print("data1[4,19,0]: "+str(data1[4,19,0])) # 30
    print("data1[4,20,0]: "+str(data1[4,20,0])) # 23
    print("data1[4,21,0]: "+str(data1[4,21,0])) # 7
    if data1[4,19,0] > 25 and data1[4,16,0]<25:
        if data1[4,18,0] > 25 and data1[4,21,0]<10:
            print("we are")
            return True
    print("we are not")
    return False





def check_if_we_holdin_yet(im = None): # im = game-screenshot, works I think
    print("checking if we holding yet")
    if im == None:
        im = game_screenshot()
    im0 = crop_wh(im, 372, 399, 101, 64)
    # im0.show()
    data1 = np.asarray(im0)
    # print(data1.shape)
    print("data1[4,16,0]: "+str(data1[4,16,0]))
    print("data1[4,17,0]: "+str(data1[4,17,0]))
    print("data1[4,18,0]: "+str(data1[4,18,0]))
    print("data1[4,19,0]: "+str(data1[4,19,0]))
    print("data1[4,20,0]: "+str(data1[4,20,0]))
    print("data1[4,21,0]: "+str(data1[4,21,0]))
    if data1[4,17,0] > 62 and data1[4,17,0]<70:
        if data1[4,18,0] > 140 and data1[4,21,0]<42:
            print("we are not")
            return False
    print("we are")
    return True



def check_if_sitting(im=None): # pass image screenshot
    print("check if sitting ...")
    if im == None:
        im = game_screenshot()
    # chkdimg = Image.open("images/global_sit_checked.png")
    # pixels_postbe = chkdimg.load()
    # actual_pixels = crop_wh(im, 20, 470, 25, 25).load() # 22, 481
    pixels = im.load()
    # print("pixels_postbe[2, 11]: "+str(pixels_postbe[2, 11]))
    # print("actual_pixels[2, 11]: "+str(actual_pixels[2, 11]))
    # print("pixels[22, 481]: "+str(pixels[22, 481]))
    # print("pixels[22, 481]: "+str(pixels[22, 481]))
    # print("pixels[22, 481][0]>20 : "+str(pixels[22, 481][0]>20))
    result = pixels[22, 481][0]>20 
    print("check_if_sitting result: "+str(result))
    return result




def unwait_4blinds(im = None):
    if im == None:
        im = game_screenshot()
    if check_if_w8_for_blinds(im):
        # pyautogui.click(531, 602)
        click(531, 602, im = im, calling_function="unwait_4blinds", debug=False)
    return im
    





def check_if_playerinfo(im = None, desperate = False):
    # print("checking player info ...")
    if im == None:
        im = game_screenshot()
    pixels = im.load()
    pix = pixels[327, 20]
    if desperate:
        print("check_if_playerinfo desperate pix: "+str(pix))
    if pix[0] == pix[1] == pix[2] == 0:
        # print("player info detected")
        return True
    elif pix[0]<4 and pix[1]<4 and pix[2]<4:
        print("player info weakly detected")
        return True
    # print("player info not detected")
    return False




# checking the global cash game sit out button thingy
def global_cash_game_sit_out(im = None): #pass image screenshot here
    print("global_cash_game_sit_out ...")
    if im == None:
        im = game_screenshot()
    if check_if_sitting(im):
        print("#already sitting out")
        return False #already sitting out
    click(24, 576, im = im, calling_function="global_cash_game_sit_out", debug=False)
    time.sleep(2.5)
    if check_if_sitting():
        print("sit out globally clicked")
        return True
    im.save(f"global_cash_game_sit_out_failed{str(time.time())[:12]}.png")
    print("!!! something went wrong at global_cash_game_sit_out")
    return False








    
def get_up_stand_up(im = None): # pass image screenshot here
    print("get_up_stand_up ...")
    if im == None:
        im = game_screenshot()
    if check_if_sitting(im):
        click(25, 576, im = im, calling_function="get_up_stand_up", debug=False)
    else: 
        return False
    # pyautogui.click(25, 581) # global cash game sit out controller
    time.sleep(1.5)
    print("got up")
    return True
    # return False
    


def run_it_up(big_blind = "200"):
    print("run it up with bb: "+big_blind)
    if not check_if_client_running(waiting=False):
        print("starting up client and logging in...")
        start_client_and_login() # always True (see comment on login)
    else:
        reset_client_window()
        # login() 
    time.sleep(1)
    reset_client_window()
    if not l_info_read:
        see_if_there_is_l_info()
    if push_holdem():
        time.sleep(.2)
        if not l_info_read:
            see_if_there_is_l_info()
        time.sleep(.2)
        scroll_to_bottom()
    return read_game_rules(big_blind=big_blind)



def is_yellow(pixel):
    r, g, b, a = pixel
    if r >= 230 and g >= 180 and b <= 50:
        return True
    return False



def read_D(im = None):
    areas = [[654, 349], [653, 150], [382, 116], [185, 150], [184, 349], [365, 366]] # pre-known areas , me last , counterclockwise
    i = 0
    if im == None:
        im = game_screenshot()
    pixels = im.load()
    for area in areas:
        if is_yellow(pixels[area[0], area[1]]): # (239, 193, 36, 255)
            return i
        i += 1
    # im.save(f"d_minus_one{str(time.time())[:12]}.png")
    return -1





def play_shape_of_my_heart(data):
    playsound('acoustic.mp3')



def check_if_w8_for_blinds(im): # works
    print("check_if_w8_for_blinds ...")
    pixels1 = im.load()
    screen_pix = pixels1[528, 503]
    return screen_pix[0]>250 and screen_pix[1] > 185 and screen_pix[1] < 210 and screen_pix[2] > 45 and screen_pix[2] < 55


