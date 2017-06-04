import unittest
from poker_cards import cards


class TestCards(unittest.TestCase):

    def setUp(self):
        self.deck = cards.Deck()
        self.hand1 = cards.Hand('hand1')
        self.hand2 = cards.Hand('hand2')
        self.deck.shuffle()

    def test_shuffle(self):
        x = self.deck.cards[0]
        self.deck.shuffle()
        y = (self.deck.cards[0])
        self.assertIsInstance(x, cards.Card)
        self.assertIsInstance(y, cards.Card)
        self.assertNotEqual(y, x, 'Shuffle Worked')
        pass

    def test_move_cards_to_hands(self):
        self.deck.move_cards(self.hand1, 2)
        self.deck.move_cards(self.hand2, 2)
        self.assertEqual(len(self.hand1.cards), 2)
        self.assertEqual(len(self.hand1.cards), len(self.hand2.cards))

    def test_move_cards_from_hand(self):
        self.deck.move_cards(self.hand1, 2)
        self.deck.move_cards(self.hand2, 2)
        self.hand1.move_cards(self.deck, 2)
        self.hand2.move_cards(self.deck, 2)
        self.assertEqual(len(self.hand1.cards), 0)
        self.assertListEqual(self.hand1.cards, self.hand2.cards)

    def test_binary_methods(self):
        def bit_count(int_type):
            count = 0
            while int_type:
                int_type &= int_type - 1
            count += 1
            return count

        self.deck.move_cards(self.hand1, 2)
        self.deck.move_cards(self.hand2, 2)
        hand1_binary_list = self.hand1.hand_to_binary()
        hand2_binary_list = self.hand2.hand_to_binary()

        self.assertIsInstance(hand1_binary_list, list)
        self.assertIsInstance(hand2_binary_list, list)
        self.assertIsInstance(hand1_binary_list[0], int)
        self.assertIsInstance(hand2_binary_list[0], int)

        for i in [hand1_binary_list, hand2_binary_list]:
            for j in range(len(i)):
                self.assertIn(cards.Card.binary_get_suit_int(i[j]), cards.Card.suit_mappings.values())
                if i == hand1_binary_list:
                    self.assertEqual(cards.Card.binary_get_rank(i[j]), self.hand1.cards[j].rank)
                elif i == hand2_binary_list:
                    self.assertEqual(cards.Card.binary_get_rank(i[j]), self.hand2.cards[j].rank)

                self.assertEqual(bit_count(cards.Card.binary_get_bit_rank(i[j])), 1)
                #print(cards.Card.integer_to_string(i[j]), cards.Card.binary_get_prime(i[j]))
                if i == hand1_binary_list:
                    self.assertEqual(cards.Card.binary_get_prime(i[j]), self.hand1.cards[j].rank_prime)
                elif i == hand2_binary_list:
                    self.assertEqual(cards.Card.binary_get_prime(i[j]), self.hand2.cards[j].rank_prime)
        # for i in [self.hand1, self.hand2]:
        #   for j in i.cards:
        #        print(j.rank_prime)
if __name__ == '__main__':
    unittest.main(verbosity=2)
