#! /usr/bin/env/python
"""Game engine that runs initializes player, deck and handles turns"""

from poker_cards import cards, player


class Game(object):

    def __init__(self, num_players=3, deck=cards.Deck(), start_money=50000):
        self.round = 0
        self.pot = 0
        self.ante = 0
        self.players = [player.Player(money=start_money) for i in range(num_players)]
        self.deck = deck

    def turn(self):
        pass

    def showdown(self):
        pass
