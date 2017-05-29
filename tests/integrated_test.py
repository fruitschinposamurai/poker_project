import unittest
from poker_cards import cards, player, game_engine as game
from poker_cards.hand_evaluation import HandEval


class TestCards(unittest.TestCase):
    def setUp(self):
        self.deck = cards.Deck()
        self.player1 = player.Player(1)
        self.player2 = player.Player(2)
        self.player3 = player.Player(3)

if __name__ == '__main__':
    unittest.main(verbosity=2)
