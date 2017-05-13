#! /usr/bin/env/python

from poker_cards import cards

"""Player class used to keep track of players, their cards, and money"""


class Player(object):
    """Player class that keeps track of player's cards and money."""

    player_counter = 1

    def __init__(self, money=0, name='Player{}'.format(player_counter),
                 hand=cards.Hand('Player{}_hand'.format(player_counter))):
        Player.player_counter += 1
        self.money = money
        self.name = name
        self.hand = hand
        self.bet_status = None #1 for check, 2call, 3 for raise, 0 for fold
        self.bet_value = None
