# Rummy Card Tracker

#### Video Demo: *[URL]*

#### Description
This Rummy Card Tracker is designed to help **me** improve my Rummy game against my wife. Over time, I’ve enhanced it to provide strategic guidance, automatically handle gameplay steps, log game histories, and offer a flexible configuration system. While I built it for myself, anyone who wants a helping hand in two-player Rummy can benefit from its features.

---

## Features

### **Menu-Driven Interface**
- Start a new game, view help, adjust settings, or quit from a simple main menu.

### **Persistent Configuration via YAML**
Key options are stored in `config.yaml` for consistency across sessions:
- **Test Mode**: No game results are saved to CSV or PDF if enabled.
- **Initial Hand Count**: Choose to deal 5, 7, or 10 cards at the start of a game.
- **Scoring Mode**: Select `manual` (enter scores at game end) or `auto` (calculate winner based on leftover card points).
- **Wife’s Strategy Display**: Toggle the visibility of her predicted strategy during gameplay.

### **Game State Tracking and Display**
- Manage dealt cards, my hand, and the discard pile.
- Track my wife’s known and unknown cards.
- Unicode suits (`♠, ♥, ♦, ♣`) improve card readability in terminal outputs.
- Separators (`------------------------------------------------------------`) between turns for easy game flow navigation.

### **Heuristic Probability and Recommendations**
- Calculates probabilities of winning for both players after each turn.
- Provides recommendations for optimal moves, including:
  - **Draw Recommendations**: Whether to draw from the deck or discard pile.
  - **Discard Recommendations**: Which card is least valuable or most harmful to keep.

### **Meld Logic and Conditional Prompts**
- Prompts for laying down melds and playing off existing melds only when relevant.
- Lists possible melds in-hand to simplify decision-making.

### **Wife’s Strategy Insights**
- Tracks her known cards and melds, analyzing why she draws or discards specific cards.
- Provides a predicted strategy, helping me make more informed moves.

### **Turn-Based Flow**
- Automates each turn step (drawing, melding, discarding) and prompts only when needed.
- Prevents skipping discard unless my hand is empty.

### **Scoring and Game End**
- **Manual Mode**: Enter final scores at the end of the game.
- **Auto Mode**: Automatically calculate winner based on leftover card points.
- Results are logged in a CSV file, and a PDF summary is generated unless in test mode.

### **Quit Anytime**
- Type `quit` or `exit` at any prompt outside the main menu to immediately end the program.

---

## How to Run

1. Clone the repository and install dependencies:
   ```bash
   pip install pyyaml fpdf
   ```
2. Navigate to the project folder.
3. Run the program:
   ```bash
   python tracker.py
   ```
4. Main menu options:
   - `1`: Start a new game (deal cards).
   - `2`: View help.
   - `3`: Adjust settings (test mode, hand count, scoring mode, wife’s strategy display).
   - `4`: Quit.

---

## Interaction and Guidance

- **Automatic Guidance**: Turn actions are handled step-by-step, prompting only for relevant decisions.
- **Strategic Recommendations**: Receive optimal move suggestions based on the game state.
- **Dynamic Prompts**: Only see options for laying down or playing off melds when applicable.

---

## New Features

### **WifeLogic Class**
- Tracks her known cards and melds.
- Analyzes her actions, offering insights into her strategy.
- Helps predict her next moves, guiding me to counter strategically.

### **Probability Enhancements**
- Includes her meld progress and unknown cards for better estimation.

### **Improved Validation and Error Prevention**
- Prevents duplicate discards.
- Validates draw and discard actions for consistency.

### **Streamlined Gameplay Flow**
- Automatically integrates her strategy insights into the turn rotation.
- Configurable display for wife’s strategy (toggleable via options menu).

---

## Additional Commands (Optional)

- **Manual Updates**:
  - `update_hand`, `update_discard`, `wife_picks_discard`, `wife_draws_card`, `wife_discards_card` allow manual adjustments.
- **Manual Recommendations**:
  - `recommend_discard`, `recommend_draw_action` for recalculated suggestions.
- **Meld Logic**:
  - `suggest_melds`, `calculate_probabilities` for manual intervention.
- **End Game**:
  - `end_game` to finish and log the game early.

---

## Remaining Tasks

- **Undo Functionality**: Allow undoing the last action during a turn.
- **Advanced Strategy Analysis**: Enhance the `WifeLogic` class with deeper insights into meld-building and discard patterns.
- **GUI Transition**: Develop a graphical interface for improved user experience.
- **Expanded Testing**: Strengthen edge case handling through rigorous testing.
- **Rummy Variants**: Add support for advanced Rummy rule sets and scoring.

## Changelog

- Started the project.
- Implemented initial structure and integrated files (`tracker.py`, `utils.py`, `README.md`, `data/game_history.csv`).
- Added basic commands (`dealt_cards`, `process_command`) and initial logic for state tracking.
- Updated `README.md` to reflect initial usage and features.
- Implemented meld detection and logic for laying down melds.
- Introduced heuristic probability calculations to estimate which player is closer to winning.
- Established a turn-based structure to automate the draw, meld, and discard phases.
- Improved wife’s card handling, differentiating known and unknown cards.
- Implemented `end_game()` function to prompt for final scores and log results to a CSV file.
- Generated a PDF summary of game history using `fpdf`.
- Added `recommend_discard` and `recommend_draw_action` for heuristic guidance.
- Enforced the forced meld card rule when taking multiple cards from the discard pile.
- Allowed choosing a card to flip onto the discard pile at the start of the game.
- Enhanced turn prompts to “YOUR TURN” and “WIFE’S TURN” for clarity.
- Added `exit` as an alias for `quit` to end the program.
- Renamed `dealt_cards` to a menu-driven `deal` option for starting new games.
- Defaulted to dealing 7 cards without repeatedly asking each time.
- Implemented dealer selection logic to determine who starts each game.
- Added strict input validation and re-prompting for dealing and flipping the discard card.
- Moved sorting, meld checking, and card evaluation logic into `utils.py` for better organization.
- Created `test_utils.py` and `test_tracker.py` for basic testing and validation.
- Used Unicode suits (`♠, ♥, ♦, ♣`) to improve card readability and output clarity.
- Enhanced the help menu and standardized prompts throughout the program.
- Only prompted for melds and playing off melds if actually applicable to the current situation.
- Improved user feedback on invalid inputs, no meld scenarios, and empty deck conditions.
- Reduced reliance on manual commands by providing a step-by-step guided flow.
- Added separators between turns to make the terminal output easier to follow.
- Allowed quitting at any prompt (outside the main menu) by typing `quit` or `exit`.
- Prevented skipping the discard step unless my hand is actually empty.
- Introduced `config.yaml` to store persistent configuration options between sessions.
- Added an options menu accessible from the main menu to toggle test mode, set initial hand count (5/7/10), and choose scoring mode (manual/auto).
- In test mode, prevented writing results to CSV/PDF for a safe testing environment.
- Implemented auto scoring mode, which calculates leftover card points at the end of the game to determine the winner automatically.
- Added a WifeLogic class in wife_logic.py to analyze her gameplay decisions.
- Integrated wife’s strategy analysis into tracker.py for discard and draw actions.
- Added an option to toggle the display of her strategy in the options menu.
- Updated the configuration file (config.yaml) to persist the DISPLAY_WIFE_STRATEGY setting.
- Enhanced the probability calculation to include her meld progress and unknown cards.
- Added error prevention to avoid duplicate discards in the discard pile.
- Improved input validation for wife’s draw and discard actions.
- Streamlined gameplay flow to automatically include wife’s strategy analysis without requiring manual prompts.
- Refactored turn-based logic for better clarity and maintainability.
