#! /usr/bin/env/python
"""cards.py contains the classes for cards, decks, and hands"""

import random


class Card(object):
    """Single playing card
    Cards can be compared by number or suite, although cards of the same
    number and differing suite are not necessarily more valuable when compared
    individually"""

    def __init__(self, suit=0, rank=2):
        self.suit = suit
        self.rank = rank

    suit_names = ['Clubs', 'Diamonds', 'Hearts', 'Spades']
    rank_names = [None, '2', '3', '4', '5', '6', '7',
                  '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']

    def __str__(self):
        return '{} of {}'.format(Card.rank_names[self.rank],
                                 Card.suit_names[self.suit])

    def __lt__(self, other):
        card1 = self.rank
        card2 = other.rank


        return ((card1 > card2) - (card1 < card2))

class Deck(object):
    """Deck consists of 52 cards"""


    def __init__(self):
        self.cards = []
        for suit in range(4):
            for rank in range(1,14):
                card = Card(suit, rank)
                self.cards.append(card)

    def __str__(self):
        res = []
        for card in self.cards:
            res.append(str(card))
        return '\n'.join(res)

    def pop_card(self):
        return self.cards.pop()

    def add_card(self, card):
        self.cards.append(card)

    def shuffle(self):
        random.shuffle(self.cards)

    def move_cards(self, hand, num):
        for i in range(num):
            hand.add_card(self.pop_card())


class Hand(Deck):


    def __init__(self, label=''):
        self.cards = []
        self.label = label
