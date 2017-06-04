#! /usr/bin/env/python
"""cards.py contains the classes for cards, decks, and hands"""

import random


class Card(object):
    """Single playing card
    Cards can be compared by number or suite, although cards of the same
    number and differing suite are not necessarily more valuable when compared
    individually"""

    suit_names = ['Clubs', 'Diamonds', 'Hearts', 'Spades']
    rank_names = ['2', '3', '4', '5', '6', '7',
                  '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']
    rank_integers = list(range(13))
    rank_mappings = dict(list(zip(rank_names, rank_integers)))
    primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41]
    suit_mappings = {
        suit_names[0]: 1,  # clubs
        suit_names[1]: 2,  # diamonds
        suit_names[2]: 4,  # hearts
        suit_names[3]: 8  # spades
    }

    suit_mappings_to_name = {
        1: suit_names[0],
        2: suit_names[1],
        4: suit_names[2],
        8: suit_names[3],
    }

    def __init__(self, suit=0, rank=0):
        self.suit = suit
        self.rank = rank
        self.suit_int = Card.suit_mappings[Card.suit_names[self.suit]]
        self.rank_prime = Card.primes[self.rank]

    def __str__(self):
        return '{} of {}'.format(Card.rank_names[self.rank], Card.suit_names[self.suit])

    def string_to_binary(self):
        """
        Converts card information to binary integer representation
        :return: binary integer
        """
        bit_rank = 1 << self.rank << 16
        suit_bit = self.suit_int << 12
        rank_bit = self.rank << 8

        return bit_rank | suit_bit | rank_bit | self.rank_prime

    @staticmethod
    def binary_get_suit_int(binary_integer):
        """
        Used to get the self.suit_int value from a cards binary value
        :param binary_integer: 
        :return: integer
        """
        return (binary_integer >> 12) & 0xF

    @staticmethod
    def binary_get_rank(binary_integer):
        """
        Used to get the self.rank value from a cards binary value
        :param binary_integer: 
        :return: integer
        """
        return (binary_integer >> 8) & 0xF

    @staticmethod
    def binary_get_bit_rank(binary_integer):
        """
        Used to get the integer value of the cards bit_rank from a cards binary value
        :param binary_integer: 
        :return: integer
        """
        return (binary_integer >> 16) & 0x1FFF

    @staticmethod
    def binary_get_prime(binary_integer):
        """
        Used to get the self.rank_prime value from a cards binary value
        :param binary_integer: 
        :return: integer
        """
        return binary_integer & 0x3F

    @staticmethod
    def int_to_binary(binary_integer):
        """
        For debugging purposes. Displays the binary number as a 
        human readable string in groups of four digits.
        :param binary_integer:
        :return: string
        """
        bstr = bin(binary_integer)[2:][::-1]  # chop off the 0b and THEN reverse string
        output = list("".join(["0000" + "\t"] * 7) + "0000")

        for i in range(len(bstr)):
            output[i + int(i / 4)] = bstr[i]

        # output the string to console
        output.reverse()
        return "".join(output)

    @staticmethod
    def integer_to_string(card_integer):
        """
        Converts card integer to a string format for the card value
        :param card_integer: integer
        :return: string
        """
        rank_int = Card.binary_get_rank(card_integer)
        suit_int = Card.binary_get_suit_int(card_integer)
        return Card.rank_names[rank_int] + Card.suit_mappings_to_name[suit_int]


class Deck(object):
    """Deck consists of 52 cards"""

    def __init__(self):
        self.cards = []
        for suit in range(4):
            for rank in range(13):
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
        super(Hand, self).__init__()
        self.cards = []
        self.label = label

    def hand_to_binary(self):
        """
        Takes the cards in a hand and gives back a list of 
        binary integers
        :return: list
        """
        bin_hand = []
        for card in self.cards:
            bin_hand.append(card.string_to_binary())

        return bin_hand

    # Should this really be a static method? May have to rewrite this function
    @staticmethod
    def hand_prime_product(integer_cards_list):
        """
        Takes a list of cards in integer form and 
        gives back the prime product
        :param integer_cards_list: 
        :return: integer
        """
        product = 1
        for card_integer in integer_cards_list:
            product *= (card_integer & 0xFF)

        return product

    # Should this really be a static method? May have to rewrite this function
    @staticmethod
    def hand_prime_product_rankbits(hand_rankbits):
        """
        
        :param hand_rankbits: 
        :return: 
        """
        product = 1
        for i in Card.rank_integers:
            if hand_rankbits & (1 << i):
                product *= Card.primes[i]
        return product
