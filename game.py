class UltimateTicTacToe:
    def __init__(self):
        # The board is a 3x3 grid of smaller 3x3 boards
        self.board = [[[0 for _ in range(3)] for _ in range(3)] for _ in range(9)]
        self.meta_board = [0 for _ in range(9)]  # The overarching 3x3 "meta-board"
        self.current_subboard = -1  # -1 means the player can choose any sub-board

    def display(self):
        """Display the board in a readable format."""
        for i in range(3):
            for row in range(3):
                line = ""
                for j in range(3):
                    subboard_index = i * 3 + j
                    line += " | ".join(
                        ["X" if cell == 1 else "O" if cell == -1 else "." for cell in self.board[subboard_index][row]]
                    )
                    line += "   "
                print(line)
            print("-" * 50)
        print("\nMeta-Board:")
        for i in range(3):
            print(" | ".join(
                ["X" if cell == 1 else "O" if cell == -1 else "." for cell in self.meta_board[i * 3:i * 3 + 3]]
            ))
        print()

    def is_winner(self, subboard):
        """Check if a sub-board has a winner."""
        # Check rows, columns, and diagonals
        for i in range(3):
            if abs(sum(self.board[subboard][i])) == 3:  # Row check
                return self.board[subboard][i][0]
            if abs(sum(row[i] for row in self.board[subboard])) == 3:  # Column check
                return self.board[subboard][0][i]
        # Diagonal checks
        if abs(self.board[subboard][0][0] + self.board[subboard][1][1] + self.board[subboard][2][2]) == 3:
            return self.board[subboard][0][0]
        if abs(self.board[subboard][0][2] + self.board[subboard][1][1] + self.board[subboard][2][0]) == 3:
            return self.board[subboard][0][2]
        return 0  # No winner yet

    def update_meta_board(self):
        """Update the overarching 3x3 meta-board based on sub-board winners."""
        for i in range(9):
            if self.meta_board[i] == 0:  # Check if the sub-board isn't already won
                winner = self.is_winner(i)
                if winner != 0:
                    self.meta_board[i] = winner

    def is_draw(self):
        """Check if the meta-board ends in a draw."""
        return all(cell != 0 for cell in self.meta_board)

    def make_move(self, subboard, row, col, player):
        """Make a move in the given sub-board."""
        if self.board[subboard][row][col] != 0:
            raise ValueError("Invalid move: Cell is already occupied.")
        self.board[subboard][row][col] = player

        # Check if the sub-board is now won
        self.update_meta_board()

        # Determine the next sub-board to play in
        self.current_subboard = row * 3 + col
        if self.meta_board[self.current_subboard] != 0:  # If the sub-board is already won, any sub-board can be played
            self.current_subboard = -1

    def evaluate(self):
        """Heuristic evaluation function for the AI."""
        # Meta-board evaluation: Favor boards won by the player
        return sum(self.meta_board)

    def minimax(self, depth, is_maximizing, alpha, beta):
        self.update_meta_board()
        winner = self.check_meta_winner()
        if winner != 0 or depth == 0:
            # you can return winner, or better yet your evaluate()
            return self.evaluate()

        # figure out which subboards are legal to play right now
        if self.current_subboard != -1:
            allowed = [self.current_subboard]
        else:
            allowed = [i for i, v in enumerate(self.meta_board) if v == 0]

        if is_maximizing:
            max_eval = float('-inf')
            for sb in allowed:
                for r in range(3):
                    for c in range(3):
                        if self.board[sb][r][c] != 0:
                            continue

                        # simulate the move
                        old_sub = self.current_subboard
                        self.board[sb][r][c] = 1

                        # update forced‐next‐subboard
                        target = r * 3 + c
                        if self.meta_board[target] == 0:
                            self.current_subboard = target
                        else:
                            self.current_subboard = -1

                        val = self.minimax(depth - 1, False, alpha, beta)

                        # undo 
                        self.board[sb][r][c] = 0
                        self.current_subboard = old_sub

                        max_eval = max(max_eval, val)
                        alpha = max(alpha, val)
                        if beta <= alpha:
                            break
            return max_eval

        else:
            min_eval = float('inf')
            for sb in allowed:
                for r in range(3):
                    for c in range(3):
                        if self.board[sb][r][c] != 0:
                            continue

                        old_sub = self.current_subboard
                        self.board[sb][r][c] = -1

                        target = r * 3 + c
                        if self.meta_board[target] == 0:
                            self.current_subboard = target
                        else:
                            self.current_subboard = -1

                        val = self.minimax(depth - 1, True, alpha, beta)

                        self.board[sb][r][c] = 0
                        self.current_subboard = old_sub

                        min_eval = min(min_eval, val)
                        beta = min(beta, val)
                        if beta <= alpha:
                            break
            return min_eval

    def find_best_move(self, player, depth=3):
        best_score = float('-inf') if player == 1 else float('inf')
        best_move = None

        # figure out which subboards AI is allowed to start in
        if self.current_subboard != -1:
            allowed = [self.current_subboard]
        else:
            allowed = [i for i, v in enumerate(self.meta_board) if v == 0]

        for sb in allowed:
            for r in range(3):
                for c in range(3):
                    if self.board[sb][r][c] != 0:
                        continue

                    # simulate
                    old_sub = self.current_subboard
                    self.board[sb][r][c] = player

                    target = r * 3 + c
                    if self.meta_board[target] == 0:
                        self.current_subboard = target
                    else:
                        self.current_subboard = -1

                    score = self.minimax(depth - 1, player == -1, float('-inf'), float('inf'))

                    # undo
                    self.board[sb][r][c] = 0
                    self.current_subboard = old_sub

                    if (player == 1 and score > best_score) or (player == -1 and score < best_score):
                        best_score = score
                        best_move = (sb, r, c)

        return best_move

    def check_meta_winner(self):
        """Check if the meta-board has a winner."""
        # Same logic as sub-board winner checking
        for i in range(3):
            if abs(sum(self.meta_board[i * 3:(i + 1) * 3])) == 3:  # Row check
                return self.meta_board[i * 3]
            if abs(sum(self.meta_board[i::3])) == 3:  # Column check
                return self.meta_board[i]
        if abs(self.meta_board[0] + self.meta_board[4] + self.meta_board[8]) == 3:  # Diagonal
            return self.meta_board[0]
        if abs(self.meta_board[2] + self.meta_board[4] + self.meta_board[6]) == 3:  # Diagonal
            return self.meta_board[2]
        return 0  # No winner

if __name__ == "__main__":
    game = UltimateTicTacToe()
    game.display()

    while True:
        # Human player
        subboard, row, col = map(int, input("Enter subboard, row, col: ").split())
        if game.current_subboard != -1 and subboard != game.current_subboard:
            print(f"Invalid move: you must play in sub-board {game.current_subboard}")
            continue
        game.make_move(subboard, row, col, 1)
        game.display()

        # AI move
        move = game.find_best_move(-1)
        if move:
            game.make_move(*move, -1)
            print(f"AI moved: {move}")
            game.display()
        else:
            print("Game Over!")
            break
