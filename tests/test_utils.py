from src.utils import sort_hand, detect_melds

def test_sort_hand():
    hand = ["3H", "2S", "5D", "AH"]
    sort_hand(hand)
    assert hand == ["2S", "3H", "5D", "AH"]

def test_detect_melds():
    hand = ["3H", "4H", "5H"]
    assert detect_melds(hand) == []  # Placeholder until implemented
