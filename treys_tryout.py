from treys import Card
from treys import Evaluator


def bin_score(trays_score = 2):
    
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




# card = Card.new('Qh')
board = [Card.new('2s'),Card.new('2d'),Card.new('3h')]
hand = [Card.new('2h'),Card.new('6c')]
evaluator = Evaluator()
hand_score = evaluator.evaluate(hand, board)
hand_class = evaluator.get_rank_class(hand_score)
print(hand_score, hand_class, evaluator.class_to_string(hand_class))

bin_score(hand_score)



# bin_score(2)



