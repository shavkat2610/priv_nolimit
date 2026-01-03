import random
import numpy as np
from collections import Counter

from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error

import xgboost as xgb
from treys import Card, Deck, Evaluator

from monte_carlo_0 import exact_win_probability












# -------------------------
# Card utilities
# -------------------------
RANKS = "23456789TJQKA"
RANK_TO_INT = {r: i for i, r in enumerate(RANKS)}

def rank(card):
    return RANK_TO_INT[card[0]]

def suit(card):
    return card[1]












# -------------------------
# Straight detection
# -------------------------
def is_straight(ranks):
    unique = sorted(set(ranks))
    if {12, 0, 1, 2, 3}.issubset(unique):
        return True
    for i in range(len(unique) - 4):
        if unique[i + 4] - unique[i] == 4:
            return True
    return False












# -------------------------
# Hand category (0-7)
# -------------------------
def hand_rank_category(cards):
    ranks_ = [rank(c) for c in cards]
    suits_ = [suit(c) for c in cards]

    rank_counts = Counter(ranks_)
    suit_counts = Counter(suits_)
    counts = sorted(rank_counts.values(), reverse=True)

    flush = any(v >= 5 for v in suit_counts.values())
    straight = is_straight(ranks_)

    if counts[0] == 4:
        return 7
    if counts[0] == 3 and counts[1] >= 2:
        return 6
    if flush:
        return 5
    if straight:
        return 4
    if counts[0] == 3:
        return 3
    if counts[0] == 2 and counts[1] == 2:
        return 2
    if counts[0] == 2:
        return 1
    return 0

















# -------------------------
# 32-feature flop extractor
# -------------------------
def extract_flop_features(hole, flop):
    cards = hole + flop
    ranks_ = [rank(c) for c in cards]
    suits_ = [suit(c) for c in cards]

    board_ranks = [rank(c) for c in flop]
    hole_ranks = [rank(c) for c in hole]

    rank_counts = Counter(ranks_)
    suit_counts = Counter(suits_)

    features = []

    # A. Made hand (8)
    made = [0] * 8
    made[hand_rank_category(cards)] = 1
    features.extend(made)

    # B. Pair quality (5)
    board_max = max(board_ranks)
    board_min = min(board_ranks)
    top_pair = int(any(r == board_max for r in hole_ranks))
    overpair = int(hole_ranks[0] == hole_ranks[1] and hole_ranks[0] > board_max)
    middle_pair = int(any(board_min < r < board_max for r in hole_ranks))
    bottom_pair = int(any(r == board_min for r in hole_ranks))
    kicker = max(hole_ranks) / 12.0
    features.extend([top_pair, overpair, middle_pair, bottom_pair, kicker])

    # C. Draws (7)
    flush_draw = int(any(v == 4 for v in suit_counts.values()))
    backdoor_flush = int(any(v == 3 for v in suit_counts.values()))
    unique = sorted(set(ranks_))
    gaps = [unique[i+1] - unique[i] for i in range(len(unique)-1)]
    oesd = int(any(g <= 1 for g in gaps) and len(unique) >= 4)
    gutshot = int(any(g == 2 for g in gaps))
    double_gutshot = int(len([g for g in gaps if g == 2]) >= 2)
    backdoor_straight = int(len(unique) >= 3)
    combo_draw = int(flush_draw and (oesd or gutshot))
    features.extend([flush_draw, backdoor_flush, oesd, gutshot, double_gutshot, combo_draw, backdoor_straight])

    # D. Board texture (7)
    board_counts = Counter(board_ranks)
    board_suits = Counter(suit(c) for c in flop)
    board_paired = int(any(v == 2 for v in board_counts.values()))
    board_trips = int(any(v == 3 for v in board_counts.values()))
    monotone = int(len(board_suits) == 1)
    two_tone = int(len(board_suits) == 2)
    connectedness = np.mean([abs(board_ranks[i] - board_ranks[j]) for i in range(3) for j in range(i+1, 3)]) / 12.0
    board_high = max(board_ranks) / 12.0
    wheel_possible = int(set([12, 0, 1, 2, 3]).issuperset(board_ranks))
    features.extend([board_paired, board_trips, monotone, two_tone, connectedness, board_high, wheel_possible])

    # E. Dominance (5)
    overcards = sum(r > board_max for r in hole_ranks)
    nut_fd = int(flush_draw and max(hole_ranks) == 12)
    nut_sd = int(oesd and max(hole_ranks) >= 10)
    blockers_flush = int(any(suit(c) in board_suits for c in hole))
    blockers_straight = int(any(r in board_ranks for r in hole_ranks))
    features.extend([overcards, nut_fd, nut_sd, blockers_flush, blockers_straight])

    return np.array(features, dtype=np.float32)














# -------------------------
# Treys Monte Carlo equity
# -------------------------
evaluator = Evaluator()

def treys_equity(hole, flop, iters=5000):
    wins = 0
    hole_t = [Card.new(c) for c in hole]
    flop_t = [Card.new(c) for c in flop]

    for _ in range(iters):
        deck = Deck()
        deck.cards = [c for c in deck.cards if c not in hole_t + flop_t]

        turn = deck.draw(1)
        river = deck.draw(1)
        board = flop_t + turn + river
        opp = deck.draw(2)

        hero_score = evaluator.evaluate(board, hole_t)
        opp_score = evaluator.evaluate(board, opp)

        if hero_score <= opp_score:  # lower is better in Treys
            wins += 1

    return wins / iters





# -------------------------
# Dataset generation
# -------------------------
def generate_dataset(n_samples=10001):
    import time
    import pickle
    X, y = [], []
    try:
        with open("X", "rb") as fp:   # Unpickling
            X = pickle.load(fp)
        with open("y", "rb") as fp:   # Unpickling
            y = pickle.load(fp)  
    except:
        print('no pickles could be loaded (none there yet most likely)')  
    for i in range(n_samples):
        if i%10 == 0:
            print(f"generated {i} of {n_samples} samples ...")
        deck = Deck()
        cards = deck.draw(5)
        hole = [Card.int_to_str(c) for c in cards[:2]]
        flop = [Card.int_to_str(c) for c in cards[2:]]
        X.append(extract_flop_features(hole, flop))
        y.append(treys_equity(hole, flop, iters=50000))
        if i%10000 == 0:
            print(f"saving samples ...")
            secs = time.time()
            with open(f"X", "wb") as fp:   #Pickling      
                pickle.dump(X, fp)
            with open(f"y", "wb") as fp:   #Pickling      
                pickle.dump(y, fp)                
    return np.array(X), np.array(y)











# -------------------------
# Train XGBoost
# -------------------------
def train_xgb():
    print("generating dataset")
    X, y = generate_dataset()
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.05)

    model = xgb.XGBRegressor(
        n_estimators=25000,
        max_depth=5, 
        learning_rate=0.01,
        subsample=0.8, 
        colsample_bytree=0.8, 
        objective='reg:squarederror',
        n_jobs=-1,
        random_state=42
    )

    print("fitting now")

    model.fit(X_train, y_train)
    preds = model.predict(X_test)
    print("MAE:", mean_absolute_error(y_test, preds))
    return model










# -------------------------
# Inference example
# -------------------------
if __name__ == "__main__":
    from joblib import dump, load
    hole = ["Ks", "Kd"]
    flop = ["Ah", "Kc", "Kh"]
    # print(treys_equity(hole, flop, iters=25000))

    # features = extract_flop_features(hole, flop)
    # xgb_loaded = load("flop_equity_xgb_0.joblib")
    # equity = xgb_loaded.predict([features])[0]
    # print("Predicted equity:", equity)    
    # exit()
    
    model = train_xgb()
    features = extract_flop_features(hole, flop)
    # equity = model.predict([features])[0]
    # print("Predicted flop equity:", round(equity, 7))



    

    dump(model, "flop_equity_xgb.joblib")    

    xgb_loaded = load("flop_equity_xgb.joblib")

    # Predict
    equity = xgb_loaded.predict([features])[0]
    print("Predicted equity:", equity)

    print("exact_win_probability: "+str(exact_win_probability(hero_cards=hole, board_cards=flop)['Win probability']))

    # import matplotlib.pyplot as plt
    # import seaborn as sns
    # import numpy as np

    # # Assuming 'model' is your trained XGBoost model
    # feature_groups = {
    #     "Made Hand": [
    #         "made_high_card", "made_pair", "made_two_pair", "made_three_kind",
    #         "made_straight", "made_flush", "made_full_house", "made_four_kind"
    #     ],
    #     "Pair Quality": [
    #         "top_pair", "overpair", "middle_pair", "bottom_pair", "kicker"
    #     ],
    #     "Draws": [
    #         "flush_draw", "backdoor_flush", "oesd", "gutshot", 
    #         "double_gutshot", "combo_draw", "backdoor_straight"
    #     ],
    #     "Board Texture": [
    #         "board_paired", "board_trips", "monotone", "two_tone",
    #         "connectedness", "board_high", "wheel_possible"
    #     ],
    #     "Dominance": [
    #         "overcards", "nut_fd", "nut_sd", "blockers_flush", "blockers_straight"
    #     ]
    # }

    # # Flatten feature names
    # feature_names = [f for group in feature_groups.values() for f in group]
    # importances = model.feature_importances_

    # # Sort features within each group
    # heatmap_data_sorted = []
    # sorted_feature_names = []
    # group_importances = []

    # start = 0
    # for group_name, group_features in feature_groups.items():
    #     n = len(group_features)
    #     group_feat_importances = importances[start:start+n]
        
    #     # Sort features by importance descending
    #     sort_idx = np.argsort(group_feat_importances)[::-1]
    #     sorted_feat_importances = group_feat_importances[sort_idx]
    #     sorted_feats = [group_features[i] for i in sort_idx]
        
    #     heatmap_data_sorted.append(sorted_feat_importances)
    #     sorted_feature_names.extend(sorted_feats)
    #     group_importances.append(np.sum(group_feat_importances))
        
    #     start += n

    # heatmap_data_sorted = np.array(heatmap_data_sorted)

    # # Plot
    # fig, ax = plt.subplots(figsize=(18,6))

    # sns.heatmap(heatmap_data_sorted, annot=True, fmt=".3f", cmap="YlGnBu",
    #             yticklabels=list(feature_groups.keys()), xticklabels=sorted_feature_names, ax=ax)

    # # Overlay group importance bars
    # for i, g_imp in enumerate(group_importances):
    #     ax.barh(i+0.5, g_imp, height=0.3, color='orange', alpha=0.5, align='center')

    # ax.set_title("Flop Equity Feature Importance (Sorted Within Groups)")
    # ax.set_xlabel("Features (sorted by importance within group)")
    # ax.set_ylabel("Feature Groups")
    # plt.xticks(rotation=90)
    # plt.tight_layout()
    # plt.show()
