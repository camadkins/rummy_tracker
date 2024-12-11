from src.scoreboard import Scoreboard

def test_scoreboard():
    sb = Scoreboard()
    sb.add_score("me", 10)
    assert sb.get_total_score("me") == 10
    sb.add_score("wife", 15)
    assert sb.get_total_score("wife") == 15
