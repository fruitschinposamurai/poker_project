#! /usr/bin/env/python

from poker_cards import cards

"""Player class used to keep track of players, their cards, and money"""


class Player(object):
    """Player class that keeps track of player's cards and money."""

    player_counter = 1

    def __init__(self, money=0, name='Player{}'.format(player_counter), hand=None):
        Player.player_counter += 1
        self.money = money
        self.name = name
        self.hand = hand
