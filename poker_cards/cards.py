#!/Users/AK47/anaconda/bin/python3.6
"""cards.py contains the classes for cards, decks, and hands"""


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
