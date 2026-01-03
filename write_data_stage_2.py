from itertools import combinations
from treys import Card, Deck, Evaluator

RANKS = "23456789TJQKA"
SUITS = "shdc"

def rank(card):
    return RANKS.index(card[0])

def suit(card):
    return card[1]


def board_texture(board):
    suits = [suit(c) for c in board]
    ranks = sorted([rank(c) for c in board])

    texture = {
        "paired": len(set(ranks)) < len(ranks),
        "flush_possible": max(suits.count(s) for s in SUITS) >= 2,
        "monotone": max(suits.count(s) for s in SUITS) == 3,
        "connected": max(ranks) - min(ranks) <= 4
    }
    return texture



def has_flush_draw(hand, board):
    suits = [suit(c) for c in hand + board]
    return any(suits.count(s) == 4 for s in SUITS)

def has_straight_draw(cards):
    ranks = sorted(set(rank(c) for c in cards))
    for r in range(len(ranks) - 3):
        if ranks[r+3] - ranks[r] == 3:
            return True
    return False



def pot_odds(bet, pot):
    return bet / (pot + bet)




import random
evaluator = Evaluator()

def monte_carlo_equity(hand, board, iterations=50000):
    wins = 0
    hole_t = [Card.new(c) for c in hand]
    flop_t = [Card.new(c) for c in board]

    for _ in range(iterations):
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

    return wins / iterations




def flop_features(hand, board, pot, stack):
    return {
        "equity": monte_carlo_equity(hand, board),
        "flush_draw": has_flush_draw(hand, board),
        "straight_draw": has_straight_draw(hand + board),
        "board": board_texture(board),
        "SPR": stack / pot
    }




def river_features(hand, board, pot, bet):
    return {
        "equity": monte_carlo_equity(hand, board),
        "pot_odds": pot_odds(bet, pot),
        "blocker_ace": any(c[0] == "A" for c in hand),
        "board": board_texture(board)
    }






































