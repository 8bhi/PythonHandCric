# Cricket Game

## Overview

This is a simple text-based Cricket Game written in Python. The player can play a game of cricket against the computer. The game includes batting and bowling mechanics, with a total of 2 wickets and 2 overs (12 balls) for each side.

## Features

* Toss system: Player can choose between heads or tails.
* Batting and Bowling: Players take turns to bat and bowl.
* Wicket Mechanism: Wickets fall if the player's number matches the computer's number.
* Score Tracking: Runs are tracked, and the winner is determined at the end of the match.
* MySQL Database Integration:

  * Creates a table to store the match details (player, runs, wickets).
  * Allows the user to clear the table after the match.

## How to Run

1. Install Python (version 3.7 or above).
2. Install MySQL and ensure it is running.
3. Install MySQL Connector for Python using the command:

   ```bash
   pip install mysql-connector-python
   ```
4. Create a MySQL database named `cric`.
5. Ensure your MySQL credentials (host, user, password, database) in the script are correct.
6. Run the script using:

   ```bash
   python cricket_game.py
   ```

## Game Instructions

1. The player must select a number between 1 to 6 for each ball.
2. If the player’s number matches the computer’s, the player loses a wicket.
3. The innings end after 2 wickets or 12 balls.
4. The player with the highest score at the end of two innings wins.

## Database Details

* The script connects to a MySQL database (`cric`) and creates a table for each match (named `<your_team>_vs_computer`).
* The table stores player names, their runs, and wickets.
* Users can clear the table at the end of the match to avoid duplicates.

## Example Gameplay

* Toss: Choose heads (h) or tails (t).
* Batting/Bowling: Choose a number between 1 and 6.
* The game continues until all balls are bowled or all wickets are lost.

## Future Improvements

* Add GUI for better user interaction.
* Add multiplayer support.
* Enhance the toss mechanism to allow player choice.
