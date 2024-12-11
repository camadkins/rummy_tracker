import unittest
from src.tracker import calculate_probabilities, recommend_discard, recommend_draw_action
from src.utils import detect_melds, sort_hand

class TestTracker(unittest.TestCase):

    def test_calculate_probabilities(self):
        global my_hand, wife_known_cards, wife_unknown_cards, my_melds, wife_melds, discard_pile, deck
        my_hand = ["5H", "6H", "7H"]
        wife_known_cards = ["5S", "5D"]
        wife_unknown_cards = ["8C", "9C"]
        my_melds = [["5H", "6H", "7H"]]
        wife_melds = [["5S", "5D"]]
        discard_pile = ["KD", "QC"]
        deck = ["9H", "8D"]

        calculate_probabilities()

    def test_recommend_discard(self):
        global my_hand
        my_hand = ["5H", "6H", "7H", "8C"]
        recommend_discard()

    def test_recommend_draw_action(self):
        global my_hand, discard_pile
        my_hand = ["5H", "6H"]
        discard_pile = ["7H", "8D"]
        recommend_draw_action()

    def test_detect_melds_edge_case(self):
        hand = ["5H", "6H", "7H", "8H", "9H", "7S", "7D", "7C"]
        melds = detect_melds(hand)

        def normalize_melds(melds):
            return [sorted(meld) for meld in melds]

        sorted_melds = normalize_melds(melds)

        expected_run = ["5H", "6H", "7H", "8H", "9H"]
        expected_set = ["7S", "7D", "7C", "7H"]  # Account for 4-card set

        sorted_expected_run = sorted(expected_run)
        sorted_expected_set = sorted(expected_set)

        self.assertIn(sorted_expected_run, sorted_melds)
        self.assertIn(sorted_expected_set, sorted_melds)

if __name__ == "__main__":
    unittest.main()
