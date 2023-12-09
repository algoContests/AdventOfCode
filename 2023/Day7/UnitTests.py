from Hand import *
from functions import *


class TestFunctions(unittest.TestCase):
    def test_functions(self):
        self.assertEqual(five_of_a_kind(['2', '2', '2', '2', '2']), 6)
        self.assertEqual(five_of_a_kind(['2', '3', '4', '5', '6']), -1)
        self.assertEqual(four_of_a_kind(['2', '2', '2', '2', '6']), 5)
        self.assertEqual(four_of_a_kind(['2', '3', '4', '5', '6']), -1)
        self.assertEqual(full_house(['2', '2', '2', '6', '6']), 4)
        self.assertEqual(full_house(['2', '3', '4', '5', '6']), -1)
        self.assertEqual(three_of_a_kind(['2', '2', '2', '5', '6']), 3)
        self.assertEqual(three_of_a_kind(['2', '3', '4', '5', '6']), -1)
        self.assertEqual(two_pairs(['2', '2', '4', '4', '6']), 2)
        self.assertEqual(two_pairs(['2', '3', '4', '5', '6']), -1)
        self.assertEqual(one_pair(['2', '2', '3', '4', '6']), 1)
        self.assertEqual(high_card(['1', '2', '3', '4', '6']), 0)


class TestClasses(unittest.TestCase):
    def test_hand_repr(self):
        hand = Hand(['2', '3', '4', '5', '6'], 1)
        self.assertEqual(hand.__repr__(), "(['2', '3', '4', '5', '6'] 1 0)")

    def test_hand_value(self):
        hand = Hand(['2', '3', '4', '5', '6'], 1)
        self.assertEqual(hand.value, 0)

    def test_hand_lt(self):
        hand_1 = Hand(['2', '3', '4', '5', '6'], 1)
        hand_2 = Hand(['2', '3', '4', '5', '7'], 1)
        self.assertTrue(hand_1 < hand_2)
        hand_3 = Hand(['2', '3', '4', '5', '6'], 1)
        hand_4 = Hand(['2', '3', '4', '5', '7'], 2)
        self.assertTrue(hand_3 < hand_4)
        hand_5 = Hand(['2', '3', '4', '5', '6'], 2)
        hand_6 = Hand(['2', '3', '4', '5', '7'], 3)
        self.assertTrue(hand_5 < hand_6)
        hand_7 = Hand(['2', '3', '4', '5', '6'], 3)
        hand_8 = Hand(['2', '3', '4', '5', '7'], 4)
        self.assertTrue(hand_7 < hand_8)

    def test_hand_gt(self):
        hand_1 = Hand(['2', '3', '4', '5', '6'], 1)
        hand_2 = Hand(['2', '3', '4', '5', '7'], 1)
        self.assertTrue(hand_2 > hand_1)
        hand_3 = Hand(['2', '3', '4', '5', '6'], 1)
        hand_4 = Hand(['2', '3', '4', '5', '7'], 2)
        self.assertTrue(hand_4 > hand_3)
        hand_5 = Hand(['2', '3', '4', '5', '6'], 2)
        hand_6 = Hand(['2', '3', '4', '5', '7'], 3)
        self.assertTrue(hand_6 > hand_5)
        hand_7 = Hand(['2', '3', '4', '5', '6'], 3)
        hand_8 = Hand(['2', '3', '4', '5', '7'], 4)
        self.assertTrue(hand_8 > hand_7)


if __name__ == '__main__':
    test1 = TestFunctions()
    test1.test_functions()
    test2 = TestClasses()
    test2.test_hand_value()
    test2.test_hand_lt()
    test2.test_hand_gt()
