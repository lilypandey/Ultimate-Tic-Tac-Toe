# Ultimate Tic-Tac-Toe with AI (Minimax & Alpha-Beta Pruning)

This project implements an AI bot to play **Tic-Tac-Toe** using the **Minimax algorithm** with **Alpha-Beta pruning**. The game allows human interaction, where Player O makes moves manually, while Player X is controlled by the AI. The AI makes decisions based on a **heuristic evaluation** of the board state.

## Features

- **AI Player (Player X)**: The AI uses the **Minimax algorithm** with **Alpha-Beta pruning** for optimal decision-making.
- **Human Player (Player O)**: Player O makes manual moves by inputting the row and column for their move.
- **Heuristic Evaluation**: The AI evaluates board states using a heuristic function that assigns a score to each board configuration.
- **Game Termination**: The game ends when a player wins or when the board is full, resulting in a draw.

## Game Rules

The game is played on a **single 3x3 board**. Players take turns placing their marks on the grid. A win is achieved by completing three marks in a row, either horizontally, vertically, or diagonally. The game ends when one player wins or when all cells are filled, resulting in a draw.

## How to Play

1. **Player X (AI)**: The AI will automatically make its move using the Minimax algorithm to find the best move.
2. **Player O (Human)**: The human player will input their move in the format `row col` (where row and column are integers between 0 and 2). The move will be placed on the global board if the selected cell is empty.
3. The game ends when a player wins or when the board is full.