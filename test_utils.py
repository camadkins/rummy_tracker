import unittest
from utils import (
    sort_hand, is_valid_meld, detect_melds, card_value, display_card, display_hand,
    load_config, save_config
)

class TestUtils(unittest.TestCase):

    def test_sort_hand(self):
        hand = ["5H", "2C", "AS", "KD", "9H"]
        sort_hand(hand)
        self.assertEqual(hand, ["AS", "2C", "5H", "9H", "KD"])

    def test_is_valid_meld_run(self):
        meld = ["5H", "6H", "7H"]
        self.assertTrue(is_valid_meld(meld))

    def test_is_valid_meld_set(self):
        meld = ["5H", "5S", "5D"]
        self.assertTrue(is_valid_meld(meld))

    def test_is_valid_meld_invalid(self):
        meld = ["5H", "6H", "8H"]
        self.assertFalse(is_valid_meld(meld))

    def test_detect_melds(self):
        hand = ["5H", "6H", "7H", "5S", "5D", "9C"]
        melds = detect_melds(hand)
        # Sort melds before asserting
        sorted_melds = [sorted(meld) for meld in melds]
        self.assertIn(sorted(["5H", "6H", "7H"]), sorted_melds)
        self.assertIn(sorted(["5H", "5S", "5D"]), sorted_melds)


    def test_card_value(self):
        self.assertEqual(card_value("5H"), 5)
        self.assertEqual(card_value("KH"), 10)
        self.assertEqual(card_value("AC"), 1)

    def test_display_card(self):
        self.assertEqual(display_card("5H"), "5♥")
        self.assertEqual(display_card("AS"), "A♠")

    def test_display_hand(self):
        hand = ["5H", "AS", "KD"]
        self.assertEqual(display_hand(hand), "5♥, A♠, K♦")

    def test_load_config(self):
        config = load_config("test_config.yaml")
        self.assertIn("TEST_MODE", config)
        self.assertIn("INITIAL_HAND_COUNT", config)
        self.assertIn("SCORING_MODE", config)

    def test_save_config(self):
        config = {"TEST_MODE": True, "INITIAL_HAND_COUNT": 7, "SCORING_MODE": "manual"}
        save_config(config, "test_config.yaml")
        loaded_config = load_config("test_config.yaml")
        self.assertEqual(loaded_config, config)

if __name__ == "__main__":
    unittest.main()
