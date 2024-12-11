class Scoreboard:
    def __init__(self):
        self.scores = {"me": [], "wife": []}

    def add_score(self, player, score):
        if player in self.scores:
            self.scores[player].append(score)

    def adjust_score(self, player, round_index, new_score):
        if player in self.scores and 0 <= round_index < len(self.scores[player]):
            self.scores[player][round_index] = new_score

    def get_total_score(self, player):
        return sum(self.scores[player])

    def display_scores(self):
        print("\nScoreboard:")
        print("Round   You   Wife")
        for i in range(len(self.scores["me"])):
            me_score = self.scores["me"][i] if i < len(self.scores["me"]) else "N/A"
            wife_score = self.scores["wife"][i] if i < len(self.scores["wife"]) else "N/A"
            print(f"  {i+1:2d}   {me_score:4d}  {wife_score:4d}")
