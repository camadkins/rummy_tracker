class WifeLogic:
    def __init__(self):
        self.known_cards = []  # Cards we know are in her hand
        self.melds = []  # Her known melds

    def update_known_cards(self, card, action="add"):
        """Update the list of known cards in her hand."""
        if action == "add" and card not in self.known_cards:
            self.known_cards.append(card)
        elif action == "remove" and card in self.known_cards:
            self.known_cards.remove(card)

    def add_meld(self, meld):
        """Add a new meld to her known melds."""
        self.melds.append(meld)

    def analyze_discard(self, card):
        """Analyze why she might have discarded a specific card."""
        # Check if the card fits any potential melds
        for meld in self.melds:
            if card in meld:
                return f"Discarded {card}, possibly breaking a meld."  # Unlikely, but worth noting

        # Check if it's a high-value card
        high_value = card[0] in "TJQK"
        if high_value:
            return f"Discarded {card}, possibly minimizing points in case of a loss."

        return f"Discarded {card}, likely not useful for her meld plans."

    def analyze_draw(self, cards):
        """Analyze why she might have drawn specific cards."""
        if isinstance(cards, str):
            cards = [cards]  # Convert single card to a list

        potential_melds = []
        for card in cards:
            rank = card[:-1]
            suit = card[-1]

            # Check if the drawn card complements any known melds
            for meld in self.melds:
                if any(c[:-1] == rank for c in meld) or any(c[-1] == suit for c in meld):
                    potential_melds.append((card, meld))

        if potential_melds:
            return f"Drew {', '.join(cards)}, possibly building towards melds: {potential_melds}"

        return f"Drew {', '.join(cards)}, likely aiming to complete unknown melds."

    def summary(self):
        return {
            "known_cards": self.known_cards,
            "melds": self.melds,
        }

    def predict_strategy(self):
        summary = ""
        if len(self.known_cards) < 5:
            summary += "Her hand likely contains cards unknown to us, making her moves less predictable. "
        else:
            summary += "She is building on visible patterns, possibly trying to form a run or set. "

        if self.melds:
            summary += "She has at least one meld laid down, indicating she might be advancing toward victory. "
        else:
            summary += "She has no melds laid down yet, possibly holding high-value cards. "

        return summary
