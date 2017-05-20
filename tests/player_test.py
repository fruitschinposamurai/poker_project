import unittest
from player import Player
from poker_cards import cards


class TestPlayers(unittest.TestCase):

    def setUp(self):
        self.player = Player('Player 1', 5000)


    def test_money(self):
        self.assertEqual(self.player.money, 5000, "Money checks out")

    def test_hand(self):
        self.assertIsInstance(self.player.hand, cards.Hand, "Is of class hand")

if __name__ == "__main__":
    unittest.main(verbosity=2)

