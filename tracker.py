import csv
from fpdf import FPDF
import os
import random
import sys
from scoreboard import Scoreboard

from utils import (
    sort_hand, is_valid_meld, detect_melds, card_value, display_card, display_hand,
    get_yes_no, get_choice, get_valid_card_input, safe_input,
    load_config, save_config
)

GAME_HISTORY_FILE = "data/game_history.csv"

config = load_config("config.yaml")
TEST_MODE = config.get('TEST_MODE', False)
INITIAL_HAND_COUNT = config.get('INITIAL_HAND_COUNT', 7)
SCORING_MODE = config.get('SCORING_MODE', 'manual')

ranks = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K"]
suits = ["S", "H", "D", "C"]
deck = [f"{r}{s}" for r in ranks for s in suits]

my_hand = []
wife_hand = []
discard_pile = []
wife_known_cards = []
wife_unknown_cards = []
my_melds = []
wife_melds = []
wife_meld_count = 0
forced_meld_card = None
current_player = "me"
game_active = True
scoreboard = Scoreboard()
need_final_discard = {
    "me": False,
    "wife": False
}

def main():
    print(r"""
   _____            _____   _____  _______  _____             _____  _  __ ______  _____
  / ____|    /\    |  __ \ |  __ \|__   __||  __ \     /\    / ____|| |/ /|  ____||  __ \
 | |        /  \   | |__) || |  | |  | |   | |__) |   /  \  | |     | ' / | |__   | |__) |
 | |       / /\ \  |  _  / | |  | |  | |   |  _  /   / /\ \ | |     |  <  |  __|  |  _  /
 | |____  / ____ \ | | \ \ | |__| |  | |   | | \ \  / ____ \| |____ | . \ | |____ | | \ \
  \_____|/_/    \_\|_|  \_\|_____/   |_|   |_|  \_\/_/    \_\\_____||_|\_\|______||_|  \_\
    """)
    print("                         by Cameron Adkins")
    print("")

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
                play_turn(scoreboard)
        elif choice == '2':
            show_help()
        elif choice == '3':
            options_menu()
        elif choice == '4':
            print("Goodbye!")
            return
        else:
            print("Invalid choice. Please select 1, 2, 3, or 4.")

def show_help():
    print("""
    Rummy Tracker Help:
    - Start a new game by choosing '1' from the main menu.
    - Configure settings (test mode, hand count, scoring mode) in '4) Options'.
    - Follow on-screen prompts for drawing, melding, discarding, and playing off melds.
    - Probability and recommendations appear automatically each turn.
    - End of game:
      - Manual scoring: enter final scores.
      - Auto scoring: leftover card points decide the winner.
    - In test mode, no CSV/PDF is generated.
    - Type 'quit' or 'exit' at any prompt to end the program immediately.
    """)


def options_menu():
    global TEST_MODE, INITIAL_HAND_COUNT, SCORING_MODE, config
    while True:
        print("\nOptions Menu:")
        print(f"1) Toggle test mode (current: {'ON' if TEST_MODE else 'OFF'})")
        print(f"2) Set initial hand count (current: {INITIAL_HAND_COUNT})")
        print(f"3) Set scoring mode (current: {SCORING_MODE})")
        print(f"4) Toggle wife's strategy display (current: {'ON' if config.get('DISPLAY_WIFE_STRATEGY', False) else 'OFF'})")
        print("5) Return to main menu")
        choice = safe_input("Choose an option (1/2/3/4/5): ").strip()
        if choice == '1':
            TEST_MODE = not TEST_MODE
            config['TEST_MODE'] = TEST_MODE
            save_config(config)
            print(f"Test mode is now {'ON' if TEST_MODE else 'OFF'}.")
        elif choice == '2':
            hc = safe_input("Choose hand count (5/7/10): ").strip()
            if hc in ['5','7','10']:
                INITIAL_HAND_COUNT = int(hc)
                config['INITIAL_HAND_COUNT'] = INITIAL_HAND_COUNT
                save_config(config)
                print(f"Initial hand count set to {INITIAL_HAND_COUNT}.")
            else:
                print("Invalid choice, must be 5, 7, or 10.")
        elif choice == '3':
            mode = safe_input("Scoring mode ('manual' or 'auto'): ").strip().lower()
            if mode in ['manual', 'auto']:
                SCORING_MODE = mode
                config['SCORING_MODE'] = SCORING_MODE
                save_config(config)
                print(f"Scoring mode set to {SCORING_MODE}.")
            else:
                print("Invalid mode. Must be 'manual' or 'auto'.")
        elif choice == '4':
            current_setting = config.get('DISPLAY_WIFE_STRATEGY', False)
            config['DISPLAY_WIFE_STRATEGY'] = not current_setting
            save_config(config)
            print(f"Wife's strategy display is now {'ON' if not current_setting else 'OFF'}.")
        elif choice == '5':
            return
        else:
            print("Invalid choice.")

def play_turn(scoreboard):
    global current_player
    print("-" * 60)  # Separator at start of turn

    if current_player == "me":
        print("\n--- YOUR TURN ---")
        handle_player_turn()
    else:
        print("\n--- WIFE'S TURN ---")
        handle_wife_turn()

    calculate_probabilities()
    print_scores()

    if game_over_conditions_met():
        update_scores(scoreboard)
        end_game(scoreboard)

    current_player = "wife" if current_player == "me" else "me"
    print("-" * 60)  # Separator at end of turn

def deal():
    global my_hand, wife_hand, deck, wife_unknown_cards, discard_pile, current_player, INITIAL_HAND_COUNT
    reset_game_state()

    print("Dealing cards... You must input your starting cards.")
    my_hand[:] = get_starting_hand("your", INITIAL_HAND_COUNT)
    sort_hand(my_hand)

    wife_hand[:] = ["HIDDEN"] * INITIAL_HAND_COUNT
    wife_unknown_cards[:] = deal_to_wife(INITIAL_HAND_COUNT)

    print("From the remaining deck, choose the card that is flipped onto the discard pile:")
    top_card = choose_discard_pile_card()
    if top_card:
        discard_pile.append(top_card)
        print(f"Top card {display_card(top_card)} flipped to discard pile.")
    else:
        print("No card flipped onto discard pile.")

    print_game_state()
    set_initial_player()

def handle_player_turn():
    draw_phase()
    meld_phase()
    discard_phase()

def handle_wife_turn():
    wife_draw_action()
    wife_meld_action()
    wife_discard_action()

def draw_phase():
    print("Drawing phase...")
    recommend_draw_action()
    draw_source = get_choice("Draw from (deck/discard)? ", ['deck', 'discard'])
    draw_card(draw_source, my_hand)

def meld_phase():
    possible_melds = detect_melds(my_hand)
    if possible_melds:
        lay_down_meld(possible_melds)
    play_off_meld()

def discard_phase():
    if my_hand:
        recommend_discard()
        discard_card = get_valid_card_input("Discard a card: ", deck=my_hand)
        append_to_discard(discard_card)
        my_hand.remove(discard_card)
    else:
        print("No discard needed because your hand is empty.")

def print_scores():
    my_score, wife_score = current_scores()
    print(f"Scores - You: {my_score}, Wife: {wife_score}")

def reset_game_state():
    """Resets global variables for a new game."""
    global my_hand, wife_hand, deck, wife_unknown_cards, discard_pile, current_player, my_melds, wife_melds, forced_meld_card, need_final_discard
    my_hand.clear()
    wife_hand.clear()
    discard_pile.clear()
    my_melds.clear()
    wife_melds.clear()
    wife_unknown_cards.clear()
    forced_meld_card = None
    need_final_discard = {"me": False, "wife": False}
    random.shuffle(deck)

def get_starting_hand(player, count):
    """Prompts the user to input their starting hand."""
    while True:
        hand_input = safe_input(f"Enter {player} {count} cards: ").strip().upper().split(", ")
        if len(hand_input) != count:
            print(f"Please enter exactly {count} cards.")
            continue
        if all(card in deck for card in hand_input):
            for card in hand_input:
                deck.remove(card)
            return hand_input
        print("Invalid cards detected. Please try again.")

def deal_to_wife(count):
    """Deals a random hand to the wife from the deck."""
    sample = random.sample(deck, count)
    for card in sample:
        deck.remove(card)
    return sample

def choose_discard_pile_card():
    """Prompts for the top card of the discard pile."""
    return get_valid_card_input("Enter top card to flip or 'skip' to continue: ", deck=deck, allow_skip=True)

def print_game_state():
    """Prints the current game state after dealing."""
    print(f"Your hand (sorted, {len(my_hand)} cards): {display_hand(my_hand)}")
    print(f"Wife's hand: {len(wife_hand)} cards (hidden)")
    if discard_pile:
        print(f"Discard pile: {', '.join(display_card(c) for c in discard_pile)}")
    else:
        print("Discard pile is empty.")
    print(f"Remaining cards in deck: {len(deck)}")

def set_initial_player():
    """Sets the initial player based on who dealt the cards."""
    global current_player
    dealer = safe_input("Who dealt the cards? (you/wife): ").strip().lower()
    if dealer == "you":
        current_player = "wife"
        print("Since you dealt, your wife will start.")
    else:
        current_player = "me"
        print("Since your wife dealt, you will start.")

def wife_draws_card():
    global deck, wife_hand
    if deck:
        drawn_card = deck.pop(0)
        wife_hand.append("HIDDEN")  # Add a hidden card to wife's hand
        print("Your wife drew a card from the deck.")
        print(f"Remaining cards in deck: {len(deck)}")
    else:
        print("No cards left in the deck!")

def wife_draw_action():
    global deck, wife_hand, discard_pile, wife_known_cards
    draw_source = get_choice("Did your wife draw from deck or discard? ", ["deck", "discard"])
    if draw_source == "deck":
        if deck:
            wife_hand.append("HIDDEN")
            deck.pop(0)
            print("Your wife drew a card from the deck.")
        else:
            print("Deck is empty. No cards to draw.")
    else:  # Handle discard pile logic directly
        print(f"Discard pile: {', '.join(display_card(c) for c in discard_pile)}")
        picked_cards = safe_input("Enter cards your wife picked from the discard pile (e.g., '8D, TH'): ").strip().upper().split(", ")
        for card in picked_cards:
            if card in discard_pile:
                discard_pile.remove(card)
                wife_known_cards.append(card)
                wife_hand.append("HIDDEN")
            else:
                print(f"Warning: {card} is not in the discard pile.")
        print(f"Updated discard pile: {', '.join(display_card(c) for c in discard_pile)}")


def append_to_discard(card):
    """Adds a card to the discard pile only if it's not already the top card."""
    global discard_pile
    if discard_pile and card == discard_pile[-1]:
        print("You cannot discard the same card that is already on top of the pile.")
    else:
        discard_pile.append(card)
        print(f"Card {display_card(card)} added to the discard pile.")

def wife_discards_card():
    global discard_pile, wife_hand
    discarded_card = get_valid_card_input("Enter the card your wife discarded: ")
    wife_hand.pop()
    discard_pile.append(discarded_card)
    print(f"Card {display_card(discarded_card)} added to discard pile.")
    print(f"Updated discard pile: {', '.join(display_card(c) for c in discard_pile)}")

def wife_discard_action():
    global discard_pile, wife_hand, wife_known_cards, wife_unknown_cards
    discarded_card = get_valid_card_input("Enter the card your wife discarded: ")
    append_to_discard(discarded_card)
    if discarded_card in wife_known_cards:
        wife_known_cards.remove(discarded_card)
    elif discarded_card in wife_unknown_cards:
        wife_unknown_cards.remove(discarded_card)
    if wife_hand:
        wife_hand.pop()
    print(f"Card {display_card(discarded_card)} added to discard pile.")
    print(f"Updated discard pile: {', '.join(display_card(c) for c in discard_pile)}")

def draw_card(source, target):
    if source == "deck":
        card = deck.pop(0)
        target.append(card)
        print(f"Drew {display_card(card)} from the deck.")
    elif source == "discard":
        print(f"Discard pile: {', '.join(display_card(c) for c in discard_pile)}")
        card = get_valid_card_input("Which card to pick from discard pile? ", discard_pile=discard_pile)
        idx = discard_pile.index(card)
        taken_cards = discard_pile[idx:]
        discard_pile[:] = discard_pile[:idx]
        target.extend(taken_cards)
        print(f"Took {', '.join(display_card(c) for c in taken_cards)} from discard pile.")

def lay_down_meld(possible_melds):
    print("You have the following melds detected in your hand:")
    for i, m in enumerate(possible_melds, start=1):
        displayed_meld = ", ".join(display_card(card) for card in m)
        print(f"{i}) {displayed_meld}")
    choice = get_choice("Lay down a meld? (Enter number or 'n' to skip): ",
                        [str(i) for i in range(1, len(possible_melds) + 1)] + ["n"])
    if choice != "n":
        meld_index = int(choice) - 1
        chosen_meld = possible_melds[meld_index]
        for c in chosen_meld:
            my_hand.remove(c)
        my_melds.append(chosen_meld)
        displayed_meld = ", ".join(display_card(c) for c in chosen_meld)
        print(f"Meld laid down: {displayed_meld}")
        print(f"Your remaining hand: {display_hand(my_hand)}")

def play_off_meld():
    all_table_melds = [(f"Your meld #{i}", m) for i, m in enumerate(my_melds)] + \
                      [(f"Wife's meld #{i}", m) for i, m in enumerate(wife_melds)]
    if all_table_melds:
        playable_options = []
        for owner, meld in all_table_melds:
            for c in my_hand:
                new_meld = meld + [c]
                if is_valid_meld(new_meld):
                    playable_options.append((owner, meld, c))
        if playable_options:
            print("You can play off the following melds:")
            for i, (owner, meld, c) in enumerate(playable_options, start=1):
                meld_str = ", ".join(display_card(x) for x in meld)
                print(f"{i}) Add {display_card(c)} to {owner} ({meld_str})")
            choice = get_choice("Choose a play-off option or 'n' to skip: ",
                                [str(i) for i in range(1, len(playable_options) + 1)] + ["n"])
            if choice != "n":
                selected = playable_options[int(choice) - 1]
                owner, old_meld, card_to_add = selected
                if "Your meld" in owner:
                    idx = int(owner.split('#')[-1])
                    my_melds[idx].append(card_to_add)
                else:
                    idx = int(owner.split('#')[-1])
                    wife_melds[idx].append(card_to_add)
                my_hand.remove(card_to_add)
                print(f"Added {display_card(card_to_add)} to {owner}.")
        else:
            print("No cards can be played off the existing melds on the table.")


def wife_lays_down_meld():
    global wife_hand, wife_known_cards, wife_unknown_cards, wife_meld_count
    meld_input = safe_input("Enter wife's meld (e.g. '8H, 9H, 10H'): ").strip().upper().split(", ")
    from utils import is_valid_meld, display_card
    if len(meld_input) <= len(wife_hand) and is_valid_meld(meld_input):
        for _ in meld_input:
            if wife_hand:
                wife_hand.pop()

        for c in meld_input:
            if c in wife_unknown_cards:
                wife_unknown_cards.remove(c)
            if c in wife_known_cards:
                wife_known_cards.remove(c)

        displayed_meld = ", ".join(display_card(card) for card in meld_input)
        print(f"Wife laid down: {displayed_meld}")
        print(f"Remaining in wife's hand: {len(wife_hand)}")
        wife_melds.append(meld_input)
        wife_meld_count += 1
    else:
        print("Error laying down wife's meld.")

def wife_meld_action():
    if get_yes_no("Did your wife lay down melds? (y/n): ") == "y":
        wife_lays_down_meld()


def calculate_probabilities():
    try:
        # Existing probability calculation logic
        player_completion_potential = sum(
            1 for card in my_hand if any(card[:-1] in meld_card for meld_card in my_melds)
        )
        wife_completion_potential = sum(
            1 for card in wife_known_cards if any(card[:-1] in meld_card for meld_card in wife_melds)
        )

        # Avoid division by zero
        total_potential = player_completion_potential + wife_completion_potential or 1
        player_prob = player_completion_potential / total_potential
        wife_prob = wife_completion_potential / total_potential

        print(f"Estimated win probability - You: {player_prob:.2f}, Wife: {wife_prob:.2f}")

    except Exception as e:
        print(f"Error calculating probabilities: {e}")


def recommend_discard():
    melds = detect_melds(my_hand)
    cards_in_melds = {c for m in melds for c in m}
    for c in my_hand:
        if c not in cards_in_melds:
            print(f"Recommendation: Discard {display_card(c)}, doesn't fit a meld.")
            return
    if my_hand:
        print(f"Recommendation: Discard {display_card(my_hand[-1])}, all cards seem useful.")

def recommend_draw_action():
    """Enhanced recommendation for where to draw from."""
    melds_before = detect_melds(my_hand)
    best_move = "deck"
    if discard_pile:
        top_card = discard_pile[-1]
        temp_hand = my_hand + [top_card]
        melds_after = detect_melds(temp_hand)
        if len(melds_after) > len(melds_before):
            best_move = "discard"
    # Additional logic based on probabilities
    useful_discard_cards = [
        card for card in discard_pile if any(card[:-1] == meld_card[:-1] for meld_card in my_hand)
    ]
    if useful_discard_cards:
        best_move = "discard"
        print(f"Recommendation: Draw from discard pile. Useful cards: {', '.join(display_card(c) for c in useful_discard_cards)}")
    else:
        print(f"Recommendation: Draw from the {best_move}.")

def current_scores():
    my_score = sum(card_value(c) for m in my_melds for c in m)
    wife_score = sum(card_value(c) for m in wife_melds for c in m)
    return my_score, wife_score

def update_scores(scoreboard):
    """Update scores for the current round."""
    # Automatically calculate scores
    my_leftover = sum(card_value(c) for c in my_hand)
    wife_leftover = sum(card_value(c) for c in wife_hand + wife_known_cards + wife_unknown_cards if c != 'HIDDEN')

    calculated_my_score = my_leftover
    calculated_wife_score = wife_leftover

    print(f"\nCalculated scores for this round:")
    print(f"  Your score: {calculated_my_score}")
    print(f"  Wife's score: {calculated_wife_score}")

    if SCORING_MODE == "manual":
        print("\nYou can override the calculated scores if necessary.")
        my_score = int(safe_input(f"Enter your score (default {calculated_my_score}): ").strip() or calculated_my_score)
        wife_score = int(safe_input(f"Enter wife's score (default {calculated_wife_score}): ").strip() or calculated_wife_score)
    else:  # In auto mode, use calculated scores
        my_score = calculated_my_score
        wife_score = calculated_wife_score

    # Update scoreboard
    scoreboard.add_score("me", my_score)
    scoreboard.add_score("wife", wife_score)

    print("\nScores updated:")
    scoreboard.display_scores()


def check_win_condition():
    if not my_hand and not need_final_discard["me"]:
        end_game()
    if not wife_hand and not need_final_discard["wife"]:
        end_game()

def append_game_history(my_score, wife_score, winner):
    if config.get('TEST_MODE', False):
        print("TEST MODE: Not writing to CSV.")
        return
    file_path = GAME_HISTORY_FILE
    file_exists = os.path.exists(file_path)

    with open(file_path, mode="a", newline="") as csvfile:
        import csv
        writer = csv.writer(csvfile)
        if not file_exists:
            writer.writerow(["Game Number", "My Score", "Wife's Score", "Winner"])

        if file_exists:
            with open(file_path, mode="r") as readfile:
                reader = csv.reader(readfile)
                rows = list(reader)
                game_number = len(rows)
        else:
            game_number = 1

        writer.writerow([game_number, my_score, wife_score, winner])

def generate_pdf_report():
    if config.get('TEST_MODE', False):
        print("TEST MODE: Not generating PDF report.")
        return
    file_path = GAME_HISTORY_FILE
    if not os.path.exists(file_path):
        print("No history file found, no PDF generated.")
        return
    with open(file_path, mode="r") as csvfile:
        import csv
        reader = csv.reader(csvfile)
        rows = list(reader)

    headers = rows[0]
    data_rows = rows[1:]

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "Rummy Game History", ln=True, align="C")

    pdf.ln(10)
    pdf.set_font("Arial", "", 12)

    col_width = pdf.w / len(headers) - 10
    for header in headers:
        pdf.cell(col_width, 10, header, 1, 0, "C")
    pdf.ln(10)

    for row in data_rows:
        for item in row:
            pdf.cell(col_width, 10, item, 1, 0, "C")
        pdf.ln(10)

    pdf.output("data/game_summary.pdf")

def game_over_conditions_met():
    global need_final_discard, my_hand, wife_hand

    if not my_hand and not wife_hand and not (need_final_discard["me"] or need_final_discard["wife"]):
        return True

    return False


def end_game(scoreboard):
    print("\nThe game has ended!")
    scoreboard.display_scores()

    my_total = scoreboard.get_total_score("me")
    wife_total = scoreboard.get_total_score("wife")
    winner = "Tie" if my_total == wife_total else "Me" if my_total < wife_total else "Wife"

    print(f"\nFinal Scores - You: {my_total}, Wife: {wife_total}")
    print(f"Winner: {winner}")

    # Log to CSV and generate PDF
    append_game_history(my_total, wife_total, winner)
    generate_pdf_report()
    global game_active
    game_active = False

if __name__ == "__main__":
    main()
