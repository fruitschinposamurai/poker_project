#! /usr/bin/env/python

from poker_cards import cards

"""Player class used to keep track of players, their cards, and money"""


class Player(object):
    """Player class that keeps track of player's cards and money."""

    def __init__(self, player_counter, money=0):
        self.money = money
        self.name = 'Player{}'.format(player_counter)
        self.hand = cards.Hand('Player{}_hand'.format(player_counter))
        self.bet_status = None #1 for check, 2call, 3 for raise, 0 for fold
        self.bet_value = None
