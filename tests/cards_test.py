import unittest
from poker_cards import cards


class TestCards(unittest.TestCase):

    def setUp(self):
        self.deck = cards.Deck()
        self.hand1 = cards.Hand('hand1')
        self.hand2 = cards.Hand('hand2')

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

if __name__ == '__main__':
    unittest.main(verbosity=2)
