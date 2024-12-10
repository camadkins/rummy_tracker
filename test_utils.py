import pytest
from utils import sort_hand, is_valid_meld, detect_melds, card_value

def test_sort_hand():
    hand = ["9H","AS","2D","3C","TH","KD","7S"]
    sort_hand(hand)
    # After sorting by suit (S,H,D,C) and rank order, check a known order
    # Suits order: S,H,D,C and ranks order A23456789TJQK
    # Hand suits: S=AS,7S; H=9H,TH; D=2D,KD; C=3C
    # Final order should be: AS,7S,9H,TH,2D,KD,3C
    assert hand == ["AS","7S","9H","TH","2D","KD","3C"]

def test_is_valid_meld():
    # Set of same rank
    assert is_valid_meld(["AS","AH","AD"]) == True
    # Run of same suit
    assert is_valid_meld(["7H","8H","9H"]) == True
    # Invalid (not a set or run)
    assert is_valid_meld(["AS","2H","9D"]) == False

def test_detect_melds():
    hand = ["AS","AH","AD","2H","3H","4H","9D"]
    melds = detect_melds(hand)
    # Expected melds: AS,AH,AD (set of Aces), and 2H,3H,4H (run of hearts)
    assert ["AS","AH","AD"] in melds
    assert ["2H","3H","4H"] in melds

def test_card_value():
    assert card_value("AS") == 1
    assert card_value("9D") == 9
    assert card_value("TH") == 10
    assert card_value("KC") == 10
