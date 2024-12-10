from collections import defaultdict
import sys
import os
import yaml

suit_map = {
    'S': '♠',
    'H': '♥',
    'D': '♦',
    'C': '♣'
}

def safe_input(prompt):
    """Wrapper around input to allow quitting at any prompt."""
    val = input(prompt)
    if val.strip().lower() in ['quit', 'exit']:
        print("Exiting the program as requested.")
        sys.exit(0)  # Terminate immediately
    return val

def display_card(card):
    rank = card[:-1]
    suit = card[-1]
    unicode_suit = suit_map.get(suit, suit)
    return f"{rank}{unicode_suit}"

def display_hand(hand):
    return ", ".join(display_card(c) for c in hand)

def sort_hand(hand):
    suits_order = ["S","H","D","C"]
    ranks_order = "A23456789TJQK"

    def card_key(card):
        rank = card[:-1]
        suit = card[-1]
        return (suits_order.index(suit), ranks_order.index(rank))

    hand.sort(key=card_key)

def is_valid_meld(meld_cards):
    ranks_order = "A23456789TJQK"
    suits = [c[-1] for c in meld_cards]
    ranks = [c[:-1] for c in meld_cards]

    if len(meld_cards) < 3:
        return False

    # Check set
    if len(set(ranks)) == 1:
        return True

    # Check run
    if len(set(suits)) == 1:
        indices = [ranks_order.index(r) for r in ranks]
        indices.sort()
        for i in range(len(indices)-1):
            if indices[i+1] - indices[i] != 1:
                return False
        return True

    return False

def detect_melds(hand):
    order = "A23456789TJQK"
    from collections import defaultdict
    suits = defaultdict(list)
    ranks = defaultdict(list)

    for card in hand:
        rank, suit = card[:-1], card[-1]
        suits[suit].append(rank)
        ranks[rank].append(suit)

    melds_found = []

    # Check runs
    for suit, ranks_list in suits.items():
        sorted_cards = sorted(ranks_list, key=order.index)
        for i in range(len(sorted_cards) - 2):
            if (order.index(sorted_cards[i+1]) - order.index(sorted_cards[i]) == 1 and
                order.index(sorted_cards[i+2]) - order.index(sorted_cards[i+1]) == 1):
                melds_found.append([f"{r}{suit}" for r in sorted_cards[i:i+3]])

    # Check sets
    for rank, suit_list in ranks.items():
        if len(suit_list) >= 3:
            melds_found.append([f"{rank}{s}" for s in suit_list[:3]])

    return melds_found

def card_value(card):
    rank = card[:-1]
    if rank in "TJQK":
        return 10
    elif rank == "A":
        return 1
    else:
        return int(rank)

def get_yes_no(prompt):
    while True:
        choice = safe_input(prompt).strip().lower()
        if choice in ['y','n']:
            return choice
        print("Please enter 'y' or 'n'.")

def get_choice(prompt, choices):
    while True:
        choice = safe_input(prompt).strip().lower()
        if choice in choices:
            return choice
        print(f"Invalid choice. Valid options: {', '.join(choices)}")

def get_valid_card_input(prompt, deck=None, discard_pile=None, allow_skip=False):
    while True:
        card = safe_input(prompt).strip().upper()
        if allow_skip and card.lower() == 'skip':
            return None
        if len(card) >= 2 and card[-1] in 'SHDC' and card[:-1] in list("A23456789TJQK"):
            if deck is not None and card not in deck:
                print("That card is not available in the deck. Try again.")
                continue
            if discard_pile is not None and card not in discard_pile:
                print("That card is not in the discard pile. Try again.")
                continue
            return card
        else:
            print("Invalid card format. Example: 'AS', '7H', 'TD' etc.")

def load_config(config_path="config.yaml"):
    if not os.path.exists(config_path):
        # Create a default config
        default_config = {
            'TEST_MODE': False,
            'INITIAL_HAND_COUNT': 7,
            'SCORING_MODE': 'manual'
        }
        with open(config_path, 'w') as f:
            yaml.safe_dump(default_config, f)
        return default_config
    else:
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)

def save_config(config, config_path="config.yaml"):
    with open(config_path, 'w') as f:
        yaml.safe_dump(config, f)
