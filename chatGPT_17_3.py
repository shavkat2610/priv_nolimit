import random
import numpy as np
from collections import Counter

from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error

from treys import Card, Deck, Evaluator


RANKS = "23456789TJQKA"
RANK_TO_INT = {r: i for i, r in enumerate(RANKS)}

def rank(card):
    return RANK_TO_INT[card[0]]

def suit(card):
    return card[1]


def is_straight(ranks):
    unique = sorted(set(ranks))

    # Wheel A-2-3-4-5
    if {12, 0, 1, 2, 3}.issubset(unique):
        return True

    for i in range(len(unique) - 4):
        if unique[i + 4] - unique[i] == 4:
            return True

    return False



def hand_rank_category(cards):
    ranks = [rank(c) for c in cards]
    suits = [suit(c) for c in cards]

    rank_counts = Counter(ranks)
    suit_counts = Counter(suits)
    counts = sorted(rank_counts.values(), reverse=True)

    flush = any(v >= 5 for v in suit_counts.values())
    straight = is_straight(ranks)

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


def extract_flop_features(hole, flop):
    cards = hole + flop
    ranks = [rank(c) for c in cards]
    suits = [suit(c) for c in cards]

    board_ranks = [rank(c) for c in flop]
    hole_ranks = [rank(c) for c in hole]

    rank_counts = Counter(ranks)
    suit_counts = Counter(suits)

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

    features.extend([
        top_pair, overpair, middle_pair, bottom_pair, kicker
    ])

    # C. Draws (7)
    flush_draw = int(any(v == 4 for v in suit_counts.values()))
    backdoor_flush = int(any(v == 3 for v in suit_counts.values()))

    unique = sorted(set(ranks))
    gaps = [unique[i+1] - unique[i] for i in range(len(unique)-1)]

    oesd = int(any(g <= 1 for g in gaps) and len(unique) >= 4)
    gutshot = int(any(g == 2 for g in gaps))
    double_gutshot = int(len([g for g in gaps if g == 2]) >= 2)
    backdoor_straight = int(len(unique) >= 3)
    combo_draw = int(flush_draw and (oesd or gutshot))

    features.extend([
        flush_draw, backdoor_flush, oesd, gutshot,
        double_gutshot, combo_draw, backdoor_straight
    ])

    # D. Board texture (7)
    board_counts = Counter(board_ranks)
    board_suits = Counter(suit(c) for c in flop)

    board_paired = int(any(v == 2 for v in board_counts.values()))
    board_trips = int(any(v == 3 for v in board_counts.values()))
    monotone = int(len(board_suits) == 1)
    two_tone = int(len(board_suits) == 2)

    connectedness = np.mean([
        abs(board_ranks[i] - board_ranks[j])
        for i in range(3) for j in range(i+1, 3)
    ]) / 12.0

    board_high = max(board_ranks) / 12.0
    wheel_possible = int(set([12, 0, 1, 2, 3]).issuperset(board_ranks))

    features.extend([
        board_paired, board_trips, monotone, two_tone,
        connectedness, board_high, wheel_possible
    ])

    # E. Dominance (5)
    overcards = sum(r > board_max for r in hole_ranks)
    nut_fd = int(flush_draw and max(hole_ranks) == 12)
    nut_sd = int(oesd and max(hole_ranks) >= 10)
    blockers_flush = int(any(suit(c) in board_suits for c in hole))
    blockers_straight = int(any(r in board_ranks for r in hole_ranks))

    features.extend([
        overcards, nut_fd, nut_sd, blockers_flush, blockers_straight
    ])

    return np.array(features, dtype=np.float32)




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

        if hero_score <= opp_score:  # lower is better in treys
            wins += 1

    return wins / iters






def generate_dataset(n_samples=30000):
    X, y = [], []

    for i in range(n_samples):
        if i%100 == 1:
            print(f"{i} of {n_samples} done")

        deck = Deck()
        cards = deck.draw(5)

        hole = [Card.int_to_str(c) for c in cards[:2]]
        flop = [Card.int_to_str(c) for c in cards[2:]]

        X.append(extract_flop_features(hole, flop))
        y.append(treys_equity(hole, flop))

    return np.array(X), np.array(y)




def train_model():
    X, y = generate_dataset()

    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.1)

    model = GradientBoostingRegressor(
        n_estimators=8000,
        max_depth=8,
        learning_rate=0.01,
        subsample=0.8
    )



    model.fit(Xtr, ytr)

    preds = model.predict(Xte)
    print("MAE:", mean_absolute_error(yte, preds))

    return model









if __name__ == "__main__":
    
    # print("training model ...")
    model = train_model()

    # print("done")

    hole = ["As", "Kd"]
    flop = ["Ah", "7d", "2c"]

    features = extract_flop_features(hole, flop)
    equity = model.predict([features])[0]

    print("Estimated flop equity:", round(equity, 3))

    from joblib import dump, load

    # Save the trained model
    dump(model, "flop_equity_model.joblib")

    # Later, load it
    model_loaded = load("flop_equity_model.joblib")

    # Test
    equity = model_loaded.predict([features])[0]
    print("Predicted equity after reload:", equity)





