



#! usr/bin/python
from datetime import datetime
import os
import csv
                
                
def make_directory_for_saving():
    datetime_now = datetime.now()
    datetime_now = str(datetime_now).split(".")[0].replace(" ", "_").replace(":", "").replace("-", "")
    os.mkdir("datasets/data/" + datetime_now)
    os.mkdir("datasets/data/" + datetime_now + "/0_preflop")
    os.mkdir("datasets/data/" + datetime_now + "/1_flop")
    os.mkdir("datasets/data/" + datetime_now + "/2_river")
    os.mkdir("datasets/data/" + datetime_now + "/3_turn")

    with open("datasets/data/" + datetime_now + "/0_preflop/table.csv",'a', newline='') as fd:
                                writer = csv.writer(fd, delimiter=";")
                                writer.writerow(["pdata_average_1","pdata_average_2","pdata_average_3","pdata_average_4","pdata_before_me_1","pdata_before_me_2","pdata_before_me_3","pdata_before_me_4","i_call_preflop","i_bet_preflop","potheight","to_call","decision","num_active_players","num_active_players_before_me","two","three","four","five","six","seven","eight","nine","ten","jack","queen","king","ace","suited","label"])   
    
    with open("datasets/data/" + datetime_now + "/1_flop/table.csv",'a', newline='') as fd:
                                writer = csv.writer(fd, delimiter=";")
                                writer.writerow(["equity_flop","pdata_average_1","pdata_average_2","pdata_average_3","pdata_average_4","pdata_before_me_1","pdata_before_me_2","pdata_before_me_3","pdata_before_me_4","i_call_preflop","i_bet_preflop","i_call_flop","i_bet_flop","potheight","potheight_after_preflop","to_call","decision","num_active_players","num_active_players_before_me","flop_feat_1","flop_feat_2","flop_feat_3","flop_feat_4","flop_feat_5","flop_feat_6","flop_feat_7","flop_feat_8","flop_feat_9","flop_feat_10","flop_feat_11","flop_feat_12","flop_feat_13","flop_feat_14","flop_feat_15","flop_feat_16","flop_feat_17","flop_feat_18","flop_feat_19","flop_feat_20","flop_feat_21","flop_feat_22","flop_feat_23","flop_feat_24","flop_feat_25","flop_feat_26","flop_feat_27","flop_feat_28","flop_feat_29","flop_feat_30","flopFeat_31","flopFeat_32","label"])   
    
    with open("datasets/data/" + datetime_now + "/2_river/table.csv",'a', newline='') as fd:
                                writer = csv.writer(fd, delimiter=";")
                                writer.writerow(["probability_1_1","pdata_average_1","pdata_average_2","pdata_average_3","pdata_average_4","pdata_before_me_1","pdata_before_me_2","pdata_before_me_3","pdata_before_me_4","i_call_preflop","i_bet_preflop","i_call_flop","i_bet_flop","i_call_river","i_bet_river","potheight","potheight_after_preflop","potheight_after_flop","to_call","decision","num_active_players","num_active_players_before_me","feat_1","feat_2","feat_3","feat_4","feat_5","feat_6","feat_7","feat_8","feat_9","feat_10","feat_11","feat_12","feat_13","feat_14","label"])   
    
    with open("datasets/data/" + datetime_now + "/3_turn/table.csv",'a', newline='') as fd:
                                writer = csv.writer(fd, delimiter=";")
                                writer.writerow(["probability_1_1","pdata_average_1","pdata_average_2","pdata_average_3","pdata_average_4","pdata_before_me_1","pdata_before_me_2","pdata_before_me_3","pdata_before_me_4","i_call_preflop","i_bet_preflop","i_call_flop","i_bet_flop","i_call_river","i_bet_river","i_call_turn","i_bet_turn","potheight","potheight_after_preflop","potheight_after_flop","potheight_after_river","to_call","decision","num_active_players","num_active_players_before_me","feat_1","feat_2","feat_3","feat_4","feat_5","feat_6","feat_7","feat_8","feat_9","feat_10","feat_11","feat_12","feat_13","feat_14","feat_15","label"])   
    
    return datetime_now



make_directory_for_saving()


