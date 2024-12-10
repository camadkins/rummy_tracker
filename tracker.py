import csv
from fpdf import FPDF
import os
import random
import sys

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

ranks = ["A","2","3","4","5","6","7","8","9","T","J","Q","K"]
suits = ["S","H","D","C"]
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
                play_turn()
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
        print("4) Return to main menu")
        choice = safe_input("Choose an option (1/2/3/4): ").strip()
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
            if mode in ['manual','auto']:
                SCORING_MODE = mode
                config['SCORING_MODE'] = SCORING_MODE
                save_config(config)
                print(f"Scoring mode set to {SCORING_MODE}.")
            else:
                print("Invalid mode. Must be 'manual' or 'auto'.")
        elif choice == '4':
            return
        else:
            print("Invalid choice.")


def play_turn():
    global current_player, my_hand, wife_hand, discard_pile, my_melds, wife_melds, need_final_discard
    print("-" * 60)  # Separator at start of turn

    if current_player == "me":
        print("\n--- YOUR TURN ---")
        if TEST_MODE:
            print("(Test Mode: No results will be saved.)")

        recommend_draw_action()
        draw_source = get_choice("Draw from (deck/discard)? ", ['deck','discard'])

        if draw_source == "deck":
            card = get_valid_card_input("Enter the card you drew: ", deck=deck)
            my_hand.append(card)
            deck.remove(card)
            sort_hand(my_hand)
            print(f"Card {display_card(card)} added.")
            print(f"Your hand ({len(my_hand)} cards): {display_hand(my_hand)}")
            print(f"Remaining deck: {len(deck)}")
        else:  # discard
            print(f"Discard pile: {', '.join(display_card(c) for c in discard_pile)}")
            card = get_valid_card_input("Which card in discard pile to pick? ", discard_pile=discard_pile)
            idx = discard_pile.index(card)
            taken_cards = discard_pile[idx:]
            discard_pile[:] = discard_pile[:idx]
            my_hand.extend(taken_cards)
            sort_hand(my_hand)
            print(f"You took {', '.join(display_card(c) for c in taken_cards)} from discard.")
            print(f"Your hand ({len(my_hand)} cards): {display_hand(my_hand)}")
            print(f"Discard pile: {', '.join(display_card(c) for c in discard_pile)}")

        possible_melds = detect_melds(my_hand)
        if possible_melds:
            print("You have the following melds detected in your hand:")
            for i, m in enumerate(possible_melds, start=1):
                displayed_meld = ", ".join(display_card(card) for card in m)
                print(f"{i}) {displayed_meld}")
            choice = get_choice("Lay down a meld? (Enter number or 'n' to skip): ",
                                [str(i) for i in range(1,len(possible_melds)+1)] + ['n'])
            if choice != 'n':
                meld_index = int(choice)-1
                chosen_meld = possible_melds[meld_index]
                for c in chosen_meld:
                    my_hand.remove(c)
                my_melds.append(chosen_meld)
                displayed_meld = ", ".join(display_card(c) for c in chosen_meld)
                print(f"Meld laid down: {displayed_meld}")
                print(f"Your remaining hand: {display_hand(my_hand)}")
        else:
            print("No possible melds to lay down this turn.")

        all_table_melds = [(f"Your meld #{i}", m) for i,m in enumerate(my_melds)] + \
                          [(f"Wife's meld #{i}", m) for i,m in enumerate(wife_melds)]
        if all_table_melds:
            playable_options = []
            for owner,meld in all_table_melds:
                for c in my_hand:
                    new_meld = meld + [c]
                    if is_valid_meld(new_meld):
                        playable_options.append((owner, meld, c))

            if playable_options:
                print("You can play off the following melds:")
                for i,(owner,meld,c) in enumerate(playable_options, start=1):
                    meld_str = ", ".join(display_card(x) for x in meld)
                    print(f"{i}) Add {display_card(c)} to {owner} ({meld_str})")

                choice = get_choice("Choose a play-off option or 'n' to skip: ",
                                    [str(i) for i in range(1,len(playable_options)+1)] + ['n'])
                if choice != 'n':
                    selected = playable_options[int(choice)-1]
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
        else:
            print("No melds on the table to play off of.")

        if not my_hand:
            need_final_discard["me"] = True

        # Discard phase: must discard if you have cards
        if my_hand:
            recommend_discard()
            while True:
                discard_card = safe_input("Discard a card: ").strip().upper()
                if discard_card in my_hand:
                    my_hand.remove(discard_card)
                    discard_pile.append(discard_card)
                    break
                else:
                    print("You must discard a valid card from your hand.")
        else:
            print("No discard needed because your hand is empty.")

    else:
        print("\n--- WIFE'S TURN ---")
        wife_draw_source = get_choice("Did wife draw from deck or discard? ", ['deck','discard'])
        if wife_draw_source == 'deck':
            wife_draws_card()
        else:
            wife_picks_discard()

        if get_yes_no("Did wife lay down melds? (y/n): ") == 'y':
            wife_lays_down_meld()

        if not wife_hand:
            need_final_discard["wife"] = True

        if wife_hand:
            print("Wife must discard a card now.")
            discarded_card = get_valid_card_input("Enter the card your wife discarded: ")
            if wife_hand:
                wife_hand.pop()
                discard_pile.append(discarded_card)
                if discarded_card in wife_known_cards:
                    wife_known_cards.remove(discarded_card)
                elif discarded_card in wife_unknown_cards:
                    wife_unknown_cards.remove(discarded_card)
                print(f"Card {display_card(discarded_card)} added to discard pile.")
                print(f"Updated discard pile: {', '.join(display_card(c) for c in discard_pile)}")
            else:
                print("No cards in wife's hand to discard!")

    calculate_probabilities()
    my_score, wife_score = current_scores()
    print(f"Scores - You: {my_score}, Wife: {wife_score}")
    check_win_condition()

    current_player = "wife" if current_player == "me" else "me"
    print("-" * 60)  # Separator at end of turn

def deal():
    global my_hand, wife_hand, deck, wife_unknown_cards, discard_pile, current_player, INITIAL_HAND_COUNT
    my_hand.clear()
    wife_hand.clear()
    discard_pile.clear()
    global forced_meld_card, my_melds, wife_melds, wife_meld_count, need_final_discard
    forced_meld_card = None
    my_melds.clear()
    wife_melds.clear()
    wife_meld_count = 0
    need_final_discard = {"me": False, "wife": False}

    ranks = ["A","2","3","4","5","6","7","8","9","T","J","Q","K"]
    suits = ["S","H","D","C"]
    global deck
    deck = [f"{r}{s}" for r in ranks for s in suits]

    print("Dealing cards... You must input your starting cards.")
    while True:
        my_hand_input = safe_input(f"Enter your {INITIAL_HAND_COUNT} cards: ").strip().upper().split(", ")
        if len(my_hand_input) != INITIAL_HAND_COUNT:
            print(f"Please enter exactly {INITIAL_HAND_COUNT} cards.")
            continue
        all_valid = True
        for card in my_hand_input:
            if card not in deck:
                print(f"Warning: {card} is not in the deck.")
                all_valid = False
        if not all_valid:
            print("Some cards were invalid. Please re-enter your hand.")
            continue
        my_hand[:] = my_hand_input
        break

    sort_hand(my_hand)
    num_wife_cards = INITIAL_HAND_COUNT
    wife_hand[:] = ["HIDDEN"] * num_wife_cards

    for card in my_hand:
        deck.remove(card)

    if num_wife_cards > len(deck):
        print("Error: Not enough cards in the deck to deal to your wife.")
    else:
        wife_cards_sample = random.sample(deck, num_wife_cards)
        for w_card in wife_cards_sample:
            deck.remove(w_card)
        wife_unknown_cards[:] = deck[:]

    print("From the remaining deck, choose the card that is flipped onto the discard pile:")
    top_card = get_valid_card_input("Enter top card to flip or 'skip' to continue: ", deck=deck, allow_skip=True)
    if top_card:
        deck.remove(top_card)
        discard_pile[:] = [top_card]
        print(f"Top card {display_card(top_card)} flipped to discard pile.")
    else:
        discard_pile.clear()
        print("No card flipped onto discard pile.")

    print(f"Your hand (sorted, {len(my_hand)} cards): {display_hand(my_hand)}")
    print(f"Wife's hand: {len(wife_hand)} cards (hidden)")
    if discard_pile:
        print(f"Discard pile: {', '.join(display_card(c) for c in discard_pile)}")
    else:
        print("Discard pile is empty.")
    print(f"Remaining cards in deck: {len(deck)}")

    dealer = safe_input("Who dealt the cards? (you/wife): ").strip().lower()
    if dealer == "you":
        current_player = "wife"
        print("Since you dealt, your wife will start.")
    else:
        current_player = "me"
        print("Since your wife dealt, you will start.")

    # Call play_turn once initially
    play_turn()

def wife_picks_discard():
    # Using logic in play_turn steps
    pass

def wife_draws_card():
    # Already implemented in play_turn steps
    pass

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

def calculate_probabilities():
    melds = detect_melds(my_hand)
    my_meld_count = len(melds)
    global wife_meld_count
    total_melds = my_meld_count + wife_meld_count
    if total_melds == 0:
        my_probability = 0.5
        her_probability = 0.5
    else:
        my_probability = my_meld_count / total_melds
        her_probability = wife_meld_count / total_melds

    print(f"Estimated win probability - You: {my_probability:.2f}, Wife: {her_probability:.2f}")

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
    melds_before = detect_melds(my_hand)
    best_move = "deck"
    if discard_pile:
        top_card = discard_pile[-1]
        temp_hand = my_hand + [top_card]
        melds_after = detect_melds(temp_hand)
        if len(melds_after) > len(melds_before):
            best_move = "discard"
    print(f"Recommendation: Draw from the {best_move}.")

def current_scores():
    my_score = sum(card_value(c) for m in my_melds for c in m)
    wife_score = sum(card_value(c) for m in wife_melds for c in m)
    return my_score, wife_score

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

def end_game():
    global game_active, SCORING_MODE, TEST_MODE
    print("The game has ended!")

    if SCORING_MODE == "manual":
        # Manual scoring as before
        my_final_score = safe_input("Enter your final score: ").strip()
        wife_final_score = safe_input("Enter your wife's final score: ").strip()

        if int(my_final_score) < int(wife_final_score):
            winner = "Me"
        elif int(wife_final_score) < int(my_final_score):
            winner = "Wife"
        else:
            winner = "Tie"
    else:
        # Auto scoring: leftover points in each hand
        my_leftover = sum(card_value(c) for c in my_hand)
        wife_leftover = sum(card_value(c) for c in wife_hand)
        print(f"Auto Scoring: Leftover points -> You: {my_leftover}, Wife: {wife_leftover}")
        if my_leftover < wife_leftover:
            winner = "Me"
        elif wife_leftover < my_leftover:
            winner = "Wife"
        else:
            winner = "Tie"
        my_final_score = str(my_leftover)
        wife_final_score = str(wife_leftover)

    append_game_history(my_final_score, wife_final_score, winner)
    generate_pdf_report()

    if not TEST_MODE:
        print("Game results saved. PDF summary generated in 'data/game_summary.pdf'.")
    else:
        print("TEST MODE: No results saved.")

    game_active = False

if __name__ == "__main__":
    main()
