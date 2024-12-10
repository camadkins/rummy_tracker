import pytest
import tracker

def test_initial_globals():
    assert isinstance(tracker.deck, list)
    assert isinstance(tracker.my_hand, list)
    assert isinstance(tracker.wife_hand, list)
    assert isinstance(tracker.discard_pile, list)

def test_append_game_history(tmp_path, monkeypatch):
    # Test append_game_history by redirecting CSV file to a temporary directory
    d = tmp_path / "data"
    d.mkdir()
    monkeypatch.setattr(tracker, "GAME_HISTORY_FILE", str(d / "game_history.csv"))

    tracker.append_game_history("10","20","Wife")  # This should create the CSV
    # Check if file was created and contains expected data
    file_path = d / "game_history.csv"
    assert file_path.exists()
    content = file_path.read_text().strip().split("\n")
    # First line should be headers, second line should be game data
    assert "Game Number,My Score,Wife's Score,Winner" in content[0]
    assert "1,10,20,Wife" in content[1]

