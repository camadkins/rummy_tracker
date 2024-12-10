# Rummy Card Tracker

#### Video Demo: *[URL]*

#### Description
This Rummy Card Tracker is designed to help **me** improve my Rummy game against my wife. Over time, I’ve enhanced it to provide strategic guidance, automatically handle gameplay steps, log game histories, and offer a flexible configuration system. While I built it for myself, anyone who wants a helping hand in two-player Rummy can benefit from its features.

## Features

- **Menu-Driven Interface**:
  On startup, a main menu offers options to start a new game, view help, quit, or configure settings. This makes it easy for me to jump right into a game or adjust options before playing.

- **Persistent Configuration via YAML**:
  A `config.yaml` file stores key options between sessions:
  - **Test Mode**: If enabled, no game results are saved to CSV/PDF.
  - **Initial Hand Count**: Choose from 5, 7, or 10 cards to be dealt initially.
  - **Scoring Mode**: Set to `manual` or `auto`. In `manual` mode, I enter final scores at game end. In `auto` mode, the program calculates leftover points in each player’s hand to determine the winner.

- **Game State Tracking and Display**:
  The program manages dealt cards, my hand, and the discard pile. My wife’s cards remain hidden but the program infers possible information about them.
  Cards are displayed using Unicode suits (`♠, ♥, ♦, ♣`) for easy readability. Separators (`------------------------------------------------------------`) appear between turns to help me distinguish the flow of the game state.

- **Heuristic Probability and Recommendations**:
  After each turn, it calculates which player is closer to winning and suggests optimal moves such as where to draw or which card to discard, saving me from guesswork.

- **Meld Logic and Conditional Prompts**:
  Only prompts me to lay down melds if I have any, showing a list of possible melds.
  Similarly, I only see prompts for playing off melds if melds exist on the table **and** I have cards that can extend them.

- **Turn-Based Flow with Guidance**:
  The program automates each turn—drawing, melding, discarding—prompting me only when necessary. If I have no melds, it doesn’t ask. If I can’t play off melds, it skips that step. This keeps the game flow smooth and clutter-free.

- **Scoring at Game End**:
  At the end of a game:
  - **Manual Mode**: I enter final scores.
  - **Auto Mode**: It calculates leftover card points for both players and decides the winner by who has fewer leftover points.

  Results are logged in a CSV file, and a PDF summary is generated—unless test mode is on, in which case no logs or PDFs are produced.

- **Quit Anytime**:
  Type `quit` or `exit` at any prompt (outside the main menu) to immediately end the program.

## How to Run

1. Clone the repository and install any dependencies (e.g. `pip install pyyaml fpdf`).
2. Navigate to the project folder.
3. Run:
   ```bash
   python tracker.py
   ```
4. From the main menu:
   - `1`: Start a new game (deal cards).
   - `2`: View help.
   - `3`: Options menu (configure test mode, initial hand count, and scoring mode).
   - `4`: Quit.

   After dealing a game, follow on-screen prompts. The program guides me through each turn. I can quit at any prompt by typing `quit` or `exit`.

## Interaction and Guidance

- Each turn is clearly separated, and I’m prompted only for relevant actions.
- Meld and play-off prompts only appear if I can actually perform those actions.
- Recommendations for drawing and discarding appear automatically.
- No skipping discard unless my hand is empty, ensuring realistic gameplay.

## Additional Commands (Rarely Needed)

- **update_hand**, **update_discard**, **wife_picks_discard**, **wife_draws_card**, **wife_discards_card**: Manually adjust the state if something gets out of sync.
- **suggest_melds**, **calculate_probabilities**: Manually request meld suggestions or recalculate probabilities (normally automatic).
- **recommend_discard**, **recommend_draw_action**: Manually request recommendations (already automatic).
- **end_game**: Manually end the game and log results.
- **quit** or **exit**: Quit at any prompt outside the main menu.

Normally, I won’t need these commands thanks to the automated guidance.

## Remaining Tasks

- **Refine Probability Calculation**: More complex logic for greater accuracy.
- **Improve Wife’s Logic**: Make her moves more realistic or strategic.
- **Expand Testing and Validation**: More unit tests, handle edge cases.
- **Further Documentation and Polish**
- **Future Enhancements**:
  - Consider a GUI for visual interaction.
  - Introduce advanced Rummy variants and scoring rules.

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
