import sys
import random

def safe_input(prompt):
    try:
        user_input = input(prompt).strip()
        if user_input.lower() in ["quit", "exit"]:
            print("Exiting the program. Goodbye!")
            sys.exit(0)
        return user_input
    except (KeyboardInterrupt, EOFError):
        print("\nExiting the program. Goodbye!")
        sys.exit(0)

def sort_hand(hand):
    hand.sort(key=lambda card: (card[1], card[0]))

def is_valid_meld(meld):
    # Example logic for validating melds (e.g., sequences or sets)
    if len(meld) < 3:
        return False
    suits = [card[-1] for card in meld]
    ranks = [card[:-1] for card in meld]
    if len(set(suits)) == 1 and all(int(ranks[i]) - int(ranks[i - 1]) == 1 for i in range(1, len(ranks))):
        return True
    return False

def detect_melds(hand):
    # Logic to detect melds from the hand
    return []  # Example placeholder implementation

def display_card(card):
    return f"{card[:-1]}{card[-1]}"

def display_hand(hand):
    return ", ".join(display_card(card) for card in hand)

def print_game_state():
    # Complete game state display
    pass

def set_initial_player():
    # Logic for determining the initial player
    pass

def reset_game_state(global_state):
    """Resets the game state variables for a new game."""
    global_state["my_hand"].clear()
    global_state["wife_hand"].clear()
    global_state["discard_pile"].clear()
    global_state["deck"] = [f"{rank}{suit}" for rank in "A23456789TJQK" for suit in "SHDC"]
    random.shuffle(global_state["deck"])
    global_state["game_active"] = True
