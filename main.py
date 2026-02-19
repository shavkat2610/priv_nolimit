import csv
import pyautogui
import time
import numpy as np
from chatGPT_XGBRegressor import river_features, turn_features
from scripts.shavkats_functions import click_ok,  game_screenshot, global_cash_game_sit_out, imagesearch, check_if_client_running, find_login_button_and_click, imagesearcharea, \
                                        login, make_screenshot_of_area, read_game_rules, run_it_up, screenshot_area, see_if_there_is_l_info, push_holdem, scroll_to_bottom, click_two_times_please, \
                                            click_one_times_please, start_client_and_login, remove_debug_imgs, read_D, open_cards, is_red, play_shape_of_my_heart, close_game, \
                                            check_if_w8_for_blinds, get_up_stand_up, unwait_4blinds
import random
from Cocoa import NSObject, NSApplication, NSApp, NSWindow, NSButton, NSSound, NSComboBox, NSTextField, NSFont, NSColor, NSSlider
from PyObjCTools import AppHelper
from AppKit import NSScreen
from Foundation import NSDate, NSLog, NSTimer, NSRunLoop, NSDefaultRunLoopMode, NSStatusBar, TRUE, NSRunLoopCommonModes
import objc
from threading import Thread, Lock
import threading
from Foundation import NSObject, NSTimer, NSRunLoop, NSDate, NSThread
from playsound3 import playsound
import pytesseract
from fish_for_cards import crop_wh, fish_for_own_cards, fish_for_deck_cards, prepare_fishing_own_cards, prepare_fishing_deck_cards, own_suits_right, own_suits_left, own_values_left, own_values_right, own_suit_left, own_value_left, own_suits_right, own_value_right, own_card_right_filenames, own_card_left_filenames
from small_shwatsgoingon import check_if_we_holdin_yet, how_much , check_holders, read_own_cards, read_own_money_valid, read_player_info, read_total_pot_money, read_deck_cards, \
                                                                    read_old_pot_money, read_own_money, load_smol_watsgoingon_model, general_whats_going_on_model, handle_all_in,\
                                                                          load_flop_equity_model, flop_equity_model_predict, extract_flop_features, load_turn_model, \
                                                                          turn_model_predict_multiple, load_river_model, river_model_predict_multiple, load_flop_model, flop_model_predict_multiple, \
                                                                                prepare_pot_digits
from monte_carlo_0 import exact_win_probability
from treys import Card
from treys import Evaluator
from PIL import Image



# os.environ['TF_CPP_MIN_LOG_LEVEL'] = '0' # 3 initally
# import subprocess


# done:


# read played info -done
# red own cards -done
# read pot money -done
# read deck cards -done
# read old pot money -done
# read own money (for who_won and to know when it's all-in) - done
# general, small whats-going-on-model to see if there is maybe a dancing man, connectivity-issues or something to click ", for added excitement" -done
# writo to csv - done
# fifth raise button, by 16x big blind - done
# keep track of money, check if everything read corrrectly ... - done
# get allIn's out of river, flop and turn samples - done



# todo:

# feed in more features in river and turn - time
# # feed in how many card holders there is still before me and after me, before big_blind
# # pot_20 etc. into I raised at preflop, flop, river, turn, how much I had to call at ... and potheight at ...
# # my raises, oponents raises at flop, river and turn time 
# features at river time, turn time
# run it three times, accept opponents request
# run it three times ... # not always done yet ...
# added money of participants fed into data ?
# read money of participants ?
# retrain tesseract # get more training samples - in works
# adjust tesseract ocr : retrain model (with how_much-, total_pot- & to_call-data)
# the features we get for flop-equity-model, get most important ones, save them for later model-adjustment
# handle all-in situations ... - in works or maybe done ?
# open last card ... - not yet done completely

# all-in logic : check if it still says so,, wait, repeat until its over -> see if we need to buy more chips or global cash game sit out and reread player info ... 
# write to app: info on win probability 1 v 1 (at flop, river and turn)
# write to app: info on win probability 1 v number called (at flop, river and turn) ( probability ^ number )
# write to app: info on win probability 1 v (number called + everyone after me , (before and including dealer , who is holding cards (who might call after me))) (at flop, river and turn) ( probability ^ number )
# make decisions based off of collected values
# after bigger win -> sit out, collect new player info if possible
# when folding early -> update player data ?

# close_game-button 
# run it back up button (with possibly another big blind)




prepare_fishing_own_cards()
prepare_fishing_deck_cards()
load_smol_watsgoingon_model()
load_flop_equity_model()
load_flop_model()
load_river_model()
load_turn_model()
prepare_pot_digits()




prod = False # play soundtrack or no
max_num_hands = 150 # todo: mave tables or restart client after this many ahnds maybe?





def count_holders(holders = [ False, False, False, False, False, False, False, False]):
    i = 0
    for holder in holders:
        if holder == True:
            i += 1
    return i


def count_before_me(dealer_pos, holders_pos):
    if dealer_pos == -1:
        return -1
    if dealer_pos == 0:
        return 0
    result = 0
    for i in range(dealer_pos):
        if holders_pos[i]==True:
            result +=1
    return result


class AppDelegate(NSObject):

    big_blind = "200"
    evaluator = Evaluator()
    
    confidence_lock = Lock()
    confidence = 3.0





    # modelling

    # not yet in use
    experts_say_fold = .0 # first model
    
    mod_writing_lock = Lock()
    flop_model_inputs = []
    made_flop_model_input = False
    river_model_inputs = []
    made_river_model_input = False
    turn_model_inputs = [] # make this into array, allow multiple . empty the list before reset values, after writing to csv, with according output # done in theory, need further testing tho maybe ...
    made_turn_model_input = False    
    model_output = 0
    made_model_output = True
    wrote_to_csv_s = False


    # holdemners_pos = [ False ,  False ,  False ,  False ,  False ,  False ,  False ,  False ,  False ] # me first, counterclockwise 
    # holdermners = 0 # 6 number of people to receive cards every round | number of True values in holdemners_pos

    player_data_lock = Lock()
    player_data = [ [ 0 , 0 , 0, 0 ], [ 0 , 0 , 0, 0 ], [ 0 , 0 , 0, 0 ], [ 0, 0, 0, 0], [ 0, 0, 0, 0], [ 0, 0, 0, 0], [ 0, 0, 0, 0], [ 0, 0, 0, 0], [ 0 , 0 , 0 , 0 ]] #read at beginning while waiting or sitting out


    mutex_screenshot = Lock()
    im = Image.open("starter_img.png")
    
    game_stage_lock = Lock()
    game_stage_current = "no_decision_to_be_made" # preflop, flop, river, turn, no_decision_to_be_made
    
    potheight_lock = Lock()
    potheight_after_preflop = 1.5
    potheight_after_flop = 3.5
    potheight_after_river = 4.5
    potheight = 0.1
    to_call = 0.0
    difference_tocall_n_potheight = to_call/potheight # important for early decision making , and also for ai models possibly

    lock = Lock() #
    own_money = 0.0
    own_money_before_last_preflop = 30.0

    d_lock = Lock() # for setting dealer position
    d_position = -1 # where is the D

    dec_lock = Lock() # for decision attribute
    decision = "None_yet"

    mk_comte_carlo_decision_lock = Lock()
    probability_1_1 = -1
    setting_monte_caro = False
    equity_river = -1
    equity_flop = -1
    flop_features = np.zeros(32)
    river_features = np.zeros(14)
    turn_features = np.zeros(15)

    lock2 = Lock() #busy ticking lock
    busy_ticking = False

    acting_lock = Lock()
    time_to_act = False # is there red buttons on the bottom right

    cards_lock = Lock()
    deck_card_1 = "nn"
    deck_card_2 = "nn"
    deck_card_3 = "nn"
    deck_card_4 = "nn"
    deck_card_5 = "nn"

    own_cards_lock = Lock()
    own_card_left = "nn"
    own_card_right = "nn"    
    cards_open = False # are we holding cards after flop or no_decision_to_be_made

    our_turn_lock = Lock()
    holders_pos = [ False ,  False ,  False ,  False ,  False ,  False ,  False ,  False ] # check_holders(im) #   # from me counting, counterclockwise, me not considered, because I still hold cards when this is interesting 
    num_active_players = 0 # 5 (card holders currently) (aka holders)
    num_active_players_before_me = 0 # starting at small blind | (aka holders)

    valset_lock = Lock()
    values_set = False
    number_of_the_universe = 1



    def setValuesOurTurn_(self, current_im):
        with self.our_turn_lock:
            self.holders_pos = check_holders(current_im)
            # print("holders set ...")
            self.num_active_players = count_holders(self.holders_pos)
            # print("num_active_players set ...")
            with self.d_lock:
                self.num_active_players_before_me = count_before_me(self.d_position, self.holders_pos)
            current_im.save(f"active_hodlers/holders_{self.num_active_players}_{self.num_active_players_before_me}_{str(time.time()).split('.')[0]}.png") # remove later
            # print("num_active_players_before_me set .") 
        # print("done with setValuesOurTurn .")

    def changeStateMonteCaro(self):
        with self.mk_comte_carlo_decision_lock:
            self.probability_1_1 = -1

    def updateOwnMoney_(self, current_im = None): # runs when it is our turn to move # cards are already set  # write to csv for poker model 
        # print("setting own money ...")
        try:
            own_money_current = read_own_money(im=current_im)
            print("own money read: "+str(own_money_current))
            if own_money_current != -10 and own_money_current != None:
                with self.lock:
                    self.own_money = own_money_current                    
                with self.valset_lock:
                    if not self.values_set:
                        self.values_set = True                    
                return True
            return False
        except Exception as e:
            print("read own money failed")
            print(e)
            exit()

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

    def updatePlayerData(self):
        return
        pyautogui.moveTo(25, 25)
        time.sleep(.5)
        if not check_if_we_holdin_yet():
            global_cash_game_sit_out()
        else: return False
        # print("updating player data !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! finally")
        # NSLog("updating player data")
        player_positions = [[760, 436], [731, 192], [422, 130], [111, 190], [89, 441]]
        close_player_info_window_position = [596, 70]
        i = 0
        for pp in player_positions:
            pyautogui.click(pp[0], pp[1])
            time.sleep(1.8)# read here
            im = game_screenshot(save=True)
            self.player_data[i] = read_player_info(im=im)
            pyautogui.click(close_player_info_window_position[0], close_player_info_window_position[1])
            time.sleep(.35)
            i += 1
        print("self.player_data : "+str(self.player_data))
        if get_up_stand_up():
            time.sleep(3)
            unwait_4blinds() # remove later maybe ?
        # return


    def set_munna_initially(self):
        munna = read_own_money()
        if munna != -10 and munna != None:
            with self.lock:
                self.own_money = munna
                self.own_money_before_last_preflop = munna
                return True
        else:
            return False


    def runItUpAgane(self):
        # start poker client and game
        if not run_it_up(big_blind = self.big_blind):
            print("run it up did not work")
            exit() # is this the right way to exit the app?
        # todo: read player data here
        try:
            self.updatePlayerData()
        except Exception as e:
            print(e)   
        # set own money initially
        time.sleep(0.35)
        if not self.set_munna_initially():
            time.sleep(0.35)
            if not self.set_munna_initially():
                time.sleep(0.35)
                if not self.set_munna_initially():
                    time.sleep(0.35)
                    if not self.set_munna_initially():
                        exit("could not read own money at start of game")                     



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
        self.raiseB3.setHidden_(False)
        self.raiseB4.setHidden_(False)
        self.raiseB5.setHidden_(False)


        # start poker client and game
        if not run_it_up(big_blind = self.big_blind):
            print("run it up did not work")
            exit() # is this the right way to exit the app?
        # todo: read player data here
        try:
            self.updatePlayerData()
        except Exception as e:
            print(e)



        # set own money initially
        time.sleep(0.15)
        if not self.set_munna_initially():
            time.sleep(0.15)
            if not self.set_munna_initially():
                time.sleep(0.15)
                if not self.set_munna_initially():
                    time.sleep(0.15)
                    if not self.set_munna_initially():
                        exit("could not read own money at start of game")       

        pyautogui.click(x=1183, y=759)       

        # start_screenshots()
        #start a timer to make screenshots every 5 seconds
        start_time = NSDate.date() #todo: every 2 secs switch between 1. make screenshot 2. use existing screenshot to evaluate
        self.timer2 = NSTimer.alloc().initWithFireDate_interval_target_selector_userInfo_repeats_(start_time, 1.7, self, 'gameScreenshot:', None, True)
        NSRunLoop.currentRunLoop().addTimer_forMode_(self.timer2, NSDefaultRunLoopMode)
        self.timer2.fire()
        print("game screenshot timer started")


    # def gSSOtherThread_(self, userInfo):
    #     NSThread.detachNewThreadSelector_toTarget_withObject_("gameScreenshot:", self, "hello")

    def fold_(self, userInfo):
        with self.dec_lock:
            if self.decision != "fold":
                self.decision = "fold"
            return
        
    def call_(self, userInfo):
        with self.dec_lock:
            if self.decision != "call":
                self.decision = "call"
            return

    def raise1_(self, userInfo):
        with self.dec_lock:
            if self.decision != "raise1":
                self.decision = "raise1"
            return

    def raise2_(self, userInfo):
        with self.dec_lock:
            if self.decision != "2raise2":
                self.decision = "2raise2"
            return

    def raise3_(self, userInfo):
        with self.dec_lock:
            if self.decision != "3raise3":
                self.decision = "3raise3"
            return

    def raise4_(self, userInfo):
        with self.dec_lock:
            if self.decision != "4raise4":
                self.decision = "4raise4"
            return

    def raise5_(self, userInfo):
        with self.dec_lock:
            if self.decision != "5raise5":
                self.decision = "5raise5"
            return


    def startCalculationsOtherThread_(self, boardCards): # only at river- or turn-time
        print("startCalculationsOtherThread_ called ...")
        if self.setting_monte_caro == True:
            return False
        with self.mk_comte_carlo_decision_lock:
            print("mk_comte_carlo_decision_lock acquired")
            self.setting_monte_caro = True
            try:
                boardCards.remove("nn") #river
                print("river")
                with self.own_cards_lock: 
                    print("cards_lock acquired for river features")
                    try: 
                        self.river_features = river_features([self.own_card_left, self.own_card_right], boardCards)     
                    except Exception as e:
                        print("problem with river features ?")
                        print(e)
                        exit()       
            except Exception as e: #turn
                print("probably turn?")
                print(e)
                with self.own_cards_lock:
                    self.turn_features = turn_features([self.own_card_left, self.own_card_right], boardCards)            
            NSThread.detachNewThreadSelector_toTarget_withObject_("doCalculation:", self, boardCards)


    def doCalculation_(self, boardCards): # check in decision, if probability_1_1 is set, or use this function on main thread ...
        print("doCalculation_ called ...")


        with self.cards_lock:
            hero_cards=[self.own_card_left, self.own_card_right]
        
        board_cards = boardCards
        with self.mk_comte_carlo_decision_lock:
            self.probability_1_1 = -1  

        # try:
        #     board_cards.remove("nn")
        # except:
        #     pass        

        if "nn" in board_cards:
            print("not enough board cards read for monte carlo, exiting, something went wrong ...")
            with self.mk_comte_carlo_decision_lock:
                self.probability_1_1 = -1
                exit()         

        monte_caro = exact_win_probability(hero_cards=hero_cards, board_cards=board_cards)

        with self.mk_comte_carlo_decision_lock:
            self.probability_1_1 = monte_caro["Win probability"]+monte_caro["Tie probability"]
            print("probability_1_1: "+str(self.probability_1_1))
        # print("\n! probability_1_1 AT FLOP TIME ! : "+str(self.probability_1_1)+"\n")


        with self.mk_comte_carlo_decision_lock:
            self.setting_monte_caro = False 
            return True


    def mkFlopModelInput(self):
        print("mkFlopModelInput called ...")
        with self.dec_lock:
            decision = self.decision
        with self.potheight_lock:     
            to_call = self.to_call   
        if decision == "fold":
            if to_call > 0.0:
                return # no need to write to table, when folding.  
            else:
                decision_temp = 0.0 # checking when there is nothing to call                                
        elif decision == "call":
            if to_call >= 1.0:
                decision_temp = 1.0    
            else:
                decision_temp = 0.0                            
        elif decision == "raise1":
            if to_call >= 1.0:
                decision_temp = 2.0    
            else:
                decision_temp = 0.25
        elif decision == "2raise2":
            if to_call >= 1.0:
                decision_temp = 2.0    
            else:
                decision_temp = 0.5
        elif decision == "3raise3":
            if to_call >= 1.0:
                decision_temp = 2.0    
            else:
                decision_temp = 0.75
        elif decision == "4raise4":
            if to_call >= 1.0:
                decision_temp = 2.0    
            else:
                decision_temp = 1.0       
        elif decision == "5raise5":
            decision_temp = 2.0                        
        with self.mod_writing_lock:
            if not self.made_flop_model_input:
                self.made_flop_model_input = True
            with self.mk_comte_carlo_decision_lock:
                with self.potheight_lock:    
                    with self.our_turn_lock:                  
                        flop_model_input = [self.equity_flop, self.potheight, self.potheight_after_preflop, self.to_call, decision_temp, 
                                                self.num_active_players, self.num_active_players_before_me,
                                                self.flop_features[0], # 7 + 32 = 39 features total for flop model input
                                                self.flop_features[1], self.flop_features[2], self.flop_features[3], self.flop_features[4],
                                                self.flop_features[5], self.flop_features[6], self.flop_features[7], self.flop_features[8],
                                                self.flop_features[9], self.flop_features[10], self.flop_features[11], self.flop_features[12],
                                                self.flop_features[13], self.flop_features[14], self.flop_features[15], self.flop_features[16],
                                                self.flop_features[17], self.flop_features[18], self.flop_features[19], self.flop_features[20],
                                                self.flop_features[21], self.flop_features[22], self.flop_features[23], self.flop_features[24],
                                                self.flop_features[25], self.flop_features[26], self.flop_features[27], self.flop_features[28],
                                                self.flop_features[29], self.flop_features[30], self.flop_features[31], self.flop_features[31]]
                        self.flop_model_inputs.append(flop_model_input)


    def mkFlopModelInputs_(self, decs): # decs could be [0.0, 0.25, 0.5, 0.75, 1.0, 2.0] (check possible) or [0.0, 1.0, 2.0] (when someone bet before me)
        flop_model_inputs = []
        with self.potheight_lock:
            with self.mk_comte_carlo_decision_lock:
                with self.our_turn_lock: 
                    for decision_temp in decs:
                        # print("self.equity_flop at model-input formation: "+str(self.equity_flop))
                        flop_model_input = [self.equity_flop, self.potheight, self.potheight_after_preflop, self.to_call, decision_temp, 
                                                self.num_active_players, self.num_active_players_before_me,
                                                self.flop_features[0], 
                                            self.flop_features[1], self.flop_features[2], self.flop_features[3], self.flop_features[4],
                                            self.flop_features[5], self.flop_features[6], self.flop_features[7], self.flop_features[8],
                                            self.flop_features[9], self.flop_features[10], self.flop_features[11], self.flop_features[12],
                                            self.flop_features[13], self.flop_features[14], self.flop_features[15], self.flop_features[16],
                                            self.flop_features[17], self.flop_features[18], self.flop_features[19], self.flop_features[20],
                                            self.flop_features[21], self.flop_features[22], self.flop_features[23], self.flop_features[24],
                                            self.flop_features[25], self.flop_features[26], self.flop_features[27], self.flop_features[28],
                                            self.flop_features[29], self.flop_features[30], self.flop_features[31], self.flop_features[31]]
                        flop_model_inputs.append(flop_model_input)
                return flop_model_inputs # different "inputs" for decision making


    def mkRiverModelInput(self):
        print("mkRiverModelInput called ...")
        with self.dec_lock:
            decision = self.decision
        with self.potheight_lock:     
            to_call = self.to_call   
        if decision == "fold":
            if to_call > 0.0:
                return # no need to write to table, when folding.  
            else:
                decision_temp = 0.0 # checking when there is nothing to call                                
        elif decision == "call":
            if to_call >= 1.0:
                decision_temp = 1.0    
            else:
                decision_temp = 0.0                            
        elif decision == "raise1":
            if to_call >= 1.0:
                decision_temp = 2.0    
            else:
                decision_temp = 0.25
        elif decision == "2raise2":
            if to_call >= 1.0:
                decision_temp = 2.0    
            else:
                decision_temp = 0.5
        elif decision == "3raise3":
            if to_call >= 1.0:
                decision_temp = 2.0    
            else:
                decision_temp = 0.75
        elif decision == "4raise4":
            if to_call >= 1.0:
                decision_temp = 2.0    
            else:
                decision_temp = 1.0       
        elif decision == "5raise5":
            decision_temp = 2.0  
        with self.mod_writing_lock:
            if not self.made_river_model_input:
                self.made_river_model_input = True
            # print("\nshould save something for river model data now ... \n")
            with self.mk_comte_carlo_decision_lock:
                with self.potheight_lock:                                
                    river_model_input = [self.probability_1_1, self.potheight, self.potheight_after_preflop, self.potheight_after_flop, # 9 + 14 = 23
                                         self.to_call, self.equity_flop, decision_temp, self.num_active_players, self.num_active_players_before_me,
                                            self.river_features[0], self.river_features[1], self.river_features[2], self.river_features[3], self.river_features[4],
                                            self.river_features[5], self.river_features[6], self.river_features[7], self.river_features[8], self.river_features[9], 
                                            self.river_features[10], self.river_features[11], self.river_features[12], self.river_features[13]
                                            ]
                    self.river_model_inputs.append(river_model_input)

    
    def mkRiverModelInputs_(self, decs): # decs could be [0.0, 0.25, 0.5, 0.75, 1.0, 2.0] (check possible) or [0.0, 1.0, 2.0] (when someone bet before me)
        river_model_inputs = []
        with self.mk_comte_carlo_decision_lock:
            with self.potheight_lock:
                for decision_temp in decs:
                    river_model_input = [self.probability_1_1, self.potheight, self.potheight_after_preflop, self.potheight_after_flop,
                                            self.to_call, self.equity_flop, decision_temp, self.num_active_players, self.num_active_players_before_me,
                                            self.river_features[0], self.river_features[1], self.river_features[2], self.river_features[3], self.river_features[4],
                                            self.river_features[5], self.river_features[6], self.river_features[7], self.river_features[8], self.river_features[9], 
                                            self.river_features[10], self.river_features[11], self.river_features[12], self.river_features[13]]
                    river_model_inputs.append(river_model_input)
                return river_model_inputs


    def mkTurnModelInput(self):
        print("mkTurnModelInput called ...")
        with self.dec_lock:
            decision = self.decision
        with self.potheight_lock:     
            to_call = self.to_call   
        if decision == "fold":
            if to_call > 0.0:
                return # no need to write to table, when folding.  
            else:
                decision_temp = 0.0 # checking when there is nothing to call                                
        elif decision == "call":
            if to_call >= 1.0:
                decision_temp = 1.0    
            else:
                decision_temp = 0.0                            
        elif decision == "raise1":
            if to_call >= 1.0:
                decision_temp = 2.0    
            else:
                decision_temp = 0.25
        elif decision == "2raise2":
            if to_call >= 1.0:
                decision_temp = 2.0    
            else:
                decision_temp = 0.5
        elif decision == "3raise3":
            if to_call >= 1.0:
                decision_temp = 2.0    
            else:
                decision_temp = 0.75
        elif decision == "4raise4":
            if to_call >= 1.0:
                decision_temp = 2.0    
            else:
                decision_temp = 1.0       
        elif decision == "5raise5":
            decision_temp = 2.0  
        with self.mod_writing_lock:
            if not self.made_turn_model_input:
                self.made_turn_model_input = True
            # print("\nshould save something for turn model data now ... \n")
            with self.mk_comte_carlo_decision_lock:
                with self.potheight_lock:# 11 + 15 = 26 features total for turn model input       
                    turn_model_input = [self.probability_1_1, self.potheight, self.potheight_after_preflop, self.potheight_after_flop, self.potheight_after_river,
                                            self.to_call, self.equity_flop, self.equity_river, decision_temp, self.num_active_players, self.num_active_players_before_me,
                                            self.turn_features[0], self.turn_features[1], self.turn_features[2], self.turn_features[3], self.turn_features[4],
                                            self.turn_features[5], self.turn_features[6], self.turn_features[7], self.turn_features[8], self.turn_features[9], 
                                            self.turn_features[10], self.turn_features[11], self.turn_features[12], self.turn_features[13], self.turn_features[14]
                                            ]
                    self.turn_model_inputs.append(turn_model_input)


    def mkTurnModelInputs_(self, decs): # decs could be [0.0, 0.25, 0.5, 0.75, 1.0, 2.0] (check possible) or [0.0, 1.0, 2.0] (when someone bet before me)
        turn_model_inputs = []
        with self.mod_writing_lock:
            with self.mk_comte_carlo_decision_lock:
                with self.potheight_lock:
                    for decision_temp in decs:
                        turn_model_input = [self.probability_1_1, self.potheight, self.potheight_after_preflop, self.potheight_after_flop, self.potheight_after_river,
                                                self.to_call, self.equity_flop, self.equity_river, decision_temp, self.num_active_players, self.num_active_players_before_me,
                                                self.turn_features[0], self.turn_features[1], self.turn_features[2], self.turn_features[3], self.turn_features[4],
                                                self.turn_features[5], self.turn_features[6], self.turn_features[7], self.turn_features[8], self.turn_features[9], 
                                                self.turn_features[10], self.turn_features[11], self.turn_features[12], self.turn_features[13], self.turn_features[14]
                                                ]
                        turn_model_inputs.append(turn_model_input)
                    return turn_model_inputs


    def mkModelOutput(self): # #read , compare new and old money here (after reading cards) , write down win or lose for ai-models
        print("mkModelOutput called ...")
        with self.mod_writing_lock:
            self.made_model_output = True
            with self.lock:    
                diff = self.own_money - self.own_money_before_last_preflop
                if diff >= 60.0 :
                    print("\nI think we just won extremely hard\n")
                    self.model_output = 2.0
                    return            
                elif diff <= -60.0 :
                    print("\nI think we just lost extremely hard\n")
                    self.model_output = -2.0
                    return  
                else:
                    self.model_output = diff / 30      
                    return             
                # if self.own_money_before_last_preflop < (self.own_money-13.0): # move around this number (-10 initially)
                #     print("\nI think we just won very hard\n")
                #     self.model_output = 3
                #     return   
                # elif self.own_money_before_last_preflop < (self.own_money-7.0): # move around this number (-10 initially)
                #     print("\nI think we just won hard\n")
                #     self.model_output = 2
                #     return    
                # elif self.own_money_before_last_preflop > (self.own_money+8.0): # move around this number (+6.0 initially) (maybe set this to seven later?)
                #     print("\nI think we just lost very hard\n")
                #     self.model_output = -3
                #     return                            
                # elif self.own_money_before_last_preflop > (self.own_money+4.0): # move around this number (+6.0 initially) (maybe set this to seven later?)
                #     print("\nI think we just lost hard\n")
                #     self.model_output = -2
                #     return                     
                # elif self.own_money_before_last_preflop > (self.own_money+2.5): # move around this number (+2.5 initially)
                #     print("\nI think we just lost\n")
                #     self.model_output = -1
                #     return
                # elif self.own_money_before_last_preflop < (self.own_money-1.0): # move around this number (-1.0 initially)
                #     print("\nI think we just won\n")
                #     self.model_output = 1
                #     return
                # else:
                #     print("\nmodel output 0\n")
                #     self.model_output = 0
                #     return
                

    def mkModelOutputAllInHandled(self): #read , compare new and old money here (after reading cards) , write down win or lose for ai-models
        print("I think we just lost")
        with self.mod_writing_lock:
            self.made_model_output   = True
            with self.lock:
                self.model_output = -self.own_money_before_last_preflop/30.0
                return


    def writeToCSVs(self): # todo: update
        print("writeToCSVs called ...")
        with self.mod_writing_lock:    
            if not self.wrote_to_csv_s:    
                print("writing to csv's ...")     
                self.wrote_to_csv_s = True                          
                if self.made_turn_model_input:
                    for turn_model_input in self.turn_model_inputs:
                        with open('csv_s/turnModel.csv','a', newline='') as fd:
                            writer = csv.writer(fd, delimiter=";")
                            print("\nliterally writing to turn csv RIGHT NOW !!!!!!!!!!!!\n")
                            writer.writerow([str(turn_model_input[0]), str(turn_model_input[1]), str(turn_model_input[2]), str(turn_model_input[3]), str(turn_model_input[4]), str(turn_model_input[5]), str(turn_model_input[6]), str(turn_model_input[7]), str(turn_model_input[8]), str(turn_model_input[9]), str(turn_model_input[10]), str(turn_model_input[11]), str(turn_model_input[12]), str(turn_model_input[13]), str(turn_model_input[14]), str(turn_model_input[15]), str(turn_model_input[16]), str(turn_model_input[17]),str(turn_model_input[18]),str(turn_model_input[19]),str(turn_model_input[20]),str(turn_model_input[21]),str(turn_model_input[22]),str(turn_model_input[23]),str(turn_model_input[24]),str(turn_model_input[25]), self.model_output])                 
                if self.made_river_model_input:
                    for river_model_input in self.river_model_inputs:    
                        with open('csv_s/riverModel.csv','a', newline='') as fd:
                            writer = csv.writer(fd, delimiter=";")
                            print("\nliterally writing to river csv RIGHT NOW !!!!!!!!!!!!\n")
                            writer.writerow([str(river_model_input[0]), str(river_model_input[1]), str(river_model_input[2]), str(river_model_input[3]), str(river_model_input[4]), str(river_model_input[5]), str(river_model_input[6]), str(river_model_input[7]), str(river_model_input[8]), str(river_model_input[9]), str(river_model_input[10]), str(river_model_input[11]), str(river_model_input[12]), str(river_model_input[13]), str(river_model_input[14]), str(river_model_input[15]), str(river_model_input[16]),str(river_model_input[17]),str(river_model_input[18]),str(river_model_input[19]),str(river_model_input[20]),str(river_model_input[21]),str(river_model_input[22]), self.model_output])                 
                if self.made_flop_model_input:
                    for flop_model_input in self.flop_model_inputs:
                        with open('csv_s/flopModel.csv','a', newline='') as fd:
                            writer = csv.writer(fd, delimiter=";")
                            print("\nliterally writing to flop csv RIGHT NOW !!!!!!!!!!!!\n")
                            writer.writerow([str(flop_model_input[0]), str(flop_model_input[1]), str(flop_model_input[2]), str(flop_model_input[3]), str(flop_model_input[4]), str(flop_model_input[5]), str(flop_model_input[6]), str(flop_model_input[7]), str(flop_model_input[8]), str(flop_model_input[9]), str(flop_model_input[10]), str(flop_model_input[11]), str(flop_model_input[12]), str(flop_model_input[13]), str(flop_model_input[14]), str(flop_model_input[15]), str(flop_model_input[16]), str(flop_model_input[17]), str(flop_model_input[18]), str(flop_model_input[19]), str(flop_model_input[20]), str(flop_model_input[21]), str(flop_model_input[22]), str(flop_model_input[23]), str(flop_model_input[24]), str(flop_model_input[25]), str(flop_model_input[26]), str(flop_model_input[27]), str(flop_model_input[28]), str(flop_model_input[29]), str(flop_model_input[30]), str(flop_model_input[31]), str(flop_model_input[32]), str(flop_model_input[33]), str(flop_model_input[34]), str(flop_model_input[35]), str(flop_model_input[36]), str(flop_model_input[37]), str(flop_model_input[38]), self.model_output])                 


    def resetValues(self): # preflop after reading cards ( when it's definitely new round )
        with self.potheight_lock:
            self.potheight_after_preflop = -1
            self.potheight_after_flop = -1   
            self.potheight_after_river = -1         
        with self.mk_comte_carlo_decision_lock:
            self.probability_1_1 = -1
            self.equity_flop = -1
            self.equity_river = -1
            self.flop_features = np.zeros(32)
            self.river_features = np.zeros(14)
            self.turn_features = np.zeros(15)
        with self.mod_writing_lock:
            if self.made_turn_model_input:
                self.made_turn_model_input = False 
                self.turn_model_inputs = []
            if self.made_river_model_input:
                self.made_turn_model_input = False 
                self.river_model_inputs = []
            if self.made_flop_model_input:
                self.made_flop_model_input = False 
                self.flop_model_inputs = []                
            self.made_model_output = False   
            self.wrote_to_csv_s = False  
        with self.cards_lock:
            if self.cards_open:
                self.cards_open = False            
            self.deck_card_1 = "nn"
            self.deck_card_2 = "nn"
            self.deck_card_3 = "nn"
            self.deck_card_4 = "nn"
            self.deck_card_5 = "nn"    
        with self.lock:
            self.own_money_before_last_preflop = self.own_money       
        with self.confidence_lock:
            self.confidence = self.slider.doubleValue()
        

    def makeAIDecision_(self, outputs): # make decision based on model outputs

        
        # outputs from model prediction
        with self.confidence_lock:
            confidence = self.confidence    
        print(f"Confidence: {confidence}")
        for output in outputs:
            # print(f"Model output: {output}")
            output = output + (0.175 * confidence) 
            # print(f"Adjusted Model output: {output}")
        if len(outputs) == 2:
            print("someone bet ... no check possible")
            print() 
            print("call equity before confidence: "+str(outputs[0]))
            print("bet equity before confidence: "+str(outputs[1]))    
            print()        
            for output in outputs:
                output = output + (0.175 * confidence) 
            call_equity = outputs[0]
            bet_equity = outputs[1]
            print("call equity: "+str(call_equity))
            print("bet equity: "+str(bet_equity))
            if bet_equity - call_equity > 0.0765:
                print("bet equity significantly higher than call equity")
                if call_equity > 0.215:
                    print("call equity good enough to raise")
                    return "raise1" # actual raise to double of what's to-call
                else:
                    if bet_equity > 0.25:
                        print("this scenario is very unlikely but ok")
                        return "raise1"
                    else:
                        if call_equity > -0.015: # fixing folding too much issue, but actually this is sus (too low value)
                            print("call equity decent enough to call")
                            return "call"
                        else:
                            print("call equity too low to call")
                            return "fold"
            else:
                if call_equity - bet_equity > 0.075:
                    print("bet equity lower than call equity")
                    if call_equity < -0.015:
                        print("call equity too low to call")
                        return "fold"
                    else:
                        print("call equity decent enough to call")
                        return "call"
                else:
                    print("call equity and bet equity similar")
                    if call_equity > -0.0165:
                        return "call"
                    else:
                        print("call equity too low to call")
                        return "fold"
        else:
            print("check was possible")
            check_equity = outputs[0]
            raise1_equity = outputs[1]
            raise2_equity = outputs[2]
            raise3_equity = outputs[3]
            raise4_equity = outputs[4]
            raise5_equity = outputs[5]
            print("check equity: "+str(check_equity))
            print("raise1 equity: "+str(raise1_equity))
            print("raise2 equity: "+str(raise2_equity))
            print("raise3 equity: "+str(raise3_equity))
            print("raise4 equity: "+str(raise4_equity))   
            print("raise5 equity: "+str(raise5_equity))

            if random.randrange(2) == 0:
                print("random decision mode")
                if random.randrange(2) == 0 and raise3_equity > 0.0: # swap these maybe later
                    return "3raise3"
                elif random.randrange(2) == 0 and raise2_equity > 0.0: # swap these maybe later
                    return "2raise2"
                elif random.randrange(2) == 0 and raise4_equity > 0.0: # swap these maybe later
                    return "4raise4"
                elif random.randrange(2) == 0 and raise5_equity > 0.0: # swap these maybe later
                    return "5raise5"
                elif raise1_equity > 0.0: # swap these maybe later
                    return "raise1"
                else:
                    return "fold"           
            else:
                if raise5_equity - raise1_equity > 0.76 :
                    return "5raise5"
                else:
                    if raise4_equity - raise1_equity > 0.57 :
                        return "4raise4"
                    else:
                        if raise3_equity - raise1_equity > 0.35:
                            return "3raise3"
                        else:
                            if raise2_equity - raise1_equity > 0.17:
                                return "2raise2"
                            else:
                                print("else ...")
                                if raise5_equity> 0.35:
                                    return "5raise5"
                                elif raise4_equity> 0.25:
                                    return "4raise4"                           
                                elif raise3_equity> 0.15:
                                    return "3raise3"                           
                                elif raise2_equity> 0.11:
                                    return "2raise2"                        
                                elif raise1_equity> 0.0015:
                                    return "raise1"
                                else:
                                    return "fold"


    def makeDecisionPreflop(self):
        print("makeDecisionPreflop called ...")
        with self.potheight_lock:
            pot_height = self.potheight
            to_call = self.to_call
        with self.own_cards_lock:
            own_card_left = self.own_card_left
            own_card_right = self.own_card_right
        print('own cards in preflop: '+own_card_left+" "+own_card_right)
        decision = "fold" 
        left_above = own_card_left.startswith("A") or own_card_left.startswith("K") or own_card_left.startswith("Q") or own_card_left.startswith("J") or own_card_left.startswith("T") or own_card_left.startswith("9") or own_card_left.startswith("8") or own_card_left.startswith("7")
        rigth_above = own_card_right.startswith("A") or own_card_right.startswith("K") or own_card_right.startswith("Q") or own_card_right.startswith("J") or own_card_right.startswith("T") or own_card_right.startswith("9") or own_card_right.startswith("8") or own_card_right.startswith("7")
        if left_above and rigth_above:
            print("debug : both seven or above")
            if to_call <= 2.5:
                decision = "call"
            if own_card_left[0] == own_card_right[0]: # suited
                print("debug : suited")
                if own_card_left.startswith("A") and own_card_right.startswith("A"):
                    decision = "3raise3"
                elif own_card_left.startswith("K") and own_card_right.startswith("K"):
                    if to_call <= 6.0: 
                        print("debug : both K")
                        decision = "3raise3"          
                    elif to_call <= 20.0: 
                        decision = "raise1"  
                    elif to_call <= 35.0:
                        decision = "call"                  
                elif own_card_left.startswith("Q") and own_card_right.startswith("Q"):
                    if to_call <= 1.5:
                        decision = "3raise3"
                    elif to_call <= 8.0: 
                        decision = "2raise2"
                    else:
                        decision = "call" 
                elif own_card_left.startswith("J") and own_card_right.startswith("J"):
                    if to_call <= 5.7:
                        decision = "raise1"      
                    else:
                        decision = "call"                                                                                                     
                elif own_card_left.startswith("T") and own_card_right.startswith("T"):
                    if to_call <= 3.67:
                        decision = "raise1" 
                    elif to_call <= 12.0:
                        decision = "call"
                elif own_card_left.startswith("9") and own_card_right.startswith("9"):
                    if to_call <= 11:
                        decision = "call" 
                elif own_card_left.startswith("8") and own_card_right.startswith("8"):
                    if to_call <= 8:
                        decision = "call"
                elif own_card_left.startswith("7") and own_card_right.startswith("7"):
                    if to_call <= 7:
                        decision = "call"                        
            elif own_card_left.startswith("A") or own_card_right.startswith("A"):# one is ace
                print("debug: one is ace")       
                if to_call <= 1.5:
                    print("debug : ace and something else, to_call very low")
                    print("funny lil raise here 2")
                    decision = "raise1" # funny move   
                elif to_call<=4.75:
                    decision = "call"
                elif to_call<=5.5 and pot_height>=8.5:
                    decision = "call"                      
                elif to_call<=7.5 and pot_height>=18.5:
                    decision = "call"                               
                if own_card_left.startswith("K") or own_card_right.startswith("K"): # ace,  king
                    print("debug : ace and king")
                    if to_call < 1.0:
                        print("funny lil raise here 3")
                        decision = "raise1"     
                    elif to_call < 7.5:
                        decision = "call"                                     
                else:                                   #                              
                    if own_card_left.startswith("Q") or own_card_right.startswith("Q"): #  ace # queen
                        print("debug : ace and queen")
                        if to_call <= 2.0:
                            print("funny lil raise here 4")
                            decision = "2raise2"
                        elif to_call <= 4.0: 
                            print("funny lil raise here 5")
                            decision = "raise1"
                        elif to_call <= 8.0: 
                            decision = "call" 
                    elif own_card_left.startswith("J") or own_card_right.startswith("J"): # ace # jack
                        print("debug : ace and jack")
                        if to_call <= 2.5:
                            print("funny lil raise here 6")
                            decision = "raise1"
                        elif to_call <= 4.9: 
                            decision = "call"
                    else:
                        if to_call <= 4.5:
                            decision = "call"                                           
                

            else: # no ace but 7 or higher                 
                if own_card_left.startswith("K") or own_card_right.startswith("K"):
                    print("debug : one is K")
                    if to_call <= 4.0: 
                        decision = "call"      
                    elif own_card_left.startswith("Q") or own_card_right.startswith("Q"): # K & Q
                        print("debug : K and Q")
                        if to_call<5.0:
                            decision = "call"                                
                        if to_call<15.0 and pot_height>=10.0:
                            decision = "call"          
                    elif own_card_left.startswith("J") or own_card_right.startswith("J"): # K & J
                        print("debug : K and J")
                        if to_call<4.0:
                            decision = "call"                                
                        if to_call<12.0 and pot_height>=8.0:
                            decision = "call"       
                    elif own_card_left.startswith("T") or own_card_right.startswith("T"): # K & T
                        print("debug : K and T")
                        if to_call<3.67:
                            decision = "call"                                
                        if to_call<12.0 and pot_height>=8.0:
                            decision = "call"                                                                                                                                                                              
                elif own_card_left.startswith("Q") and own_card_right.startswith("Q"):
                    print("both Q")
                    if to_call <= 1.5:
                        decision = "3raise3"
                    elif to_call <= 8.0: 
                        decision = "2raise2"
                    else:
                        decision = "call"
                elif own_card_left.startswith("Q") or own_card_right.startswith("Q"):
                    print("debug :one is Q")
                    if to_call <= 2.5: 
                        decision = "call"   
                    if own_card_left.startswith("J") or own_card_right.startswith("J"): # Q & J
                        print("debug : Q and J")
                        if to_call <= 5.0: 
                            decision = "call"   
                    if own_card_left.startswith("T") or own_card_right.startswith("T"): # Q & T
                        print("debug : Q and T")
                        if to_call <= 4.5: 
                            decision = "call"     
                elif own_card_left.startswith("J") and own_card_right.startswith("J"):
                    decision = "raise1"                                                                                                           
                elif own_card_left.startswith("J") or own_card_right.startswith("J"):
                    print("debug :one is J")
                    if to_call <= 2.5: 
                        decision = "call"
                    if own_card_left.startswith("T") or own_card_right.startswith("T"): # J & T
                        print("debug : J and T")
                        if to_call <= 4.5: 
                            decision = "call"                               
                elif own_card_left.startswith("T") and own_card_right.startswith("T"):
                    if to_call <= 10:
                        decision = "call"
                elif own_card_left.startswith("T") or own_card_right.startswith("T"):
                    if to_call <= 2.5:
                        decision = "call"                            
                elif own_card_left.startswith("9") and own_card_right.startswith("9"):
                    if to_call <= 9:
                        decision = "call"
                elif own_card_left.startswith("8") and own_card_right.startswith("8"):
                    if to_call <= 8:
                        decision = "call"
                elif own_card_left.startswith("7") and own_card_right.startswith("7"):
                    if to_call <= 7:
                        decision = "call"
                                         
        else:
            print("debug : one is six or under")
            if (own_card_left.startswith("A") or own_card_left.startswith("K") or own_card_left.startswith("Q") or own_card_left.startswith("J") or own_card_left.startswith("T") or own_card_left.startswith("9") or own_card_left.startswith("8") or own_card_left.startswith("7") or own_card_left.startswith("6")) or (own_card_right.startswith("A") or own_card_right.startswith("K") or own_card_right.startswith("Q") or own_card_right.startswith("J") or own_card_right.startswith("T") or own_card_right.startswith("9") or own_card_right.startswith("8") or own_card_right.startswith("7") or own_card_right.startswith("6")):
                if to_call <= 2.0 and pot_height >= 6.5: # funny move maybe ?
                    decision = "call"
                elif to_call <= 1.0 and pot_height >= 3.5: # funny move maybe ?
                    decision = "call"
                elif own_card_left.startswith("A") or own_card_right.startswith("A"):
                    # decision = "call"
                    if to_call <= 4.6:
                        decision = "call"
                else: 
                    if own_card_left.startswith("K") or own_card_right.startswith("K"):
                        if to_call <= 4.0 and pot_height > 7.6: 
                            decision = "call"             
                        elif to_call <= 3.5: 
                            decision = "call"                                                      
                    elif own_card_left.startswith("Q") or own_card_right.startswith("Q"):
                        if to_call <= 3.0: 
                            decision = "call"
                    elif own_card_left.startswith("J") or own_card_right.startswith("J"):
                        if to_call <= 2.5: 
                            decision = "call"
            else:
                print("both cards six or under")
                if own_card_left.startswith("6") and own_card_right.startswith("6"):
                    if to_call <= 6.0:
                        decision = "call"  
                elif own_card_left.startswith("5") and own_card_right.startswith("5"):
                    if to_call <= 5.5:
                        decision = "call"
                elif own_card_left.startswith("4") and own_card_right.startswith("4"):
                    if to_call <= 6.0:
                        decision = "call"
                elif own_card_left.startswith("3") and own_card_right.startswith("3"):
                    if to_call <= 5.5:
                        decision = "call"
                elif own_card_left.startswith("2") and own_card_right.startswith("2"):
                    if to_call <= 4.5:
                        decision = "call"                                                                                
        return decision
    

    def calculateFlopEquity(self):
        print("calculateFlopEquity called ...")
        with self.own_cards_lock:
            own_card_left = self.own_card_left
            own_card_right = self.own_card_right    
        with self.cards_lock:
            deck_card_1 = self.deck_card_1
            deck_card_2 = self.deck_card_2 
            deck_card_3 = self.deck_card_3  
        with self.mk_comte_carlo_decision_lock:
            print('own cards in flop: '+own_card_left+" "+own_card_right +' | deck cards: '+deck_card_1+" "+deck_card_2+" "+deck_card_3)
            try:
                self.flop_features = extract_flop_features([own_card_left, own_card_right], [deck_card_1, deck_card_2, deck_card_3])
            except Exception as e:
                print(e)
                exit(1)
            print("debug - extracted flop features: "+str(self.flop_features))
            self.equity_flop = flop_equity_model_predict(self.flop_features)
            print("debug - calculated flop equity: "+str(self.equity_flop))


    def makeDecisionFlop(self):

        print("makeDecisionFlop called ...")

        # for now no AI-decision-making
        with self.dec_lock:
            decision = self.decision

        print("flop decision was: "+decision)

        if decision == "None_yet":
            time.sleep(1.0)
            with self.dec_lock:
                decision = self.decision    
            print("flop decision was: "+decision)    
            if decision == "None_yet":
                return "fold"
            else:
                print("decision was made while waiting: "+decision)
                return decision
        else:
            print("decision already made before flop model prediction, maybe preflop decision, maybe something else ... "+decision)
            return decision
                            
        with self.potheight_lock:
            to_call = self.to_call      
        if to_call > 0.0:
            temp_Inputs = self.mkFlopModelInputs_([1.0, 2.0])
            # print("debug - flop model inputs: "+str(temp_Inputs))
            outputs = flop_model_predict_multiple(temp_Inputs)
        else:
            temp_Inputs = self.mkFlopModelInputs_([0.0, 0.25, 0.5, 0.75, 1.0, 2.0])
            # print("debug - flop model inputs: "+str(temp_Inputs))
            outputs = flop_model_predict_multiple(temp_Inputs)
        with self.mk_comte_carlo_decision_lock:   
            print("self.equity_flop: "+str(self.equity_flop))  
            if self.equity_flop > 0.40: # need to adjust confidence, while still learning ...
                with self.confidence_lock:
                    self.confidence += 0.37                
            if self.equity_flop > 0.45: # need to adjust confidence, while still learning ...
                with self.confidence_lock:
                    self.confidence += 0.47                 
            if self.equity_flop > 0.5: # need to adjust confidence, while still learning ...
                with self.confidence_lock:
                    self.confidence += 0.7                
            if self.equity_flop > 0.6: # need to adjust confidence, while still learning ...
                with self.confidence_lock:
                    self.confidence += 0.7                 
            if self.equity_flop > 0.7: # need to adjust confidence, while still learning ...
                with self.confidence_lock:
                    self.confidence += 0.7                          
            if self.equity_flop > 0.8: # need to adjust confidence, while still learning ...
                with self.confidence_lock:
                    self.confidence += 0.7    
            if self.equity_flop > 0.825: # need to adjust confidence, while still learning ...
                with self.confidence_lock:
                    self.confidence += 0.7                              
            if self.equity_flop > 0.85: # need to adjust confidence, while still learning ...
                with self.confidence_lock:
                    self.confidence += 0.7               
            if self.equity_flop > 0.86: # need to adjust confidence, while still learning ...
                with self.confidence_lock:
                    self.confidence += 0.7             
            if self.equity_flop > 0.875: # need to adjust confidence, while still learning ...
                with self.confidence_lock:
                    self.confidence += 0.7                                                    
            if self.equity_flop > 0.9: # need to adjust confidence, while still learning ...
                with self.confidence_lock:
                    self.confidence += 0.7    
            if self.equity_flop > 0.91: # need to adjust confidence, while still learning ...
                with self.confidence_lock:
                    self.confidence += 0.7                       
            if self.equity_flop > 0.92: # need to adjust confidence, while still learning ...
                with self.confidence_lock:
                    self.confidence += 0.7                       
            if self.equity_flop > 0.93: # need to adjust confidence, while still learning ...
                with self.confidence_lock:
                    self.confidence += 0.7                       
            if self.equity_flop > 0.94: # need to adjust confidence, while still learning ...
                with self.confidence_lock:
                    self.confidence += 0.7                               
            if self.equity_flop > 0.95: # need to adjust confidence, while still learning ...
                with self.confidence_lock:
                    self.confidence += 0.7                                      
            if self.equity_flop > 0.96: # need to adjust confidence, while still learning ...
                with self.confidence_lock:
                    self.confidence += 0.7             
            if self.equity_flop > 0.97: # need to adjust confidence, while still learning ...
                with self.confidence_lock:
                    self.confidence += 0.7                  
            if self.equity_flop > 0.98: # need to adjust confidence, while still learning ...
                with self.confidence_lock:
                    self.confidence += 1.7      
            if self.equity_flop > 0.99: # need to adjust confidence, while still learning ...
                with self.confidence_lock:
                    self.confidence += 7.0                                                                                        
        decision = self.makeAIDecision_(outputs)
        # with self.mk_comte_carlo_decision_lock:
        #     set_1_1 = self.equity_flop
        # with self.potheight_lock:
        #     pot_height = self.potheight

        if decision != "fold" and to_call > 0.0: # this part increases confidenc after we bet something , remove this later
            with self.confidence_lock:
                self.confidence += 1.2
                if to_call > 5.0:
                    self.confidence += 1.5    
                elif decision.startswith("4") or decision.startswith("5"):
                    self.confidence += 1.5                                    
        return decision 
        decision = "fold"
        if set_1_1 > 0.89:
            if pot_height <= 8.0:
                decision = "raise1"
            elif pot_height < 18.0:
                decision = "3raise3"
            else:
                decision = "call"
        elif set_1_1 > 0.73:
            if to_call <= 5:
                if pot_height <= 8.0:
                    decision = "raise1"
                elif pot_height < 18.0 :
                    decision = "2raise2"
                else:
                    decision = "call"
            else:
                if to_call <= 15.0: #
                    decision = "call"
                # else:
                #     decision = "fold"
        elif set_1_1 > 0.7:   
            if to_call <= 4:
                if pot_height <= 9.0:
                    decision = "raise1"
                elif pot_height < 18.0 :
                    decision = "2raise2"
                else:
                    decision = "call"
            else:

                if pot_height < 20.0:
                    decision = "call"   
                elif to_call <= 14.0: #
                    decision = "call"                                   
        elif set_1_1 > 0.65:
            if to_call <= 3.5:
                if pot_height <= 8.0:
                    decision = "raise1"
                elif pot_height < 24.0 :
                    decision = "call"
                    
                else:
                    decision = "fold"
            else:
                if to_call < 12.5:
                    decision = "call"                 
        elif set_1_1 > 0.61:
            if to_call <= 6.7:
                if pot_height < 8.5:
                    decision = "raise1"
                elif pot_height >= 6: #
                    decision = "call"   
        elif set_1_1 > 0.57:
            if to_call <= 2.0:
                decision = "raise1"
            elif to_call <= 6.0:
                decision = "call"        
        elif set_1_1 > 0.47 and pot_height < 7 and to_call < 1.0:
            decision = "raise1"                    
        elif set_1_1 > 0.45 and pot_height >= 10 and to_call <= 3.5:
            decision = "call"                 
        elif set_1_1 > 0.37 and pot_height < 4 and to_call <= 2.1:
            decision = "call"   # used to raise1 here and it worked until like 20 hands and they found out ... .
        return decision   


    def makeDecisionRiver(self):
        print("makeDecisionRiver called")

        # for now no AI-decision-making
        with self.dec_lock:
            decision = self.decision
        print("preflop decision was: "+decision)
        if decision == "None_yet":
            time.sleep(1.0)
            with self.dec_lock:
                decision = self.decision    
            print("preflop decision was: "+decision)        
            if decision == "None_yet":
                return "fold"
            else:
                return decision
        else:
            return decision

        with self.mk_comte_carlo_decision_lock:
            set_1_1 = self.probability_1_1
        print("set_1_1 at river-time: "+str(set_1_1))
        with self.potheight_lock:
            pot_height = self.potheight            
        with self.potheight_lock:
            to_call = self.to_call    
        if self.equity_flop > 0.6: # need to adjust confidence, while still learning ...
            with self.confidence_lock:
                self.confidence += 1.7              
        if set_1_1 > 0.7: # need to adjust confidence, while still learning ...
            with self.confidence_lock:
                self.confidence += 2.7               
        if set_1_1 > 0.8: # need to adjust confidence, while still learning ...
            with self.confidence_lock:
                self.confidence += 2.7   
        if set_1_1 > 0.9: # need to adjust confidence, while still learning ...
            with self.confidence_lock:
                self.confidence += 3.5       
        if set_1_1 > 0.95: # need to adjust confidence, while still learning ...
            with self.confidence_lock:
                self.confidence += 3.5                        
        # print("makeDecisionRiver probability_1_1: "+str(set_1_1))
        difference_tocall_n_potheight = to_call/pot_height
        if to_call > 0.0:
            outputs = river_model_predict_multiple(self.mkRiverModelInputs_([1.0, 2.0]))
        else:
            outputs = river_model_predict_multiple(self.mkRiverModelInputs_([0.0, 0.25, 0.5, 0.75, 1.0, 2.0]))        
        decision = self.makeAIDecision_(outputs)
        # with self.mk_comte_carlo_decision_lock:
        #     set_1_1 = self.equity_flop
        # with self.potheight_lock:
        #     pot_height = self.potheight
            
        if decision != "fold" and to_call > 0.0: # this part increases confidenc after we bet something , remove this later
            with self.confidence_lock:
                self.confidence += 1.2
                if to_call > 5.0:
                    self.confidence += 1.5
                elif decision.startswith("4") or decision.startswith("5"):
                    self.confidence += 0.5                    
        return decision 
        # if set_1_1 > 0.53 and pot_height >= 5 and to_call < 1:
        #     decision = "raise1"        
        # if set_1_1 > 0.675 and to_call > 3:
        #     decision = "call"
        # else:
        #     if set_1_1 > .65 and difference_tocall_n_potheight<0.4:
        #         if pot_height >= 7 and to_call <= 5:
        #             decision = "call"
        #         if pot_height < 7 and to_call <= 3:
        #             decision = "raise1"
        #     elif set_1_1 > .70 and  difference_tocall_n_potheight<0.35:
        #         decision = "call"
        #     elif set_1_1 > .70 and to_call<=15:
        #         decision = "call"     
        #     elif set_1_1 > .70 and to_call<=2 and pot_height <= 4:
        #         decision = "raise1"                     
        #     if set_1_1 > .80 and to_call<=2:
        #         decision = "raise1"                                       
        #     elif set_1_1 > .80 and to_call<10:
        #         decision = "4raise4"   
        #     elif set_1_1 > .80 and to_call<=20:
        #         decision = "call"     
        #     elif set_1_1 > .80 and difference_tocall_n_potheight<=0.3:
        #         decision = "call"                   
        #     if set_1_1 > .85 and to_call<80:
        #         decision = "3raise3"                          
              
            # else:
            #     if set_1_1 > 0.71:
            #         decision = "call"
            #     else:
            #         decision = "fold"
    

    def makeDecisionTurn(self):
        print("makeDecisionTurn called")


        # for now no AI-decision-making
        with self.dec_lock:
            decision = self.decision
        print("preflop decision was: "+decision)
        if decision == "None_yet":
            time.sleep(1.0)
            with self.dec_lock:
                decision = self.decision  
            print("preflop decision was: "+decision)          
            if decision == "None_yet":
                return "fold"
            else:
                return decision
        else:
            return decision


        with self.potheight_lock:
            to_call = self.to_call
        with self.mk_comte_carlo_decision_lock:
            set_1_1 = self.probability_1_1
        print("set_1_1 at turn-time: "+str(set_1_1))            
        # with self.potheight_lock:
        #     pot_height = self.potheight        
        if to_call > 0.0:
            outputs = turn_model_predict_multiple(self.mkTurnModelInputs_([1.0, 2.0]))
        else:
            outputs = turn_model_predict_multiple(self.mkTurnModelInputs_([0.0, 0.25, 0.5, 0.75, 1.0, 2.0]))
        if set_1_1 > 0.7: # need to adjust confidence, while still learning ...
            with self.confidence_lock:
                self.confidence += 2.5                
        if set_1_1 > 0.8: # need to adjust confidence, while still learning ...
            with self.confidence_lock:
                self.confidence += 2.78                
        if set_1_1 > 0.9: # need to adjust confidence, while still learning ...
            with self.confidence_lock:
                self.confidence += 3.5       
        if set_1_1 > 0.95: # need to adjust confidence, while still learning ...
            with self.confidence_lock:
                self.confidence += 3.5                 
        return self.makeAIDecision_(outputs)
    

    def makeDecision(self):  # up confidence according to pot_height when calling (the bet)
        print("makeDecision called")
        set_1_1 = -1
        if self.deck_card_1 == "nn":  # that means its preflop
            with self.dec_lock:
                if self.decision == "None_yet":
                    self.decision = self.makeDecisionPreflop()
                return
        else:
            print("debug - deck cards read in makeDecision: "+self.deck_card_1+" "+self.deck_card_2+" "+self.deck_card_3+" "+self.deck_card_4+" "+self.deck_card_5)
            if self.deck_card_2 == "nn" or self.deck_card_3 == "nn":
                print("!!!!!!!!!!!!!!! FIRST DECK CARD WAS READ ; AT LEAST ONE OTHER NOT, exiting ...")
                exit()
            if self.deck_card_4 == "nn": # that means flop      
                print("# that means flop    ")
                with self.dec_lock:
                    decision = self.decision
                if decision == "None_yet":
                    print("debug - decision still None_yet after waiting, now making flop decision ...")
                    time.sleep(0.75)
                    model_dec = self.makeDecisionFlop()
                    with self.dec_lock:
                        if self.decision == "None_yet":
                            self.decision = model_dec
                try:
                    self.mkFlopModelInput()
                except Exception as e:
                    print("error 104")
                    print(e)
                    exit()
                return
            if self.deck_card_5 == "nn": # that means river
                print("# that means river    ")
                with self.mk_comte_carlo_decision_lock:
                    set_1_1 = self.probability_1_1
                    self.equity_river = set_1_1                    
                if set_1_1 == -1:
                    pass
                else:
                    with self.dec_lock:
                        decision = self.decision
                    if decision == "None_yet":
                        time.sleep(0.75)
                        print("I was here river dec making 3")
                        model_dec = self.makeDecisionRiver()
                        with self.dec_lock:
                            decision = self.decision
                        if decision == "None_yet":
                            self.decision = model_dec
                    self.mkRiverModelInput()
                    return
                time.sleep(0.35) 
                with self.mk_comte_carlo_decision_lock:
                    set_1_1 = self.probability_1_1
                if set_1_1 == -1:
                    pass
                else:
                    with self.dec_lock:
                        decision = self.decision
                    if decision == "None_yet":
                        time.sleep(0.5)
                        model_dec = self.makeDecisionRiver()
                        with self.dec_lock:
                            decision = self.decision
                        if decision == "None_yet":
                            self.decision = model_dec
                    self.mkRiverModelInput()
                    return
                time.sleep(0.35) 
                with self.mk_comte_carlo_decision_lock:
                    set_1_1 = self.probability_1_1
                if set_1_1 == -1:
                    pass
                else:
                    with self.dec_lock:
                        decision = self.decision
                    if decision == "None_yet":
                        time.sleep(0.5)
                        model_dec = self.makeDecisionRiver()
                        with self.dec_lock:
                            decision = self.decision
                        if decision == "None_yet":
                            self.decision = model_dec
                    self.mkRiverModelInput()
                    return       
                time.sleep(0.35) 
                with self.mk_comte_carlo_decision_lock:
                    set_1_1 = self.probability_1_1
                if set_1_1 == -1:
                    pass
                else:
                    with self.dec_lock:
                        decision = self.decision
                    if decision == "None_yet":
                        model_dec = self.makeDecisionRiver()
                        with self.dec_lock:
                            decision = self.decision
                        if decision == "None_yet":
                            self.decision = model_dec
                    self.mkRiverModelInput()
                    return
                time.sleep(0.35) 
                with self.mk_comte_carlo_decision_lock:
                    set_1_1 = self.probability_1_1
                if set_1_1 == -1:
                    pass
                else:
                    with self.dec_lock:
                        decision = self.decision
                    if decision == "None_yet":
                        model_dec = self.makeDecisionRiver()
                        with self.dec_lock:
                            decision = self.decision
                        if decision == "None_yet":
                            self.decision = model_dec
                    self.mkRiverModelInput()
                    return                
                time.sleep(0.35) 
                with self.mk_comte_carlo_decision_lock:
                    set_1_1 = self.probability_1_1
                if set_1_1 == -1:
                    pass
                else:
                    with self.dec_lock:
                        decision = self.decision
                    if decision == "None_yet":
                        model_dec = self.makeDecisionRiver()
                        with self.dec_lock:
                            decision = self.decision
                        if decision == "None_yet":
                            self.decision = model_dec
                    self.mkRiverModelInput()
                    return    
                time.sleep(0.35) 
                with self.mk_comte_carlo_decision_lock:
                    set_1_1 = self.probability_1_1
                if set_1_1 == -1:
                    pass
                else:
                    with self.dec_lock:
                        decision = self.decision
                    if decision == "None_yet":
                        model_dec = self.makeDecisionRiver()
                        with self.dec_lock:
                            decision = self.decision
                        if decision == "None_yet":
                            self.decision = model_dec
                    self.mkRiverModelInput()
                    return                
                time.sleep(0.35) 
                with self.mk_comte_carlo_decision_lock:
                    set_1_1 = self.probability_1_1
                if set_1_1 == -1:
                    pass
                else:
                    with self.dec_lock:
                        decision = self.decision
                    if decision == "None_yet":
                        model_dec = self.makeDecisionRiver()
                        with self.dec_lock:
                            decision = self.decision
                        if decision == "None_yet":
                            self.decision = model_dec
                    self.mkRiverModelInput()
                    return                            
                time.sleep(0.35) 
                with self.mk_comte_carlo_decision_lock:
                    set_1_1 = self.probability_1_1
                if set_1_1 == -1:
                    pass
                else:
                    with self.dec_lock:
                        decision = self.decision
                    if decision == "None_yet":
                        model_dec = self.makeDecisionRiver()
                        with self.dec_lock:
                            decision = self.decision
                        if decision == "None_yet":
                            self.decision = model_dec
                    self.mkRiverModelInput()
                    return
                time.sleep(0.35)                     
                with self.mk_comte_carlo_decision_lock:
                    set_1_1 = self.probability_1_1
                if set_1_1 == -1:
                    print("!!!!!!!!!!!!!!!!!!!!!! exit river no-time")
                    exit()
                else:
                    with self.dec_lock:
                        if self.decision == "None_yet":
                            self.decision = self.makeDecisionRiver()  
                        self.mkRiverModelInput()
                        return    
            if self.deck_card_5 != "nn": # that means turn
                with self.mk_comte_carlo_decision_lock:
                    set_1_1 = self.probability_1_1
                if set_1_1 == -1:
                    pass
                else:
                    with self.dec_lock:
                        decision = self.decision
                    if decision == "None_yet":
                        time.sleep(0.75)
                        model_dec = self.makeDecisionTurn()
                        with self.dec_lock:
                            decision = self.decision
                        if decision == "None_yet":
                            self.decision = model_dec
                    self.mkTurnModelInput()
                    return
                time.sleep(0.7) 
                with self.mk_comte_carlo_decision_lock:
                    set_1_1 = self.probability_1_1
                if set_1_1 == -1:
                    pass
                else:
                    with self.dec_lock:
                        decision = self.decision
                    if decision == "None_yet":
                        time.sleep(0.5)
                        model_dec = self.makeDecisionTurn()
                        with self.dec_lock:
                            decision = self.decision
                        if decision == "None_yet":
                            self.decision = model_dec
                    self.mkTurnModelInput()
                    return
                time.sleep(0.7) 
                with self.mk_comte_carlo_decision_lock:
                    set_1_1 = self.probability_1_1
                if set_1_1 == -1:
                    pass
                else:
                    with self.dec_lock:
                        decision = self.decision
                    if decision == "None_yet":
                        time.sleep(0.5)
                        model_dec = self.makeDecisionTurn()
                        with self.dec_lock:
                            decision = self.decision
                        if decision == "None_yet":
                            self.decision = model_dec
                    self.mkTurnModelInput()
                    return      
                time.sleep(0.7) 
                with self.mk_comte_carlo_decision_lock:
                    set_1_1 = self.probability_1_1
                if set_1_1 == -1:
                    pass
                else:
                    with self.dec_lock:
                        decision = self.decision
                    if decision == "None_yet":
                        time.sleep(0.5)
                        model_dec = self.makeDecisionTurn()
                        with self.dec_lock:
                            decision = self.decision
                        if decision == "None_yet":
                            self.decision = model_dec
                    self.mkTurnModelInput()
                    return
                time.sleep(0.7) 
                with self.mk_comte_carlo_decision_lock:
                    set_1_1 = self.probability_1_1
                if set_1_1 == -1:
                    print("!!!!!!!!!!!!!!!!!!!!!! exit turn no-time")
                    exit()
                else:
                    with self.dec_lock:
                        decision = self.decision
                    if decision == "None_yet":
                        model_dec = self.makeDecisionTurn()
                        with self.dec_lock:
                            decision = self.decision
                        if decision == "None_yet":
                            self.decision = model_dec
                    self.mkTurnModelInput()
                    return                 
    

    def sliderChanged_(self, sender):
        if self.confidence_lock.locked():
            return
        with self.confidence_lock:
            time.sleep(0.123)
            value = sender.doubleValue()
            self.confidence = value
        print(f"Slider-Wert: {value}")
        # time.sleep(0.05)



    def roundswap_(self, current_im=None):
        if not self.updateOwnMoney_(current_im=current_im):
            time.sleep(0.35)
            if not self.updateOwnMoney_(current_im=None):
                time.sleep(0.75)
                print("retrying reading own money at preflop")
                if not self.updateOwnMoney_(current_im=None):
                    time.sleep(0.35)
                    print("retrying reading own money at preflop")
                    if not self.updateOwnMoney_(current_im=None):
                        time.sleep(0.75)
                        print("retrying reading own money at preflop")
                        if not self.updateOwnMoney_(current_im=None):
                            time.sleep(0.35)
                            print("retrying reading own money at preflop")
                            if not self.updateOwnMoney_(current_im=None):
                                print("\nread own money failed at preflop - bad ! - !!!\n")                                  
                                exit()

        # model training
        with self.mod_writing_lock:
            made_output_temp =  self.made_model_output
        if not made_output_temp:
            self.mkModelOutput()
        # print("model output made")

        self.writeToCSVs()
        self.resetValues()


    def gameScreenshot_(self, userInfo): # time to cat logic in here

        with self.acting_lock:
            if self.time_to_act:
                print("time_to_act active during game screenshot 24")
                return
            else:
                self.time_to_act = True

        # with self.lock2:
        #     if self.busy_ticking:
        #         print("busy ticking")
        #         return # already in tick, reading player info

        self.mutex_screenshot.acquire()
        try:
            self.im = game_screenshot(save=False)
        except Exception as e:
            print(e)
            self.mutex_screenshot.release()
            with self.acting_lock:
                self.time_to_act = False
            return
        current_im = self.im
        self.mutex_screenshot.release()
        

        with self.lock:
            own_money = self.own_money
        if own_money == -1: # todo: save images when clicking for debugging
            print("\n all in ... \n")
            with self.valset_lock: # reset own money please
                self.values_set = False
            if handle_all_in(current_im):
                print("ALL IN HANDLED NICELY")
                self.mkModelOutputAllInHandled()
                self.writeToCSVs()
                time.sleep(4) # write loss to model here
                get_up_stand_up()
                pyautogui.click(x=1183, y=759)    
            with self.cards_lock:
                if self.cards_open:
                    self.cards_open = False
            with self.game_stage_lock:     
                if self.game_stage_current != "no_decision_to_be_made":
                    # print("no decision to be made")
                    self.game_stage_current = "no_decision_to_be_made"
            secs = time.time()
            # current_im.save(f"shmol_model_not_sure/all_in/all_in_{str(secs).split(".")[0]}.png")
            time.sleep(0.25)
            if not self.updateOwnMoney_(current_im=None):
                time.sleep(0.35)
                if not self.updateOwnMoney_(current_im=None):
                    time.sleep(0.35)
                    if not self.updateOwnMoney_(current_im=None):
                        time.sleep(0.35)
                        if not self.updateOwnMoney_(current_im=None):
                            print("\nread own money failed at all in\n")        
            with self.acting_lock:
                self.time_to_act = False
                return
        

        game_stage = general_whats_going_on_model(im=current_im) # check if we are holding cards and such 



        if game_stage == "flop":
            print("flop")
            with self.cards_lock:
                self.cards_open = False
            with self.game_stage_lock:
                current_game_stage = self.game_stage_current
            if current_game_stage != "flop":
                with self.own_cards_lock:
                    if self.own_card_left == "nn" or self.own_card_right == "nn":
                        print("model said flop, but own cards not read, exiting out of gameScreenshot_")
                        with self.game_stage_lock:
                            self.game_stage_current = "no_decision_to_be_made" 
                        with self.acting_lock:
                            self.time_to_act = False                                                                                                 
                            current_im.save(f"shmol_model_not_sure/exiting_images/flop_{str(time.time()).split('.')[0]}.png")                                                                        
                            exit()                
                if current_game_stage != "preflop" and current_game_stage != "connectivity_issues":
                    print("\n \n!!! \nmodel said flop, but game stage was not preflop, probably a wrong classification happened\n!!!\n \n")
                    current_im.save(f"shmol_model_not_sure/exiting_images/flop_{str(time.time()).split('.')[0]}.png")
                    print("exiting")
                    exit()
                with self.potheight_lock:
                    self.potheight_after_preflop = self.potheight
                with self.game_stage_lock:
                    self.game_stage_current = "flop"
                secs = time.time()
                # current_im.save(f"shmol_new_data/flop_{str(secs).split(".")[0]}.png")     
                try:
                    with self.cards_lock:
                        [self.deck_card_1, self.deck_card_2, self.deck_card_3, self.deck_card_4, self.deck_card_5] = read_deck_cards()
                except Exception as e:
                    print(e)
                    time.sleep(0.25)
                    try:
                        with self.cards_lock:
                            [self.deck_card_1, self.deck_card_2, self.deck_card_3, self.deck_card_4, self.deck_card_5] = read_deck_cards()
                    except Exception as e:
                        print(e)
                        time.sleep(0.25)                    
                        try:
                            with self.cards_lock:
                                [self.deck_card_1, self.deck_card_2, self.deck_card_3, self.deck_card_4, self.deck_card_5] = read_deck_cards()
                        except Exception as e:
                            print(e) 
                            print("model said flop, but no cards could be read , exiting ... 24")
                            with self.game_stage_lock:
                                self.game_stage_current = "no_decision_to_be_made" 
                            with self.acting_lock:
                                self.time_to_act = False                                                                                                 
                                current_im.save(f"shmol_model_not_sure/exiting_images/flop_{str(time.time()).split('.')[0]}.png")
                                exit()
                if self.deck_card_4 != "nn":
                    print("model said flop, but found at least four cards, exiting out of gameScreenshot_")
                    current_im.save(f"shmol_model_not_sure/exiting_images/flop_{str(time.time()).split('.')[0]}.png")
                    exit()
                    with self.game_stage_lock:
                        self.game_stage_current = "no_decision_to_be_made" 
                    with self.acting_lock:
                        self.time_to_act = False                                                                             
                        return   
                self.calculateFlopEquity()     
                print("flop equity: "+str(self.equity_flop))             

                

        elif game_stage == "no_decision_to_be_made":
            if self.number_of_the_universe%50==0:
                current_im.save(f"shmol_new_data/no_decision_to_be_made_{str(time.time()).split('.')[0]}.png")
            with self.cards_lock:
                self.cards_open = False
            secs = time.time()
            # self.im.save(f"shmol_new_data/no_decision_to_be_made_{str(secs).split(".")[0]}.png")   
            with self.game_stage_lock:     
                if self.game_stage_current != "no_decision_to_be_made":
                    print("no decision to be made")
                    self.game_stage_current = "no_decision_to_be_made"
                # with self.acting_lock:
                #     self.time_to_act = False
                #     return
                
        
        elif game_stage == "river":
            print("river")
            with self.game_stage_lock:
                current_game_stage = self.game_stage_current
            if current_game_stage != "river":
                with self.own_cards_lock:
                    if self.own_card_left == "nn" or self.own_card_right == "nn":
                        print("model said river, but own cards not read, exiting out of gameScreenshot_")
                        with self.game_stage_lock:
                            self.game_stage_current = "no_decision_to_be_made" 
                        with self.acting_lock:
                            self.time_to_act = False  
                            current_im.save(f"shmol_model_not_sure/exiting_images/river_{str(time.time()).split('.')[0]}.png")                                                                         
                            exit()
                if current_game_stage != "flop" and current_game_stage != "connectivity_issues":
                    print("\n \n!!! \nmodel said flop, but game stage was not preflop, probably a wrong classification happened\n!!!\n \n")
                    current_im.save(f"shmol_model_not_sure/exiting_images/river_{str(time.time()).split('.')[0]}.png")
                    print("exiting")
                    exit()  
                with self.potheight_lock:
                    self.potheight_after_flop = self.potheight                          
                self.changeStateMonteCaro()
                with self.game_stage_lock:
                    self.game_stage_current = "river"
                with self.cards_lock:
                    self.cards_open = False
                secs = time.time()
                current_im.save(f"shmol_new_data/river_{str(secs).split(".")[0]}.png")   
                try:
                    with self.cards_lock:
                        [self.deck_card_1, self.deck_card_2, self.deck_card_3, self.deck_card_4, self.deck_card_5] = read_deck_cards(game_stage="river")
                except Exception as e:
                    print(e)
                    time.sleep(0.25)
                    try:
                        with self.cards_lock:
                            [self.deck_card_1, self.deck_card_2, self.deck_card_3, self.deck_card_4, self.deck_card_5] = read_deck_cards(game_stage="river")
                    except Exception as e:
                        print(e)
                        time.sleep(0.25)                    
                        try:
                            with self.cards_lock:
                                [self.deck_card_1, self.deck_card_2, self.deck_card_3, self.deck_card_4, self.deck_card_5] = read_deck_cards(game_stage="river")
                        except Exception as e:
                            print(e) 
                            print("model said river, but no cards could be read , exiting ... 24")
                            current_im.save(f"shmol_model_not_sure/exiting_images/river_{str(time.time()).split('.')[0]}.png")
                            with self.game_stage_lock:
                                self.game_stage_current = "no_decision_to_be_made" 
                            with self.acting_lock:
                                self.time_to_act = False                                                                           
                                exit()
                with self.cards_lock:
                    if self.deck_card_4 == "nn":
                        print("model said river, but found no four cards, exiting out of gameScreenshot_")
                        current_im.save(f"shmol_model_not_sure/exiting_images/river_{str(time.time()).split('.')[0]}.png")
                        exit()
                        with self.game_stage_lock:
                            self.game_stage_current = "no_decision_to_be_made" 
                        with self.acting_lock:
                            self.time_to_act = False                                                                           
                            exit()
                    else:
                        if self.deck_card_5 != "nn":
                            print("model said river, but is turn, exiting out of gameScreenshot_")
                            current_im.save(f"shmol_model_not_sure/exiting_images/river_{str(time.time()).split('.')[0]}.png")
                            with self.game_stage_lock:
                                self.game_stage_current = "no_decision_to_be_made" 
                            with self.acting_lock:
                                self.time_to_act = False                                                                           
                                exit()
                    self.startCalculationsOtherThread_([self.deck_card_1, self.deck_card_2, self.deck_card_3, self.deck_card_4, self.deck_card_5])


        elif game_stage == "turn":
            with self.game_stage_lock:
                current_game_stage = self.game_stage_current
            if current_game_stage != "turn":
                with self.own_cards_lock:
                    if self.own_card_left == "nn" or self.own_card_right == "nn":
                        print("model said turn, but own cards not read, exiting out of gameScreenshot_")
                        with self.game_stage_lock:
                            self.game_stage_current = "no_decision_to_be_made" 
                        with self.acting_lock:
                            self.time_to_act = False                                                                           
                            current_im.save(f"shmol_model_not_sure/exiting_images/turn_{str(time.time()).split('.')[0]}.png")
                            exit()
                if current_game_stage != "river" and current_game_stage != "connectivity_issues":
                    print("\n \n!!! \nmodel said turn, but game stage was not river, probably a wrong classification happened\n!!!\n \n")
                    current_im.save(f"shmol_model_not_sure/exiting_images/turn_{str(time.time()).split('.')[0]}.png")
                    print("exiting")
                    exit()
                with self.potheight_lock:
                    self.potheight_after_river = self.potheight
                with self.game_stage_lock:
                    self.game_stage_current = "turn"
                self.changeStateMonteCaro()
                print("turn")
                with self.cards_lock:
                    self.cards_open = False
                secs = time.time()
                current_im.save(f"shmol_new_data/turn_{str(secs).split(".")[0]}.png")     
                try:
                    with self.cards_lock:
                        [self.deck_card_1, self.deck_card_2, self.deck_card_3, self.deck_card_4, self.deck_card_5] = read_deck_cards(game_stage="turn")
                except Exception as e:
                    print(e)
                    time.sleep(0.75)
                    try:
                        with self.cards_lock:
                            [self.deck_card_1, self.deck_card_2, self.deck_card_3, self.deck_card_4, self.deck_card_5] = read_deck_cards(game_stage="turn")
                    except Exception as e:
                        print(e) 
                        print("model said turn, but no cards could be read , exiting ... 24")
                        current_im.save(f"shmol_model_not_sure/exiting_images/turn_{str(time.time()).split('.')[0]}.png")
                        exit()                          
                        with self.game_stage_lock:
                            self.game_stage_current = "no_decision_to_be_made" 
                        with self.acting_lock:
                            self.time_to_act = False
                            exit()
                with self.cards_lock:
                    if self.deck_card_4 == "nn":
                        print("model said turn, but found no four cards, exiting out of gameScreenshot_")
                        current_im.save(f"shmol_model_not_sure/exiting_images/turn_{str(time.time()).split('.')[0]}.png")
                        exit()                        
                        with self.game_stage_lock:
                            self.game_stage_current = "no_decision_to_be_made" 
                        with self.acting_lock:
                            self.time_to_act = False    
                            exit()
                    if self.deck_card_5 == "nn":
                        print("model said turn, but found no five cards, exiting out of gameScreenshot_")
                        current_im.save(f"shmol_model_not_sure/exiting_images/turn_{str(time.time()).split('.')[0]}.png")
                        exit()              
                        print("model said turn, but no five cards, returning out of gameScreenshot_")
                        with self.game_stage_lock:
                            self.game_stage_current = "no_decision_to_be_made" 
                        with self.acting_lock:
                            self.time_to_act = False                                                                           
                            exit()
                    self.startCalculationsOtherThread_([self.deck_card_1, self.deck_card_2, self.deck_card_3, self.deck_card_4, self.deck_card_5])

        
        elif game_stage == "preflop":
            if self.number_of_the_universe%50==0:
                current_im.save(f"shmol_new_data/preflop_{str(time.time()).split('.')[0]}.png")
            with self.game_stage_lock:
                current_game_stage = self.game_stage_current
            if current_game_stage != "preflop":
                
                with self.game_stage_lock:
                    self.game_stage_current = "preflop"                
                with self.d_lock: # only once after turn or once every preflop
                    self.d_position = read_D(current_im)
                self.roundswap_(current_im)
                print("preflop")
                with self.cards_lock:
                    if self.cards_open == False:
                        secs = time.time()
                        # current_im.save(f"shmol_new_data/preflop_{str(secs).split(".")[0]}.png")  
                        if check_if_we_holdin_yet(current_im):
                            print("I was here 9")
                            try:
                                [self.own_card_left, self.own_card_right] = read_own_cards()
                                self.cards_open = True
                            except Exception as e:
                                # print(e)
                                time.sleep(0.25)
                                try:
                                    [self.own_card_left, self.own_card_right] = read_own_cards()
                                    self.cards_open = True
                                except Exception as e:
                                    # print(e)
                                    time.sleep(0.25)                                
                                    try:
                                        [self.own_card_left, self.own_card_right] = read_own_cards()
                                        self.cards_open = True
                                    except Exception as e:
                                        # print(e)
                                        time.sleep(0.25)
                                        try:
                                            [self.own_card_left, self.own_card_right] = read_own_cards()
                                            self.cards_open = True
                                        except Exception as e:
                                            print(e)
                                            print("cards could not be read, although they are supposed to be there : returning out of gameScreenshot_ ...")  
                                            fish_for_own_cards()   
                                            with self.game_stage_lock:
                                                self.game_stage_current = "no_decision_to_be_made" 
                                            with self.acting_lock:
                                                self.time_to_act = False                                                                           
                                                return
                        else:
                            print("check_if_we_holdin_yet failed, model said preflop ...")
                            time.sleep(1)
                            if check_if_we_holdin_yet(current_im):
                                try:
                                    [self.own_card_left, self.own_card_right] = read_own_cards()
                                    self.cards_open = True
                                except Exception as e:
                                    # print(e)
                                    time.sleep(0.25)
                                    try:
                                        [self.own_card_left, self.own_card_right] = read_own_cards()
                                        self.cards_open = True
                                    except Exception as e:
                                        # print(e)
                                        time.sleep(0.25)
                                        try:
                                            [self.own_card_left, self.own_card_right] = read_own_cards()
                                            self.cards_open = True
                                        except Exception as e:
                                            print(e)
                                            print("cards could not be read, although they are supposed to be there : returning out of gameScreenshot_ ... 222222222222222222") # maybe save screenshot for reclassification purposes
                                            fish_for_own_cards()                                      
                                            with self.game_stage_lock:
                                                self.game_stage_current = "no_decision_to_be_made"  
                                            with self.acting_lock:
                                                self.time_to_act =False                                                                              
                                                return
                            else:
                                with self.game_stage_lock:
                                    self.game_stage_current = "no_decision_to_be_made"  
                                with self.acting_lock:
                                    self.time_to_act = False                                                                              
                                    return                                

                with self.cards_lock:   
                    if not self.cards_open:
                        print("SOMETHING WENT WRONG preflop - 21 - exiting")
                        with self.game_stage_lock:
                            self.game_stage_current = "no_decision_to_be_made"  
                        with self.acting_lock:
                            self.time_to_act = False                                                                              
                            return
                        
                

        

        elif game_stage == "connectivity_issues":
            print("connectivity_issues") 
            secs = time.time()
            current_im.save(f"shmol_new_data/connectivity_issues_{str(secs).split(".")[0]}.png")
            time.sleep(1)
            if handle_all_in(current_im):
                print("ALL IN HANDLED NICELY")
                self.mkModelOutputAllInHandled()
                self.writeToCSVs()
                time.sleep(4) # write loss to model here
                get_up_stand_up()
            with self.acting_lock:
                self.time_to_act = False            
                return


        pix = current_im.getpixel((530, 500)) # there should be a red button here, when it is our turn 
        # print("pix (where red button might be): "+ str(pix))
        if is_red(pix): 
            # pyautogui.moveTo(25, 45)
            # time to cat logic :
            with self.potheight_lock:
                result = read_total_pot_money(current_im)
                if result["result"] > 0.1:
                    self.potheight = result["result"]
                # if self.potheight > 0.2:
                #     pot_rescaled = ((self.potheight/8)**2)
        

            with self.potheight_lock:
                self.to_call = how_much(im=current_im)
                to_call = self.to_call
                print(f"to_call is : {str(to_call)}")
            self.setValuesOurTurn_(current_im=current_im)
            # print("debug I was here 20")
            try:
                self.makeDecision()
            except Exception as e:
                print(f"Exception in makeDecision: {e}")
                exit()
            print("debug I was here 21")
            time.sleep(0.5)

            with self.dec_lock:
                self_dec = self.decision
            if self_dec == "fold":
                if to_call < 0.1:
                    print("checking here !!!")
                    pyautogui.moveTo(670, 610, duration=0.1)
                    time.sleep(0.1)
                    pyautogui.click(670, 610)
                    pyautogui.click(x=1183, y=759)
                    with self.dec_lock:
                        self.decision = "None_yet"                        
                    # self.to_call = 0.0 # already here
                else :
                    pyautogui.moveTo(540, 610, duration=0.1)
                    time.sleep(0.1)                    
                    pyautogui.click(540, 610) # folding, reset values
                    pyautogui.click(x=1183, y=759)
                    with self.lock:
                        if self.own_money > 99.0:
                            close_game()
                            time.sleep(2)
                            print("exiting program bc own money > 99.0")
                            # open_game()
                            exit()        
                    self.resetValues() 

                    # with self.potheight_lock:
                    #     self.to_call = 0.0
                    # with self.cards_lock:
                    #     self.own_card_left = "nn"
                    #     self.own_card_right = "nn"
                    #     self.deck_card_1 = "nn"
                    #     self.deck_card_2 = "nn"
                    #     self.deck_card_3 = "nn"
                    #     self.deck_card_4 = "nn"
                    #     self.deck_card_5 = "nn"
                    # with self.dec_lock:
                    #     self.decision = "None_yet"
            if self_dec.startswith("c"):
                with self.dec_lock:
                    self.decision = "None_yet"
                pyautogui.moveTo(670, 610, duration=0.1)
                time.sleep(0.1)                     
                pyautogui.click(670, 610)
                pyautogui.click(x=1183, y=759)
                print("call was clicked")
                with self.potheight_lock: 
                    self.to_call = 0.0    
                with self.valset_lock:
                    self.values_set = False # own money value only in this                         
            elif self_dec.startswith("r"):
                if to_call < 1.0:
                    pyautogui.moveTo(730, 557, duration=0.1)
                    time.sleep(0.1)     
                    pyautogui.click(730, 557)
                    pyautogui.typewrite("1")
                    pyautogui.moveTo(800, 610)
                    time.sleep(0.1)                  
                    pyautogui.click(800, 610)
                    pyautogui.moveTo(670, 610)
                    time.sleep(0.1)            
                    pyautogui.click(670, 610) # call click
                    pyautogui.click(x=1183, y=759)
                    with self.potheight_lock:
                        self.to_call = 0.0
                    with self.dec_lock:
                        self.decision = "None_yet"
                    with self.valset_lock:
                        self.values_set = False # own money value only in this        
                else: # simply clicking the raise button
                    pyautogui.moveTo(800, 610, duration=0.1)
                    time.sleep(0.1)                  
                    pyautogui.click(800, 610)
                    pyautogui.moveTo(670, 610)
                    time.sleep(0.1)            
                    pyautogui.click(670, 610) # call click
                    pyautogui.click(x=1183, y=759)
                    with self.potheight_lock:
                        self.to_call = 0.0
                    with self.dec_lock:
                        self.decision = "None_yet"
                    with self.valset_lock:
                        self.values_set = False # own money value only in this                                              
            elif self_dec.startswith("2"):
                if to_call < 1:
                    pyautogui.moveTo(730, 557, duration=0.1)
                    time.sleep(0.1)     
                    pyautogui.click(730, 557)
                    pyautogui.typewrite("2")
                    pyautogui.moveTo(800, 610)
                    time.sleep(0.1)                  
                    pyautogui.click(800, 610)
                    pyautogui.moveTo(670, 610)
                    time.sleep(0.1)            
                    pyautogui.click(670, 610) # call click
                    pyautogui.click(x=1183, y=759)
                    with self.potheight_lock:
                        self.to_call = 0.0
                    with self.dec_lock:
                        self.decision = "None_yet"
                    with self.valset_lock:
                        self.values_set = False # own money value only in this    
                else: # simply clicking the raise button
                    pyautogui.moveTo(800, 610, duration=0.1)
                    time.sleep(0.1)                  
                    pyautogui.click(800, 610)
                    pyautogui.moveTo(670, 610)
                    time.sleep(0.1)            
                    pyautogui.click(670, 610) # call click
                    pyautogui.click(x=1183, y=759)
                    with self.potheight_lock:
                        self.to_call = 0.0
                    with self.dec_lock:
                        self.decision = "None_yet"
                    with self.valset_lock:
                        self.values_set = False # own money value only in this                                                           
            elif self_dec.startswith("3"):
                if to_call < 2:
                    print("raise3 was clicked")
                    # todo click text field, type 3, hit (800, 610)
                    pyautogui.moveTo(730, 557, duration=0.1)
                    time.sleep(0.1)     
                    pyautogui.click(730, 557)
                    pyautogui.typewrite("4")
                    pyautogui.moveTo(800, 610)
                    time.sleep(0.1)                  
                    pyautogui.click(800, 610)
                    pyautogui.moveTo(670, 610)
                    pyautogui.click(670, 610) # call click
                    pyautogui.click(x=1183, y=759)
                    with self.dec_lock:
                        self.decision = "None_yet"
                    with self.potheight_lock:
                        self.to_call = 0.0
                    with self.valset_lock:
                        self.values_set = False # own money value only in this     
                else: # simply clicking the raise button
                    pyautogui.moveTo(800, 610, duration=0.1)
                    time.sleep(0.1)                  
                    pyautogui.click(800, 610)
                    pyautogui.moveTo(670, 610)
                    time.sleep(0.1)            
                    pyautogui.click(670, 610) # call click
                    pyautogui.click(x=1183, y=759)
                    with self.potheight_lock:
                        self.to_call = 0.0
                    with self.dec_lock:
                        self.decision = "None_yet"
                    with self.valset_lock:
                        self.values_set = False # own money value only in this                                                       
            elif self_dec.startswith("4"):
                if to_call < 2:
                    print("raise4 was clicked")
                    # click text field, type 4, hit (800, 610)
                    pyautogui.moveTo(730, 557, duration=0.1)
                    time.sleep(0.1)              
                    pyautogui.click(730, 557)
                    pyautogui.typewrite("8")
                    pyautogui.moveTo(800, 610)
                    time.sleep(0.1)              
                    pyautogui.click(800, 610)
                    pyautogui.moveTo(670, 610)
                    time.sleep(0.1)             
                    pyautogui.click(670, 610) # call click
                    pyautogui.click(x=1183, y=759)
                    with self.potheight_lock:
                        self.to_call = 0.0
                    with self.dec_lock:
                        self.decision = "None_yet"
                    with self.valset_lock:
                        self.values_set = False # own money value only in this     
                else: # simply clicking the raise button
                    pyautogui.moveTo(800, 610, duration=0.1)
                    time.sleep(0.1)                  
                    pyautogui.click(800, 610)
                    pyautogui.moveTo(670, 610)
                    time.sleep(0.1)            
                    pyautogui.click(670, 610) # call click
                    pyautogui.click(x=1183, y=759)
                    with self.potheight_lock:
                        self.to_call = 0.0
                    with self.dec_lock:
                        self.decision = "None_yet"
                    with self.valset_lock:
                        self.values_set = False # own money value only in this            
            elif self_dec.startswith("5"):
                if to_call < 8:
                    print("raise5 was clicked")
                    # click text field, type 4, hit (800, 610)
                    pyautogui.moveTo(730, 557, duration=0.1)
                    time.sleep(0.1)              
                    pyautogui.click(730, 557)
                    pyautogui.typewrite("16")
                    pyautogui.moveTo(800, 610)
                    time.sleep(0.1)              
                    pyautogui.click(800, 610)
                    pyautogui.moveTo(670, 610)
                    time.sleep(0.1)             
                    pyautogui.click(670, 610) # call click
                    pyautogui.click(x=1183, y=759)
                    with self.potheight_lock:
                        self.to_call = 0.0
                    with self.dec_lock:
                        self.decision = "None_yet"
                    with self.valset_lock:
                        self.values_set = False # own money value only in this     
                else: # simply clicking the raise button
                    pyautogui.moveTo(800, 610, duration=0.1)
                    time.sleep(0.1)                  
                    pyautogui.click(800, 610)
                    pyautogui.moveTo(670, 610)
                    time.sleep(0.1)            
                    pyautogui.click(670, 610) # call click
                    pyautogui.click(x=1183, y=759)
                    with self.potheight_lock:
                        self.to_call = 0.0
                    with self.dec_lock:
                        self.decision = "None_yet"
                    with self.valset_lock:
                        self.values_set = False # own money value only in this                               
                            
                # time.sleep(1.4)
                # if not self.updateOwnMoney_(current_im=None):
                #     time.sleep(0.45)
                #     if not self.updateOwnMoney_(current_im=None):
                #         print("\nread own money failed after clicking ... 20\n")                                                 
        else: # no red button to push
            try:
                result = read_total_pot_money(current_im)
            except Exception as e:
                print("exiting here 27")
                print(e)
                exit()
            
            if result["result"] > 0.1:
                with self.potheight_lock: # regularly 
                    self.potheight = result["result"]
                    print("debug potheight set to: "+str(self.potheight))
            time.sleep(0.375)
            with self.valset_lock:
                self.number_of_the_universe += 1
                need_set = False
                if not self.values_set: # own money value not set after it changed 
                    need_set = True
            if need_set:
                if not self.updateOwnMoney_(current_im=None):
                    time.sleep(0.25)
                    self.updateOwnMoney_(current_im=None)
                    # print("\nread own money failed gss ... \n")    

        with self.acting_lock:
            self.time_to_act = False  
        # pyautogui.moveTo(15, 55)     




# import signal

# def install_signal_handlers(app):
#     # Schedule cleanup + terminate on main thread when signal arrives.
#     def handler(signum, frame):
#         print("Received signal", signum)
#         # Schedule cleanup on the main run loop (main thread).
#         AppHelper.callAfter(run_cleanup)
#         # After cleanup runs, schedule termination.
#         AppHelper.callAfter(lambda: app.terminate_(None))

#     for sig in ("SIGINT", "SIGTERM", "SIGHUP"):
#         try:
#             signal.signal(getattr(signal, sig), handler)
#         except Exception:
#             # Some signals may not be available on all macOS/Python builds
#             pass










def GUI():

    win = NSWindow.alloc()
    w = 500 # width for the gui123
    h = 350 # height for the gui
    sw = NSScreen.mainScreen().frame().size.width
    frame = ((sw-w, 0), (w, h))
    win.initWithContentRect_styleMask_backing_defer_(frame, 15, 2, 0)
    win.setTitle_("GG")
    win.setLevel_(3)  # floating window
    app = NSApplication.sharedApplication()
    app.activateIgnoringOtherApps_(True)
    delegate = AppDelegate.alloc().init()
    NSApp().setDelegate_(delegate)
    # install_signal_handlers(app)
    delegate.window = win
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
    foldB.setKeyEquivalent_("f")
    delegate.foldB = foldB

    callB = NSButton.alloc().initWithFrame_(((70.0, 260.0), (50.0, 50.0)))
    win.contentView().addSubview_(callB)
    callB.setBezelStyle_(4)
    callB.setTitle_("call")
    callB.setTarget_(app.delegate())
    callB.setAction_("call:")
    callB.setHidden_(True)
    callB.setKeyEquivalent_("c")
    delegate.callB = callB

    raiseB1 = NSButton.alloc().initWithFrame_(((130.0, 260.0), (50.0, 50.0)))
    win.contentView().addSubview_(raiseB1)
    raiseB1.setBezelStyle_(4)
    raiseB1.setTitle_("1")
    raiseB1.setTarget_(app.delegate())
    raiseB1.setAction_("raise1:")
    raiseB1.setHidden_(True)
    raiseB1.setKeyEquivalent_("1")
    delegate.raiseB1 = raiseB1

    raiseB2 = NSButton.alloc().initWithFrame_(((190.0, 260.0), (50.0, 50.0)))
    win.contentView().addSubview_(raiseB2)
    raiseB2.setBezelStyle_(4)
    raiseB2.setTitle_("2")
    raiseB2.setTarget_(app.delegate())
    raiseB2.setAction_("raise2:")
    raiseB2.setHidden_(True)
    raiseB2.setKeyEquivalent_("2")
    delegate.raiseB2 = raiseB2

    raiseB3 = NSButton.alloc().initWithFrame_(((250.0, 260.0), (50.0, 50.0)))
    win.contentView().addSubview_(raiseB3)
    raiseB3.setBezelStyle_(4)
    raiseB3.setTitle_("4")
    raiseB3.setTarget_(app.delegate())
    raiseB3.setAction_("raise3:")
    raiseB3.setHidden_(True)
    raiseB3.setKeyEquivalent_("3")
    delegate.raiseB3 = raiseB3

    raiseB4 = NSButton.alloc().initWithFrame_(((310.0, 260.0), (50.0, 50.0)))
    win.contentView().addSubview_(raiseB4)
    raiseB4.setBezelStyle_(4)
    raiseB4.setTitle_("8")
    raiseB4.setTarget_(app.delegate())
    raiseB4.setAction_("raise4:")
    raiseB4.setHidden_(True)
    raiseB4.setKeyEquivalent_("4")
    delegate.raiseB4 = raiseB4


    raiseB5 = NSButton.alloc().initWithFrame_(((370.0, 260.0), (50.0, 50.0)))
    win.contentView().addSubview_(raiseB5)
    raiseB5.setBezelStyle_(4)
    raiseB5.setTitle_("16")
    raiseB5.setTarget_(app.delegate())
    raiseB5.setAction_("raise5:")
    raiseB5.setKeyEquivalent_("5")
    raiseB5.setHidden_(True)
    delegate.raiseB5 = raiseB5

    # Erstelle einen Slider
    slider = NSSlider.alloc().initWithFrame_(((10, 100), (280, 30)))
    slider.setMinValue_(-10.0)
    slider.setMaxValue_(10.0)
    slider.setDoubleValue_(3.0)  # Startwert
    slider.setTarget_(delegate)
    slider.setAction_("sliderChanged:")
    # Füge den Slider zum Fenster hinzu
    win.contentView().addSubview_(slider)
    # window.makeKeyAndOrderFront_(None)
    delegate.slider = slider


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


