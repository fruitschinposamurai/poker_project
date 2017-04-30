#! /usr/bin/env/python
"""Game engine that runs initializes player, deck and handles turns"""

from poker_cards import cards, player


class Game(object):
    def __init__(self, num_players=3, deck=cards.Deck(), start_money=50000):
        self.rounds = 0
        self.pot = 0
        self.ante = 0
        self.players = [player.Player(money=start_money) for i in range(num_players)]
        self.deck = deck
        self.winner = None
        self.hand_won = None

    def individual_turn(self):
        # Individual player chooses to fold, check, call, or raise
        pass

    def showdown(self):
        # call hand evaluator here to figure out winner
        pass

    def turn(self):
        if self.rounds == 0:
            for competitor in self.players:
                if competitor.bet_status != 0:
                    self.individual_turn()
        if self.rounds == 1:
            for competitor in self.players:
                if competitor.bet_status != 0:
                    self.individual_turn()
        if self.rounds == 2:
            for competitor in self.players:
                if competitor.bet_status != 0:
                    self.individual_turn()
        if self.rounds == 3:
            for competitor in self.players:
                if competitor.bet_status != 0:
                    self.individual_turn()
        self.rounds += 1

    def round(self):
        for competitor in self.players:
            self.deck.move_cards(competitor.hand, 2)
        # Add queue to help betting flow here. Use players from self.players
        while self.rounds < 3 and not self.hand_won:
            self.turn()
        if self.rounds < 3 and not self.hand_won:
            self.showdown()

    def redistribute(self):
        # Redistributes money based on who won the hand
        pass
