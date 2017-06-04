#! /usr/bin/env/python
"""Game engine that runs initializes player, deck and handles turns"""

from poker_cards import cards, player, hand_evaluation as evaluator
from collections import deque


class Game(object):
    def __init__(self, num_players=4, deck=cards.Deck(), start_money=50000):
        self.rounds = 0
        self.pot = 0
        self.ante = 0
        self.players = [player.Player(str(i), money=start_money) for i in range(num_players)]
        self.deck = deck
        self.winner = None
        self.hand_won = None
        self.bet = None
        self.folded = None
        self.turn_queue = None
        self.call_check = None
        self.dealer = None
        self.small_blind = None
        self.big_blind = None
        self.position = 0
        self.table = cards.Hand('Cards on the table')
        self.evaluator = evaluator.HandEval()

    def individual_turn(self, competitor):
        # Individual player chooses to fold, check, call, or raise
        choice = None
        if not self.bet:

            while choice.lower() not in ['check', 'fold', 'raise']:
                choice = input('Check, Fold, or Raise?')

            if choice.lower() == 'check':
                self.call_check.append(self.turn_queue.popleft())

            elif choice.lower() == 'raise':
                competitor.bet_value = input('Choose a number between {} and {}'.format(str(self.ante),
                                                                                        str(competitor.money)))
                while int(competitor.bet_value) < self.ante or int(competitor.bet_value) > competitor.money:
                    competitor.bet_value = input('Choose a number between {} and {}'.format(str(self.ante),
                                                                                            str(competitor.money)))
                if int(competitor.bet_value) == competitor.money:
                    print('Going all in!!')

                self.bet = competitor.bet_value
                self.pot += self.bet
                competitor.money -= self.bet

                while len(self.call_check) > 0:
                    self.turn_queue.append(self.call_check.popleft())

                self.call_check.append(self.turn_queue.popleft())

            elif choice.lower() == 'fold':
                self.folded.append(self.turn_queue.popleft())

        elif self.bet:

            while choice.lower() not in ['call', 'fold', 'raise']:
                choice = input('Call, Fold, or Raise?')

            if choice.lower() == 'call':
                competitor.bet_value = self.bet
                competitor.money -= competitor.bet_value
                self.call_check.append(self.turn_queue.popleft())

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
                self.pot += self.bet
                competitor.money -= competitor.bet_value

                while len(self.call_check) > 0:
                    self.turn_queue.append(self.call_check.popleft())

                self.call_check.append(self.turn_queue.popleft())

            elif choice.lower() == 'fold':
                self.folded.append(self.turn_queue.popleft())

                # return choice.lower(), competitor.bet_value

    def showdown(self):
        # call hand evaluator here to figure out winner
        table_binary_list = self.table.hand_to_binary()
        eval_dict = {}

        for competitor in self.turn_queue:
            # Print out actual hand class, e.g full house
            eval_dict[competitor.name] = self.evaluator.eval(competitor.hand.hand_to_binary(), table_binary_list)
            print(competitor.name+' ',
                  competitor.hand+' ',
                  self.evaluator.class_to_string(self.evaluator.get_rank_class(eval_dict[competitor.name])))

        # Figure out winners
        min_value = min(eval_dict.values())
        winners = [k for k in min_value if min_value[k] == min_value]

        # Pay out money to competitors
        for competitor in self.turn_queue:
            if competitor.name in winners:
                competitor.money += self.pot / len(winners)

        self.pot = 0
        self.hand_won = True

    def turn(self):
        # Pre flop
        if self.rounds == 0:
            if len(self.turn_queue) > 1:
                for competitor in self.turn_queue:
                    self.individual_turn(competitor)
                self.bet = None

            elif len(self.turn_queue) == 1:
                self.showdown()

        # FLop
        if self.rounds == 1:
            if len(self.turn_queue) > 1:
                self.deck.move_cards(self.table, 3)
                print(self.table)
                for competitor in self.turn_queue:
                    self.individual_turn(competitor)
                self.bet = None

            elif len(self.turn_queue) == 1:
                self.showdown()

        # Turn
        if self.rounds == 2:
            if len(self.turn_queue) > 1:
                self.deck.move_cards(self.table, 1)
                print(self.table)
                for competitor in self.turn_queue:
                    self.individual_turn(competitor)
                self.bet = None

            elif len(self.turn_queue) == 1:
                self.showdown()

        # River
        if self.rounds == 3:
            if len(self.turn_queue) > 1:
                self.deck.move_cards(self.table, 1)
                print(self.table)
                for competitor in self.turn_queue:
                    self.individual_turn(competitor)
                self.bet = None

        self.rounds += 1

    def round(self):
        """
        Handles objects that control game flow in a betting round
        :return: None
        """
        # Initialize flow control objects
        self.turn_queue = deque(self.players)
        self.call_check = deque()
        self.folded = []
        self.dealer = self.turn_queue[self.position % 4]
        self.small_blind = self.turn_queue[(self.position + 1) % 4]
        self.big_blind = self.turn_queue[(self.position + 2) % 4]

        # Deal cards to competitors
        for competitor in self.players:
            self.deck.move_cards(competitor.hand, 2)

        # Keep turns going if nobody has won and its not the 3rd round
        while self.rounds < 3 and not self.hand_won:
            self.turn()

        # See cards if  its the end of the third round
        if self.rounds > 3 and not self.hand_won:
            self.showdown()

        # Return cards
        self.table.move_cards(self.deck, 5)
        for competitor in self.players:
            competitor.hand.move_cards(self.deck, 2)

        # Adjust dealer and blinds
        self.position += 1

        # to stop game in between if host chooses to
        x = input('continue?')
        if x.lower() == 'quit':
            exit()
