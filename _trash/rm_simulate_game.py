import random
from tracker import (
    deal, detect_melds, card_value, calculate_probabilities, update_scores,
    end_game, current_scores, my_hand, wife_hand, discard_pile, deck,
    my_melds, wife_melds, game_active, current_player, scoreboard, SCORING_MODE,
)
from utils import sort_hand, display_card

# Randomized decision functions
def simulate_draw_action():
    """Randomly decide where to draw from."""
    draw_choices = ["deck", "discard"]
    weights = [0.7, 0.3]  # Favor deck slightly
    return random.choices(draw_choices, weights=weights, k=1)[0]

def simulate_discard(hand):
    """Randomly decide which card to discard."""
    if not hand:
        return None
    non_meld_cards = [card for card in hand if card not in {c for meld in detect_melds(hand) for c in meld}]
    discard_pool = non_meld_cards if non_meld_cards else hand
    return random.choice(discard_pool)

def simulate_meld_laying(hand):
    """Decide whether to lay down melds with some probability."""
    possible_melds = detect_melds(hand)
    if possible_melds and random.random() < 0.8:  # 80% chance to lay down melds
        return random.choice(possible_melds)
    return None

def simulate_wife_turn():
    global wife_hand, discard_pile
    draw_source = simulate_draw_action()
    if draw_source == "deck" and deck:
        wife_hand.append(deck.pop(0))
    elif discard_pile:
        wife_hand.append(discard_pile.pop())

    meld = simulate_meld_laying(wife_hand)
    if meld:
        for card in meld:
            wife_hand.remove(card)
        wife_melds.append(meld)

    if wife_hand:
        discard_card = simulate_discard(wife_hand)
        if discard_card:
            wife_hand.remove(discard_card)
            discard_pile.append(discard_card)

def simulate_player_turn():
    """Simulate the player's turn in the game."""
    global my_hand, discard_pile

    # Simulate drawing a card
    draw_source = simulate_draw_action()  # Randomly decides between "deck" or "discard"
    if draw_source == "deck" and deck:
        drawn_card = deck.pop(0)
        my_hand.append(drawn_card)
        print(f"Me drew {display_card(drawn_card)} from deck.")
    elif discard_pile:
        drawn_card = discard_pile.pop()
        my_hand.append(drawn_card)
        print(f"Me drew {display_card(drawn_card)} from discard pile.")

    # Simulate laying down a meld
    meld = simulate_meld_laying(my_hand)
    if meld:
        for card in meld:
            my_hand.remove(card)
        my_melds.append(meld)
        print(f"Me laid down meld: {meld}")

    # Simulate discarding a card
    discard_card = simulate_discard(my_hand)
    if discard_card:
        my_hand.remove(discard_card)
        discard_pile.append(discard_card)
        print(f"Me discarded {discard_card}.")

def simulate_game():
    global current_player, game_active

    deal(simulate=True)  # Deal initial hands for simulation

    print(f"Dealt hands: Player - {my_hand}, Wife - {len(wife_hand)} cards hidden.")
    print(f"Top of discard pile: {display_card(discard_pile[-1])}\n")

    while game_active:
        # Terminate if the deck is empty and no valid actions are possible
        if not deck and not discard_pile:
            print("Deck is empty, and no valid moves are possible. Ending game.")
            game_active = False
            break

        if current_player == "me":
            print("--- PLAYER'S TURN ---")
            # Simulate player's turn
            simulate_player_turn()
        else:
            print("--- WIFE'S TURN ---")
            simulate_wife_turn()

        # Update probabilities
        calculate_probabilities()

        # Check win conditions
        if not my_hand:
            print("Player has no cards left. Player wins!")
            game_active = False
        elif not wife_hand:
            print("Wife has no cards left. Wife wins!")
            game_active = False

        # Switch turns
        current_player = "wife" if current_player == "me" else "me"

    print("Game over. Final scores:")
    update_scores(scoreboard)


if __name__ == "__main__":
    simulate_game()
