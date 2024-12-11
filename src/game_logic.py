from src.utils import sort_hand, detect_melds, display_hand, safe_input, reset_game_state
from src.player_logic import handle_player_turn
from src.wife_logic import handle_wife_turn

global_state = {
    "my_hand": [],
    "wife_hand": [],
    "discard_pile": [],
    "deck": [],
    "game_active": True,
}

def deal():
    """Deals cards and sets up the game state."""
    reset_game_state(global_state)
    global_state["my_hand"] = global_state["deck"][:7]
    global_state["wife_hand"] = ["HIDDEN"] * 7
    global_state["deck"] = global_state["deck"][14:]
    global_state["discard_pile"].append(global_state["deck"].pop())
    print("Game setup complete. Your hand:", display_hand(global_state["my_hand"]))
    global_state["game_active"] = True


def play_turn():
    """Plays a single turn for either player."""
    global game_active
    print("Your turn!")
    handle_player_turn()
    # Simulate wife's turn for now
    handle_wife_turn()
    # Check for game over
    if not my_hand or not wife_hand:
        print("Game Over!")
        game_active = False
