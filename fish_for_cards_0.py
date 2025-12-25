import os
import pyautogui
import time
import numpy as np
import cv2
from scripts.shavkats_functions import click_ok, compare_num, fold, game_screenshot, imagesearch, check_if_client_running, find_login_button_and_click, imagesearcharea, \
                                        login, make_screenshot_of_area, read_game_rules, run_it_up, screenshot_area, see_if_there_is_l_info, push_holdem, scroll_to_bottom, click_two_times_please, \
                                            click_one_times_please, start_client_and_login, remove_debug_imgs, read_D, open_cards, is_red, play_shape_of_my_heart
import random
import glob
from Cocoa import NSObject, NSApplication, NSApp, NSWindow, NSButton, NSSound, NSComboBox, NSTextField, NSFont, NSColor
from PyObjCTools import AppHelper
from AppKit import NSScreen
from Foundation import NSDate, NSLog, NSTimer, NSRunLoop, NSDefaultRunLoopMode, NSStatusBar, TRUE, NSRunLoopCommonModes
import objc
from threading import Thread, Lock
import threading
import objc
from Foundation import NSObject, NSTimer, NSRunLoop, NSDate, NSThread
from playsound3 import playsound

class TimerTarget(NSObject):
    def handleTimer_(self, timer):
        print("Timer fired")

prod = True


# remove_debug_imgs()


# def screenshot_loop(iterable):
#     global im 
#     global im2
#     while True:
#         mutex_screenshot.acquire()
#         im = game_screenshot()
#         mutex_screenshot.release()
#         time.sleep(2)
#         mutex_copy.acquire()
#         im2 = im
#         mutex_copy.release()

# def start_screenshots():
#     t = Thread(target=screenshot_loop, args=(1000000,))
#     t.start()




def bin_score(trays_score = 1):
    
    n = 2048 / trays_score

    bin_string = ""

    curr = 1024

    for i in range(13):
        if n>=curr:
            bin_string += "1"
            n -= curr
        else:
            bin_string += "0"
        curr /= 2

    print(bin_string)

    return bin_string



# while training, to enforce confidence with both a greater, but unknown hand (no real world examples of it yet) and a higher own bit/raise before everyone else folding, swap those examples with artificial examples of us bitting higher, (everyone folding in those examples), and/or us owning better hands (enforce lotto-hand-holding-recognition, (low treys score means we got the highest at pants down)), but same output as everyone folds, we get the current pot. machine will learn how to bet and raise carefully , one should think  | then, enforce same behaouviour with pants down, but swapped with rare treys-score value (cards) , to enforce learning of those values (where we win a high amount, with already very rare treys score (start at : just swap cards carefully for a royal flush to teach the machine about it)) | enforce confidence at the start of the learning phase, to collect more data (we win this hand for sure (oh wow ok (when so))) (by us bitting higher & everyone folding more often in training data) | only during training, with play money and a good & long while before production stage (carefully enhancing training data)


class AppDelegate(NSObject):

    card_positions = [255, 327, 399, 471, 543] #195, 25 25
    cards = [ "2d" , "2h" , "2s" , "2c" , "3d" , "3h" , "3s" , "3c" , "4d" , "4h" , "4s" , "4c" , "5d" , "5h" , "5s" , "5c" , "6d" , "6h" , "6s" , "6c" , "7d" , "7h" , "7s" , "7c" , "8d" , "8h" , "8s" , "8c" , "9d" , "9h" , "9s" , "9c" , "Td" , "Th" , "Ts" , "Tc" , "Jd" , "Jh" , "Js" , "Jc" , "Qd" , "Qh" , "Qs" , "Qc" , "Kd" , "Kh" , "Ks" , "Kc" , "Ad" , "Ah" , "As" , "Ac" ]
    # learn 1 + 16 swap suits according to schema, to multiply data and get rid of bias against suits

    #no more ticks when this all is colleted
    done_collected = False
    big_blind = "200"
    mutex_screenshot = Lock()
    mutex_copy = Lock()
    im = game_screenshot(save=False) # game screenshot
    im2 = game_screenshot(save=False) # copy of game screenshot
    cards_open = False # are we holding cards
    d_position = -1 # where is the D
    own_card_left = "nn"
    own_card_right = "nn"
    deck_card_1 = "nn"
    deck_card_2 = "nn"
    deck_card_3 = "nn"
    deck_card_4 = "nn"
    deck_card_5 = "nn"

    hand_cards = [ 0 , 0 , ] # two-hot : .5 for one , 1 for two of that value
    hand_same_suited = False

    treys_score = [ 8000 , 8000 , 8000 ] # bin_score, encode in binary to feed into machine | one for flop, turn and river each, 0 at earlier stages of game respectively
    # todo: bin_score here

    holdemners_pos = [ False ,  False ,  False ,  False ,  False ,  False ,  False ,  False ,  False ] # me first, counterclockwise | in future list representations the positions marked False here will be skipped
    holdermners = 0 # 6 number of people to receive cards every round | number of True values in holdemners_pos
    num_active_players = 0 # 6 (card holders currently)
    num_active_players_after_me = 0
    num_active_players_before_me = 0 # starting at small blind
    everyones_money = [ 0, 0, 0, 0, 0, 0, 0, 0, 0] #remember to see if player swaps (clockwise from my position only holdemners, not empty seats (move remaining seats, if one empties))
    everyones_moneydiff_1_round = [ 0, 0, 0, 0, 0, 0, 0, 0, 0] #remember to see if player swaps (number rounds in player info)
    everyones_moneydiff_2_round = [ 0, 0, 0, 0, 0, 0, 0, 0, 0] # """"
    everyones_moneydiff_4_round = [ 0, 0, 0, 0, 0, 0, 0, 0, 0] # ...
    everyones_moneydiff_8_round = [ 0, 0, 0, 0, 0, 0, 0, 0, 0]#remember to see if player swaps (clockwise counting from my position only holdemners, not empty seats (move remaining seats, if one empties))
    everyones_moneydiff_16_round = [ 0, 0, 0, 0, 0, 0, 0, 0, 0]
    everyones_moneydiff_32_round = [ 0, 0, 0, 0, 0, 0, 0, 0, 0]#remember to see if player swaps (clockwise counting from my position only holdemners, not empty seats (move remaining seats, if one empties))
    everyones_moneydiff_64_round = [ 0, 0, 0, 0, 0, 0, 0, 0, 0]
    player_data = [ [ 8000 , 8000 , 8000, 8000 ], [ 8000 , 8000 , 8000, 8000 ], [ 8000 , 8000 , 8000, 8000 ], [ 8000 , 8000 , 8000, 8000 ], [ 8000 , 8000 , 8000, 8000 ], [ 8000 , 8000 , 8000, 8000 ], [ 8000 , 8000 , 8000, 8000 ], [ 8000 , 8000 , 8000, 8000 ], [ 8000 , 8000 , 8000 ]] #read at beginning while waiting or sitting out
    n_called_with_me = []
    
    
    total_pot_money = 0 
    round_pot = 0
    old_pot = 0
    
    
    small_blind_position = [ False ,  False ,  False ,  False ,  False ,  False ,  False ,  False ,  False ] # me first | (clockwise counting from my position only holdemners, not empty seats (move remaining seats, if one empties))

    round_phase = [ False , False , False , False ] # preflop flop turn river (one-hot)^

    number_raises_per_roundphase = [ 0 , 0 , 0 , 0 ] # preflop flop turn river

    number_calls_per_roundphase = [ 0 , 0 , 0 , 0 ] # preflop flop turn river

    pot_grew_perRoundphase = [ 0 , 0 , 0 , 0 ] # preflop flop turn river

    

    number_raises_all_together = 0

    number_calls_all_together = 0

    experts_say_fold = .0 # first model
    decision = "None_yet"
    experts_would_win = .0 # model , taking decision in consideration



    lock = threading.Lock() #decision lock
    lock2 = threading.Lock() #busy ticking lock
    busy_ticking = False

    
    time_to_act = False # is there red buttons on the bottom right

    def applicationDidFinishLaunching_(self, aNotification):
        if prod:
            NSThread.detachNewThreadSelector_toTarget_withObject_("startSong:", self, "hello")

    def sayHello_(self, sender):
        print("Hello again, World!")

    def hide_(self, sender):
        print("Hiding buttons ...")
        if self.hello is not None:
            self.hello.setHidden_(True)
        sender.setHidden_(True)

    def dropdownSelectionChanged_(self, sender):
        selected_index = sender.indexOfSelectedItem()
        selected_value = sender.objectValueOfSelectedItem()
        print(f"Dropdown selection changed: index={selected_index}, value='{selected_value}'")
        if selected_value in ["200", "500"]:
            self.big_blind = selected_value
            if self.bb_info is not None:
                self.bb_info.setStringValue_(f"Big Blind: {self.big_blind}")
            # bb_info.setNeedsDisplay_(True)
        else:
            # sender.deselectItemAtIndex_(selected_index)
            sender.setStringValue_(self.big_blind)
            # print(f"Invalid big blind selection: '{selected_value}'")
            # sender.setStringValue_(big_blind)
            # sender.setNeedsDisplay_(True)
            print(f"Invalid selection. Reverting to previous big blind: '{self.big_blind}'")

    def startSong_(self, sender):
        # self.performSelectorOnMainThread_withObject_waitUntilDone_("seeIfThisPrints:", None, False)
        playsound('acoustic.mp3')
        # self.performSelectorOnMainThread_withObject_waitUntilDone_("didFinish:", None, False)
    
    def didFinish_(self, arg):
        NSLog("didFinish called on main thread")

    def runitup_(self, sender):

        # hide start-up controls
        if self.dropdown is not None:
            self.dropdown.setHidden_(True)
        if self.bb_info is not None:
            self.bb_info.setHidden_(True)
        if self.gg_poker_button is not None:
            self.gg_poker_button.setHidden_(True)


        # new buttons here
        # buttons for holdem
        self.foldB.setHidden_(False)
        self.callB.setHidden_(False)
        self.raiseB1.setHidden_(False)
        self.raiseB2.setHidden_(False)


        # start poker client and game
        run_it_up(big_blind = self.big_blind)

        time.sleep(.1)

        # make first screenshot before anyone acquires any lock on these
        self.im = game_screenshot()
        self.im2 = self.im

        # start_screenshots()
        #start a timer to make screenshots every 5 seconds
        start_time = NSDate.date() #todo: every 2 secs switch between 1. make screenshot 2. use existing screenshot to evaluate
        self.timer2 = NSTimer.alloc().initWithFireDate_interval_target_selector_userInfo_repeats_(start_time, 5.0, self, 'gSSOtherThread:', None, True)
        self.timer2.setTolerance_(6.0)  
        NSRunLoop.currentRunLoop().addTimer_forMode_(self.timer2, NSDefaultRunLoopMode)
        self.timer2.fire()

        


        # start a timer to tick every <n> seconds
        start_time = NSDate.date() #todo: every 2 secs switch between 1. make screenshot 2. use existing screenshot to evaluate
        self.timer = NSTimer.alloc().initWithFireDate_interval_target_selector_userInfo_repeats_(start_time, 1.2, self, 'tickOtherThread:', None, True)
        self.timer2.setTolerance_(1.0)  
        NSRunLoop.currentRunLoop().addTimer_forMode_(self.timer, NSDefaultRunLoopMode)
        self.timer.fire()


    def gSSOtherThread_(self, userInfo):
        NSThread.detachNewThreadSelector_toTarget_withObject_("gameScreenshot:", self, "hello")



    def fold_(self, userInfo):
        with self.lock:
            self.decision = "fold"
        

    def call_(self, userInfo):
        with self.lock:
            self.decision = "call"

    def raise1_(self, userInfo):
        with self.lock:
            self.decision = "raise1"

    def raise2_(self, userInfo):
        with self.lock:
            self.decision = "2raise2"

        
    def gameScreenshot_(self, userInfo): # time to cat logic in here
        self.mutex_screenshot.acquire()
        self.im = game_screenshot()
        self.mutex_screenshot.release()
        # time.sleep(2)
        self.mutex_copy.acquire()
        self.im2 = self.im
        self.mutex_copy.release()

        # time to cat logic :

        # if time to act: timeToAct()
        # self.timeToAct_(None) #this needs be only place to call this function (for image mutex')
        self.time_to_act = True 
        pix = self.im.getpixel((530, 500)) # there should be a red button here, when it is our turn 
        # print("pix (where red button might be): "+ str(pix))
        if is_red(pix):
            time.sleep(2)
            print("self.decision: "+str(self.decision))
            with self.lock:
                if self.decision == "None_yet":
                    #acting (ToDo) check if all values have been read, read everything necessary (number on the middle button) and make decision
                    pyautogui.click(540, 610)
                elif self.decision == "fold":
                    print("fold was clicked")
                    pyautogui.click(540, 610)
                elif self.decision == "call":
                    print("call was clicked")
                    pyautogui.click(670, 610)
                elif self.decision == "raise1":
                    print("raise1 was clicked")
                    pyautogui.click(800, 610)
                    self.decision == "call"
                elif self.decision == "2raise2":
                    print("raise2 was clicked")
                    pyautogui.click(659, 557)
                    pyautogui.click(800, 610)
                    self.decision == "call"
                else: 
                    self.decision == "None_yet"
        else:
            print("no red buttons ...")
        self.time_to_act = False
        

    # def timeToAct_(self, user_info):
    #     fold_pos = [530, 600] #there should be a red button here, when it is our turn 
    #     pix = self.im.getpixel((fold_pos[0], fold_pos[1]-100))
    #     # pix = pixels[fold_pos[0], fold_pos[1]-100]
        
    #     if is_red(pix):
    #         time.sleep(2.5)
    #         if self.decision == "None_yet":
    #             self.time_to_act = True 
    #             #acting (ToDo) check if all values have been read, read everything necessary (number on the middle button) and make decision
    #             pyautogui.click(fold_pos[0], fold_pos[1])
    #             print("Fold button clicked.")  
    #             self.time_to_act = False
    #             return True
    #         else: return True
    #     return False

    def tickOtherThread_(self, notification):
        NSThread.detachNewThreadSelector_toTarget_withObject_("tick:", self, "hello")
    
    

    # ingame iteration loop
    def tick_(self, notification):

        if self.done_collected: #maybe never happens or used 
            return

        if self.time_to_act:
            print("time_to_act active")
            return
        
        if self.busy_ticking:
            print("BUSY TICKIINGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG")
            return # already in this q
        
        with self.lock2:
            self.busy_ticking = True

        # print(notification)
        
        # print("\n ... \n")

        # print(self.state)
        # print("tick at %@", NSDate.date())

        # print(" - ")

        # #debug: show pixel value at (600,590)
        
        # get current screenshot
        if not self.mutex_screenshot.locked():
            print("TOOK ORIGINAL !!!!!!!!!!!!!!!!!!!")
            self.mutex_screenshot.acquire()
            current_im = self.im
            self.mutex_screenshot.release()
        elif not self.mutex_copy.locked():
            # print("tick_ took old copy (screenshot being made)")
            self.mutex_copy.acquire()
            current_im = self.im2
            self.mutex_copy.release()
        else:
            print("---- !!!!! I SHOULD NOT BE HERE !!!!! ----")
            return

        
        # im_array = np.array(im)
        # print(" type(im_array) =", type(im_array))
        # print(" im_array.shape =", im_array.shape)
        # for i in range(5):
        #     print("lalala "+str(i+1)+": ")
        #     print(" im_array[500, 600] =", im_array[500, 600])

        
        self.d_position = read_D(current_im)
        print("self.d_position: "+str(self.d_position))


        # print("cards open : "+str(self.cards_open))

        # if not self.cards_open:
        #     temp_opencards = open_cards(current_im)
        #     print('temp_opencards: '+str(temp_opencards))
        #     if temp_opencards:
        #         self.cards_open = True


        # time.sleep(1)

        # if self.cards_open == True:
        #     print("I was here #12")
        #     try:
        #         if fold(current_im):
        #             print('I was here agane #12')
        #             self.cards_open = False
        #     except Exception as e:
        #         print(e)

        # print(" - ")

        with self.lock2:
            self.busy_ticking = False























def GUI():

    win = NSWindow.alloc()
    w = 500 # width for the gui
    h = 350 # height for the gui
    sw = NSScreen.mainScreen().frame().size.width
    frame = ((sw-w, 0), (w, h))
    win.initWithContentRect_styleMask_backing_defer_(frame, 15, 2, 0)
    win.setTitle_("Poker Game")
    win.setLevel_(3)  # floating window
    delegate = AppDelegate.alloc().init()
    NSApp().setDelegate_(delegate)
    delegate.window = win
    app = NSApplication.sharedApplication()

    # we must keep a reference to the delegate object ourselves,
    # NSApp.setDelegate_() doesn't retain it. A local variable is
    # enough here.



    # sh = NSScreen.mainScreen().frame().size.height



    dropdown = NSComboBox.alloc().initWithFrame_(((20.0, 310.0), (150.0, 26.0)))
    dropdown.addItemsWithObjectValues_(["200", "500"])
    win.contentView().addSubview_(dropdown)
    dropdown.selectItemAtIndex_(0)
    dropdown.setEditable_(True)
    dropdown.setUsesDataSource_(False)
    dropdown.setBezeled_(True)
    dropdown.setDrawsBackground_(True)
    dropdown.setEnabled_(True)  
    dropdown.setHidden_(False)
    # dropdown.setCompletes_(True)
    # dropdown.setNumberOfVisibleItems_(3)
    # dropdown.setDelegate_(delegate)
    # dropdown.setTarget_(delegate)
    dropdown.setAction_("dropdownSelectionChanged:")
    dropdown.setStringValue_("200")
    print(f"Initial big blind value in dropdown: '{"200"}'")
    # dropdown.setFont_(NSFont.fontWithName_size_("Helvetica", 14.0))
    dropdown.setPlaceholderString_("Select Big Blind")
    # dropdown.setUsesDataSource_(True)
    # dropdown.reloadData()
    dropdown.setNumberOfVisibleItems_(2)
    # dropdown.setCompletes_(True)
    dropdown.setDelegate_(delegate)
    dropdown.setTarget_(app.delegate())
    delegate.dropdown = dropdown

    # delegate.button = btn


    bb_info = NSTextField.alloc().initWithFrame_(((20.0, 270.0), (150.0, 26.0)))
    win.contentView().addSubview_(bb_info)
    bb_info.setStringValue_(f"Big Blind: {"200"}")
    bb_info.setBezeled_(False)
    bb_info.setDrawsBackground_(False)
    bb_info.setEditable_(False)
    bb_info.setSelectable_(False)
    delegate.bb_info = bb_info
    # bb_info.setFont_(NSFont.fontWithName_size_("Helvetica", 14.0))
    # bb_info.setAlignment_(2)  # center alignment
    # bb_info.sizeToFit()
    # bb_info.setFrameOrigin_((200.0, 280.0))
    # bb_info.setHidden_(False)
    # bb_info.setNeedsDisplay_(True)
    # bb_info.display()

     # Create buttons

    gg_poker_button = NSButton.alloc().initWithFrame_(((190.0, 260.0), (80.0, 80.0)))
    win.contentView().addSubview_(gg_poker_button)
    gg_poker_button.setBezelStyle_(4)
    gg_poker_button.setTitle_("Start Poker")
    gg_poker_button.setTarget_(app.delegate())
    gg_poker_button.setAction_("runitup:")
    delegate.gg_poker_button = gg_poker_button

    hello = NSButton.alloc().initWithFrame_(((10.0, 10.0), (80.0, 80.0)))
    win.contentView().addSubview_(hello)
    hello.setBezelStyle_(4)
    hello.setTitle_("Hello!")
    hello.setTarget_(app.delegate())
    hello.setAction_("sayHello:")
    delegate.hello = hello

    # holdm btns
    foldB = NSButton.alloc().initWithFrame_(((10.0, 260.0), (50.0, 50.0)))
    win.contentView().addSubview_(foldB)
    foldB.setBezelStyle_(4)
    foldB.setTitle_("fikd")
    foldB.setTarget_(app.delegate())
    foldB.setAction_("fold:")
    foldB.setContentTintColor_(NSColor.redColor())
    foldB.setHidden_(True)
    delegate.foldB = foldB

    callB = NSButton.alloc().initWithFrame_(((70.0, 260.0), (50.0, 50.0)))
    win.contentView().addSubview_(callB)
    callB.setBezelStyle_(4)
    callB.setTitle_("call")
    callB.setTarget_(app.delegate())
    callB.setAction_("call:")
    callB.setHidden_(True)
    delegate.callB = callB

    raiseB1 = NSButton.alloc().initWithFrame_(((130.0, 260.0), (50.0, 50.0)))
    win.contentView().addSubview_(raiseB1)
    raiseB1.setBezelStyle_(4)
    raiseB1.setTitle_("R")
    raiseB1.setTarget_(app.delegate())
    raiseB1.setAction_("raise1:")
    raiseB1.setHidden_(True)
    delegate.raiseB1 = raiseB1

    raiseB2 = NSButton.alloc().initWithFrame_(((190.0, 270.0), (30.0, 30.0)))
    win.contentView().addSubview_(raiseB2)
    raiseB2.setBezelStyle_(4)
    raiseB2.setTitle_("R2")
    raiseB2.setTarget_(app.delegate())
    raiseB2.setAction_("raise2:")
    raiseB2.setHidden_(True)
    delegate.raiseB2 = raiseB2

    # foldB = NSButton.alloc().initWithFrame_(((10.0, 230.0), (80.0, 80.0)))
    # foldB.setBezelStyle_(4)
    # foldB.setTitle_("fikd")
    # foldB.setTarget_(app.delegate())
    # foldB.setAction_("fold:")
    # delegate.foldB = foldB

    # foldB = NSButton.alloc().initWithFrame_(((10.0, 230.0), (80.0, 80.0)))
    # foldB.setBezelStyle_(4)
    # foldB.setTitle_("fikd")
    # foldB.setTarget_(app.delegate())
    # foldB.setAction_("fold:")
    # delegate.foldB = foldB

    # beep = NSSound.alloc()
    # beep.initWithContentsOfFile_byReference_("/System/Library/Sounds/Tink.Aiff", 1)
    # hello.setSound_(beep)

    bye = NSButton.alloc().initWithFrame_(((100.0, 10.0), (80.0, 80.0)))
    win.contentView().addSubview_(bye)
    bye.setBezelStyle_(4)
    bye.setTarget_(app)
    bye.setAction_("stop:")
    bye.setEnabled_(1)
    # bye.setHidden_(True)
    bye.setTitle_("Goodbye!")

    hide = NSButton.alloc().initWithFrame_(((190.0, 10.0), (80.0, 80.0)))
    win.contentView().addSubview_(hide)
    hide.setBezelStyle_(4)
    hide.setTarget_(app.delegate())
    hide.setAction_("hide:")
    hide.setEnabled_(1)
    hide.setTitle_("Hide!")





    

    # adios = NSSound.alloc()
    # adios.initWithContentsOfFile_byReference_("/System/Library/Sounds/Basso.aiff", 1)
    # bye.setSound_(adios)

    win.display()
    win.orderFrontRegardless()  # but this one does

    AppHelper.runEventLoop()




GUI()


