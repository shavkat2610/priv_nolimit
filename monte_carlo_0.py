from treys import Card, Evaluator, Deck
import itertools
import time


def exact_win_probability(hero_cards, board_cards=None):
    evaluator = Evaluator()

    hero = [Card.new(c) for c in hero_cards]
    board = [Card.new(c) for c in (board_cards or [])]

    deck = Deck().cards
    known = set(hero + board)

    # Remove known cards from deck
    remaining = [c for c in deck if c not in known]

    wins = ties = losses = 0

    # Opponent hole card combinations
    for opp in itertools.combinations(remaining, 2):
        rem2 = [c for c in remaining if c not in opp]

        # Complete board if needed
        need = 5 - len(board)

        if need == 0:      # river
            possibilities = [()]
        else:
            possibilities = itertools.combinations(rem2, need)

        for add_board in possibilities:
            full_board = board + list(add_board)

            hero_score = evaluator.evaluate(hero, full_board)
            opp_score = evaluator.evaluate(list(opp), full_board)

            if hero_score < opp_score:
                wins += 1
            elif hero_score == opp_score:
                ties += 1
            else:
                losses += 1

    total = wins + ties + losses

    return {
        "Win probability": wins / total,
        "Tie probability": ties / total,
        "Lose probability": losses / total,
        "Total evaluated": total
    }




if __name__ == "__main__":
    start = time.time()
    # -----------------------------
    # Example use (turn stage)
    # Hero: Ah Kh
    # Board: Qh Jh 2c 9s
    # -----------------------------
    result = exact_win_probability(
        hero_cards=["Td", "Qs"],
        board_cards=["Kd", "Ah", "Jh",  "3d", "6c"]
    )

    print(result)
    print()
    end = time.time()
    print(end - start)
