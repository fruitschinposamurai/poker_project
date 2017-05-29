#! /usr/bin/env/python
"""Evaluates hands for and between players"""
from poker_cards import cards as card, lookup_table
import itertools


class HandEval(object):

    def __init__(self):

        self.hash_table = lookup_table.HashTable()
        self.hand_size_map = {
            5: self._five_eval,
            6: self._choose_five_eval,
            7: self._choose_five_eval
        }

    def eval(self, player_hand, table):
        """
        eval evaluates the list of hand and table, where hand
        :param player_hand: 
        :param table: 
        :return: 
        """
        full_hand = player_hand + table

        return self.hand_size_map[len(full_hand)](full_hand)

    def _five_eval(self, cards):
        """"""
        if cards[0] & cards[1] & cards[2] & cards[3] & cards[4] & 0xF000 != 0:
            print(cards)
            hand_or = (cards[0] | cards[1] | cards[2] | cards[3] | cards[4]) >> 16
            print(hand_or)
            prime = card.Hand.hand_prime_product_rankbits(hand_or)

            return self.hash_table.flush_lookup[prime]

        else:
            prime = card.Hand.hand_prime_product(cards)
            return self.hash_table.unsuited_lookup[prime]

    def _choose_five_eval(self, cards):
        """
        Does a Xc5 based on the number of cards in the hand
        :param cards: 
        :return: 
        """
        minimum = self.hash_table.MAX_HIGH_CARD

        all5cardcombobs = itertools.combinations(cards, 5)
        for combo in all5cardcombobs:

            score = self._five_eval(combo)
            if score < minimum:
                minimum = score

        return minimum

    def get_rank_class(self, hand_rank):
        """
        
        :param hand_rank: 
        :return: 
        """
        if hand_rank >= 0 and hand_rank <= self.hash_table.MAX_STRAIGHT_FLUSH:
            return self.hash_table.MAX_TO_RANK_CLASS[self.hash_table.MAX_STRAIGHT_FLUSH]
        elif hand_rank <= self.hash_table.MAX_FOUR_OF_A_KIND:
            return self.hash_table.MAX_TO_RANK_CLASS[self.hash_table.MAX_FOUR_OF_A_KIND]
        elif hand_rank <= self.hash_table.MAX_FULL_HOUSE:
            return self.hash_table.MAX_TO_RANK_CLASS[self.hash_table.MAX_FULL_HOUSE]
        elif hand_rank <= self.hash_table.MAX_FLUSH:
            return self.hash_table.MAX_TO_RANK_CLASS[self.hash_table.MAX_FLUSH]
        elif hand_rank <= self.hash_table.MAX_STRAIGHT:
            return self.hash_table.MAX_TO_RANK_CLASS[self.hash_table.MAX_STRAIGHT]
        elif hand_rank <= self.hash_table.MAX_THREE_OF_A_KIND:
            return self.hash_table.MAX_TO_RANK_CLASS[self.hash_table.MAX_THREE_OF_A_KIND]
        elif hand_rank <= self.hash_table.MAX_TWO_PAIR:
            return self.hash_table.MAX_TO_RANK_CLASS[self.hash_table.MAX_TWO_PAIR]
        elif hand_rank <= self.hash_table.MAX_PAIR:
            return self.hash_table.MAX_TO_RANK_CLASS[self.hash_table.MAX_PAIR]
        elif hand_rank <= self.hash_table.MAX_HIGH_CARD:
            return self.hash_table.MAX_TO_RANK_CLASS[self.hash_table.MAX_HIGH_CARD]
        else:
            raise Exception("Invalid hand rank, cannot return rank class")

    def class_to_string(self, class_int):
        """
        Converts the integer class hand score into a human-readable string.
        """
        return self.hash_table.RANK_CLASS_TO_STRING[class_int]