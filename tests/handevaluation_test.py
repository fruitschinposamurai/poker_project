import unittest
from poker_cards.cards import Card, Deck, Hand
from poker_cards.hand_evaluation import HandEval
import sys
import pdb
import functools
import traceback
import logging
logging.basicConfig(filename="hand_evaluation.log", level=logging.INFO, format='%(asctime)s %(message)s')
log = logging.getLogger("ex")
log.info('Logging started')


def debug_on(*exceptions):
    if not exceptions:
        exceptions = (AssertionError, )

    def decorator(f):
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            try:
                return f(*args, **kwargs)
            except exceptions:
                info = sys.exc_info()
                traceback.print_exception(*info)
                pdb.post_mortem(info[2])
        return wrapper
    return decorator


class TestCards(unittest.TestCase):

    def setUp(self):
        """
        Set up that run before every function
        :return:
        """
        self.deck = Deck()
        self.hand1 = Hand('Hand 1')
        self.hand2 = Hand('Hand 2')
        self.table = Hand('table')
        self.eval = HandEval()

    def test_eval(self):
        """
        Tests that 2 hands and the table can be evaluated correctly
        :return:
        """
        self.deck.shuffle()
        self.deck.move_cards(self.table, 5)
        self.deck.move_cards(self.hand1, 2)
        self.deck.move_cards(self.hand2, 2)

        table_binary_list = self.table.hand_to_binary()
        hand1_binary_list = self.hand1.hand_to_binary()
        hand2_binary_list = self.hand2.hand_to_binary()
        hand1_eval = self.eval.eval(hand1_binary_list, table_binary_list)
        hand2_eval = self.eval.eval(hand2_binary_list, table_binary_list)

        self.assertIsInstance(hand1_eval, int)
        self.assertIsInstance(hand2_eval, int)
        self.assertGreaterEqual(hand1_eval, 1)
        self.assertGreaterEqual(hand2_eval, 1)
        self.assertLessEqual(hand1_eval, 7462)
        self.assertLessEqual(hand2_eval, 7462)

        log.info(self.eval.class_to_string(self.eval.get_rank_class(hand1_eval)))
        log.info(self.eval.class_to_string(self.eval.get_rank_class(hand2_eval)))
        log.info(str(hand1_eval))
        log.info(str(hand2_eval))
        items = ['Hand1', 'Hand2', 'Table']
        items_objects = [hand1_binary_list, hand2_binary_list, table_binary_list]

        for k in range(len(items_objects)):
            log.info(items[k])
            printed_cards = []
            for j in items_objects[k]:
                printed_cards.append(Card.integer_to_string(j))
            log.info(printed_cards)

if __name__ == '__main__':
    for i in range(1000):
        try:
            unittest.main(verbosity=2, exit=False)
            log.info('Test %s comleted', i)
        except KeyError as err:
            log.exception("Error on test %s!", i, err)
