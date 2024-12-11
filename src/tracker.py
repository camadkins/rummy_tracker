from src.game_logic import play_turn, deal, reset_game_state, game_active
from src.config import load_config, save_config
from src.utils import safe_input

config = load_config()

def show_main_menu():
    while True:
        print("\nMain Menu:")
        print("1) Deal new game")
        print("2) Help")
        print("3) Options")
        print("4) Quit")
        choice = safe_input("Choose an option (1/2/3/4): ").strip()
        if choice == '1':
            deal()
            while game_active:
                play_turn()
        elif choice == '2':
            show_help()
        elif choice == '3':
            show_options()
        elif choice == '4':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please select 1, 2, 3, or 4.")

def show_help():
    print("""
    Help Menu:
    - Start a new game from the main menu.
    - Follow prompts for drawing, melding, and discarding.
    - Type 'quit' or 'exit' at any prompt to end the program immediately.
    """)

def show_options():
    global config
    print("\nOptions Menu:")
    print("1) Toggle Test Mode")
    print("2) Set Initial Hand Count")
    print("3) Toggle Display of Wife's Strategy")
    print("4) Return to Main Menu")

    choice = safe_input("Choose an option (1/2/3/4): ").strip()
    if choice == '1':
        config['TEST_MODE'] = not config['TEST_MODE']
        print(f"Test Mode is now {'ON' if config['TEST_MODE'] else 'OFF'}.")
    elif choice == '2':
        new_count = safe_input("Set Initial Hand Count (5, 7, 10): ").strip()
        if new_count in ['5', '7', '10']:
            config['INITIAL_HAND_COUNT'] = int(new_count)
            print(f"Initial Hand Count set to {new_count}.")
        else:
            print("Invalid input. Please enter 5, 7, or 10.")
    elif choice == '3':
        config['DISPLAY_WIFE_STRATEGY'] = not config.get('DISPLAY_WIFE_STRATEGY', False)
        print(f"Wife's Strategy Display is now {'ON' if config['DISPLAY_WIFE_STRATEGY'] else 'OFF'}.")
    elif choice == '4':
        return
    else:
        print("Invalid choice.")
    save_config(config)

if __name__ == "__main__":
    show_main_menu()
