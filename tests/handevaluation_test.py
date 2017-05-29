import unittest
from poker_cards.cards import Card, Deck, Hand
from poker_cards.hand_evaluation import HandEval


class TestCards(unittest.TestCase):

    def setUp(self):
        self.deck = Deck()
        self.hand1 = Hand('Hand 1')
        self.hand2 = Hand('Hand 2')
        self.table = Hand('table')
        self.eval = HandEval()

    def test_eval(self):
        """"""
        self.deck.shuffle()
        self.deck.move_cards(self.table, 5)
        self.deck.move_cards(self.hand1, 2)
        self.deck.move_cards(self.hand2, 2)

        table_binary_list = self.table.hand_to_binary()
        hand1_binary_list = self.hand1.hand_to_binary()
        hand2_binary_list = self.hand2.hand_to_binary()
        hand1_eval = self.eval.eval(hand1_binary_list, table_binary_list)
        hand2_eval = self.eval.eval(hand2_binary_list, table_binary_list)

        self.assertIsInstance(hand1_eval, int)
        self.assertIsInstance(hand2_eval, int)
        self.assertGreaterEqual(hand1_eval, 1)
        self.assertGreaterEqual(hand2_eval, 1)
        self.assertLessEqual(hand1_eval, 7462)
        self.assertLessEqual(hand2_eval, 7462)
        print(self.table, self.hand1)
        print(self.eval.class_to_string(self.eval.get_rank_class(hand1_eval)))
        print(hand1_eval, hand2_eval)
if __name__ == '__main__':
    unittest.main(verbosity=2)
