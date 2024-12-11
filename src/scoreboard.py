class Scoreboard:
    def __init__(self):
        self.scores = {"me": 0, "wife": 0}

    def update_score(self, player, points):
        if player in self.scores:
            self.scores[player] += points

    def display_scores(self):
        print(f"Current Scores: Me: {self.scores['me']} | Wife: {self.scores['wife']}")

    def get_total_score(self, player):
        return self.scores.get(player, 0)
