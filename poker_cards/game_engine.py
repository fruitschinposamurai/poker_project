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
        self.bet = None

    def individual_turn(self, competitor):
        # Individual player chooses to fold, check, call, or raise
        choice = None
        if not self.bet:
            while choice.lower() not in ['check', 'fold', 'raise']:
                choice = input('Check, Fold, or Raise?')

            if choice.lower() == 'check':
                competitor.bet_status = 1

            elif choice.lower() == 'raise':
                competitor.bet_value = input('Choose a number between {} and {}'.format(str(self.ante),
                                                                                        str(competitor.money)))
                while int(competitor.bet_value) < self.ante or int(competitor.bet_value) > competitor.money:
                    competitor.bet_value = input('Choose a number between {} and {}'.format(str(self.ante),
                                                                                            str(competitor.money)))
                if int(competitor.bet_value) == competitor.money:
                    print('Going all in!!')
                self.bet = competitor.bet_value

            elif choice.lower() == 'fold':
                competitor.bet_status = 0

        elif self.bet:

            while choice.lower() not in ['call', 'fold', 'raise']:
                choice = input('Call, Fold, or Raise?')

            if choice.lower() == 'call':
                competitor.bet_value = self.bet

            elif choice.lower() == 'raise':
                competitor.bet_value = input(
                    'Choose a number between {} and {}'.format(str(self.ante),
                                                               str(competitor.money)))
                while int(competitor.bet_value) < self.ante or int(competitor.bet_value) > competitor.money:
                    competitor.bet_value = input(
                        'Choose a number between {} and {}'.format(str(self.ante),
                                                                   str(competitor.money)))
                if int(competitor.bet_value) == competitor.money:
                    print('Going all in!!')
                self.bet = competitor.bet_value
            elif choice.lower() == 'fold':
                competitor.bet_status = 0
            pass
        return choice.lower(), competitor.bet_value

    def showdown(self):
        # call hand evaluator here to figure out winner
        pass

    def turn(self):
        if self.rounds == 0:
            for competitor in self.players:
                if competitor.bet_status != 0:
                    self.individual_turn(competitor)
        if self.rounds == 1:
            for competitor in self.players:
                if competitor.bet_status != 0:
                    self.individual_turn(competitor)
        if self.rounds == 2:
            for competitor in self.players:
                if competitor.bet_status != 0:
                    self.individual_turn(competitor)
        if self.rounds == 3:
            for competitor in self.players:
                if competitor.bet_status != 0:
                    self.individual_turn(competitor)
        self.rounds += 1

    def round(self):
        for competitor in self.players:
            self.deck.move_cards(competitor.hand, 2)
        # Add queue to help betting flow here. Use players from self.players
        while self.rounds < 3 and not self.hand_won:
            self.turn()
        if self.rounds > 3 and not self.hand_won:
            self.showdown()

    def redistribute(self):
        # Redistributes money based on who won the hand
        pass
