#! /usr/bin/env/python
"""Game engine that runs initializes player, deck and handles turns"""

from poker_cards import cards, player, hand_evaluation as evaluator
import socket, sys, logging, json
from collections import deque
import threading
import pdb

# TODO: Rotating player starts from left of the dealer


class Game(object):
    def __init__(self, num_players=4, deck=cards.Deck(), start_money=50000):
        self.rounds = 0
        self.pot = 0
        self.ante = 0
        self.players = [player.Player(str(i), money=start_money) for i in range(num_players)]
        self.player_dict = {plyr.name: plyr for plyr in self.players}
        self.deck = deck
        self.winner = None
        self.hand_won = False
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
        self.socket = Game_Socket()

        print("Today's players are: {}".format(','.join([i.name for i in self.players])))

    def individual_turn(self, competitor):
        # Individual player chooses to fold, check, call, or raise
        print(competitor.name)
        choice = None
        # If the player can still check
        if not self.bet:

            while choice not in ['check', 'fold', 'raise']:
                choice = input('Check, Fold, or Raise?')
                if choice == 'money':
                    print(competitor.money)
                elif choice == 'hand':
                    print(competitor.hand)
                elif choice == 'table':
                    print(self.table)
                elif choice == 'pot':
                    print(self.pot)
                elif choice == 'cck':
                    print(self.call_check)

            # Check
            if choice.lower() == 'check':
                # pdb.set_trace()
                self.call_check.append(self.turn_queue.popleft())

            # Raise
            elif choice.lower() == 'raise':
                competitor.bet_value = input('Choose a number between {} and {}'.format(str(self.ante),
                                                                                        str(competitor.money)))
                while int(competitor.bet_value) < self.ante or int(competitor.bet_value) > competitor.money:
                    competitor.bet_value = input('Choose a number between {} and {}'.format(str(self.ante),
                                                                                            str(competitor.money)))
                if int(competitor.bet_value) == competitor.money:
                    print('Going all in!!')

                self.bet = int(competitor.bet_value)
                self.pot += self.bet
                competitor.money -= self.bet

                while len(self.call_check) > 0:
                    self.turn_queue.append(self.call_check.popleft())

                self.call_check.append(self.turn_queue.popleft())

            # Fold
            elif choice.lower() == 'fold':
                self.folded.append(self.turn_queue.popleft())

        # If player cannot check
        elif self.bet:

            while choice not in ['call', 'fold', 'raise']:
                choice = input('Call, Fold, or Raise?')
            if choice == 'money':
                print(competitor.money)
            elif choice == 'hand':
                print(competitor.hand)
            elif choice == 'table':
                print(self.table)
            elif choice == 'pot':
                print(self.pot)
            elif choice == 'cck':
                print(self.call_check)

            # Call
            if choice.lower() == 'call':
                competitor.bet_value = self.bet
                competitor.money -= competitor.bet_value
                self.pot += self.bet
                self.call_check.append(self.turn_queue.popleft())

            # Raise
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

                self.bet = int(competitor.bet_value)
                self.pot += self.bet
                competitor.money -= competitor.bet_value

                while len(self.call_check) > 0:
                    self.turn_queue.append(self.call_check.popleft())

                self.call_check.append(self.turn_queue.popleft())

            # Fold
            elif choice.lower() == 'fold':
                self.folded.append(self.turn_queue.popleft())

    def showdown(self):
        # pdb.set_trace()
        # call hand evaluator here to figure out winner

        if len(self.call_check) == 1:
            self.call_check[0].money += self.pot

        elif len(self.call_check) > 1:

            table_binary_list = self.table.hand_to_binary()
            eval_dict = {}

            for competitor in self.call_check:
                # Print out actual hand class, e.g full house
                eval_dict[competitor.name] = self.evaluator.eval(competitor.hand.hand_to_binary(), table_binary_list)
                print(competitor.name+' ',
                      competitor.hand)
                print(self.evaluator.class_to_string(self.evaluator.get_rank_class(eval_dict[competitor.name])))

            # Figure out winners
            min_value = min(eval_dict.values())
            winners = [k for k in eval_dict.keys() if eval_dict[k] == min_value]

            # Pay out money to competitors
            print('The winners of this round are: ')
            for competitor in self.call_check:
                if competitor.name in winners:
                    print(competitor.name, competitor.hand)
                    competitor.money += self.pot / len(winners)

        self.pot = 0
        self.hand_won = True

    def turn(self):
        # pdb.set_trace()
        # Pre flop
        if self.rounds == 0:
            while len(self.turn_queue) > 1:
                for competitor in list(self.turn_queue):
                    if len(self.folded) != (len(self.players) - 1):
                        self.individual_turn(competitor)
            self.bet = None

            if (len(self.turn_queue) == 0) and (len(self.folded) == (len(self.players) - 1)):
                self.showdown()

            for i in range(len(self.call_check)):
                self.turn_queue.append(self.call_check.popleft())

        # FLop
        elif self.rounds == 1:
            self.deck.move_cards(self.table, 3)
            print(self.table)
            while len(self.turn_queue) > 1:
                for competitor in list(self.turn_queue):
                    if len(self.folded) != (len(self.players) - 1):
                        self.individual_turn(competitor)
            self.bet = None

            if (len(self.turn_queue) == 0) and (len(self.folded) == (len(self.players) - 1)):
                self.showdown()

            for i in range(len(self.call_check)):
                self.turn_queue.append(self.call_check.popleft())

        # Turn
        elif self.rounds == 2:
            self.deck.move_cards(self.table, 1)
            print(self.table)
            while len(self.turn_queue) > 1:
                for competitor in list(self.turn_queue):
                    if len(self.folded) != (len(self.players) - 1):
                        self.individual_turn(competitor)
            self.bet = None

            if (len(self.turn_queue) == 0) and (len(self.folded) == (len(self.players) - 1)):
                self.showdown()

            for i in range(len(self.call_check)):
                self.turn_queue.append(self.call_check.popleft())

        # River
        elif self.rounds == 3:
            self.deck.move_cards(self.table, 1)
            print(self.table)
            while len(self.turn_queue) > 1:
                for competitor in list(self.turn_queue):
                    if len(self.folded) != (len(self.players) - 1):
                        self.individual_turn(competitor)
            self.bet = None

        self.rounds += 1

    def round(self):
        """
        Handles objects that control game flow in a betting round
        :return: None
        """
        # Initialize flow control objects
        self.deck.shuffle()
        self.turn_queue = deque(self.players)
        self.call_check = deque()
        self.folded = []
        offset = -((self.position + 1) % len(self.turn_queue))
        # self.dealer = self.turn_queue[self.position % len(self.turn_queue)]
        # self.small_blind = self.turn_queue[(self.position + 1) % len(self.turn_queue)]
        # self.big_blind = self.turn_queue[(self.position + 2) % len(self.turn_queue)]
        self.turn_queue.rotate(offset)

        # Keep turns going if nobody has won and its not the 3rd round
        while self.rounds < 4 and not self.hand_won:
            if self.rounds == 1:

                # Deal cards to competitors
                for competitor in self.turn_queue:
                    self.deck.move_cards(competitor.hand, 2)
            self.turn()
            # pdb.set_trace()

        # See cards if its the end of the third round
        if self.rounds > 3 and not self.hand_won:
            self.showdown()

        # Return cards and reset logic counters
        self.table.move_cards(self.deck, len(self.table.cards))
        for competitor in self.players:
            competitor.hand.move_cards(self.deck, len(competitor.hand.cards))
        self.rounds = 0
        self.hand_won = False
        self.pot = 0
        # Adjust dealer and blinds
        self.position += 1

        # to stop game in between if host chooses to
        x = input('continue?')
        if x.lower() == 'quit':
            exit()

class Game_Socket():
    """
    Handles information transfer between Game() and players
    """
    def _init__(self, game):
        """"""
        self.serv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print('Socket created')
        self.replies = {"cards": self._cards, "join": self._join}
        self.game = game

    def _bind(self, HOST = socket.gethostbyname(socket.gethostname()),
        PORT = 8888):
        """"""
        try:
            self.serv_sock.bind((HOST, PORT))
        except OSError as err:
            print("Bind failed. Error Code : {0}".format(err))
            sys.exit()

        print('Socket{0},{1} bind complete'.format(HOST, PORT))
        self.serv_sock.listen(10)
        print('socket listening at {}'.format(PORT))

    def clientreply(self, conn, func):
        """
        Send info back to client from the server
        :param conn:
        :param func:
        :return:
        """
        while True:
            info = json.loads(conn.recv(1024))
            intReply = self.game.replies[info["request"]]
            reply = self.replies[intReply](info)
            if not info:
                break

            conn.sendall(reply)
        conn.close()

    def _cards(self, info):
        """
        Sends back cards for players who request crd response
        :param info: JSON info for player who is requesting card info
        :return: [player hand, table]
        """
        return [self.game.player_dict[info["name"]].hand, self.game.table]

    def _join(self, info):
        """
        Joins players who send info to the game
        :param info: JSON info for player who is joining the game
        :return:
        """
        self.game.players.append(player.Player(info["name"]))
        return "Player {} added to game".format(info["name"])

    # TODO Add player login methods such that players are added as the game runs.
            # Players are generated based on their socket info sent. Players send a login packet
            # consisting of a name

    # TODO clientreply method such that it returns json object of request

