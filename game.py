import math
import copy

# Constants for the game
PLAYER_X = "X"
PLAYER_O = "O"
EMPTY = "-"

def create_empty_board():
    """Creates a 3x3 board where each cell is another 3x3 board."""
    return [[[[EMPTY for _ in range(3)] for _ in range(3)] for _ in range(3)] for _ in range(3)]

def check_winner(board):
    """Checks the winner of a 3x3 board."""
    for row in board:
        if row[0] == row[1] == row[2] != EMPTY:
            return row[0]
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] != EMPTY:
            return board[0][col]
    if board[0][0] == board[1][1] == board[2][2] != EMPTY:
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != EMPTY:
        return board[0][2]
    return None

def is_full(board):
    """Checks if a 3x3 board is full."""
    return all(cell != EMPTY for row in board for cell in row)

def evaluate(board):
    """Heuristic evaluation for a 3x3 board."""
    winner = check_winner(board)
    if winner == PLAYER_X:
        return 10
    elif winner == PLAYER_O:
        return -10
    return 0

def is_terminal(board):
    """Checks if the game is over for a 3x3 board."""
    return check_winner(board) is not None or is_full(board)

def minimax(board, depth, alpha, beta, maximizing_player):
    """Minimax algorithm with alpha-beta pruning for a 3x3 board."""
    if depth == 0 or is_terminal(board):
        return evaluate(board)

    if maximizing_player:
        max_eval = -math.inf
        for i in range(3):
            for j in range(3):
                if board[i][j] == EMPTY:
                    board[i][j] = PLAYER_X
                    eval = minimax(board, depth - 1, alpha, beta, False)
                    board[i][j] = EMPTY
                    max_eval = max(max_eval, eval)
                    alpha = max(alpha, eval)
                    if beta <= alpha:
                        break
        return max_eval
    else:
        min_eval = math.inf
        for i in range(3):
            for j in range(3):
                if board[i][j] == EMPTY:
                    board[i][j] = PLAYER_O
                    eval = minimax(board, depth - 1, alpha, beta, True)
                    board[i][j] = EMPTY
                    min_eval = min(min_eval, eval)
                    beta = min(beta, eval)
                    if beta <= alpha:
                        break
        return min_eval

def find_best_move(board, maximizing_player):
    """Finds the best move for the current player."""
    best_move = None
    best_value = -math.inf if maximizing_player else math.inf

    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                board[i][j] = PLAYER_X if maximizing_player else PLAYER_O
                move_value = minimax(board, 4, -math.inf, math.inf, not maximizing_player)
                board[i][j] = EMPTY

                if maximizing_player and move_value > best_value:
                    best_value = move_value
                    best_move = (i, j)
                elif not maximizing_player and move_value < best_value:
                    best_value = move_value
                    best_move = (i, j)

    return best_move

def play_game():
    """Main game loop for Ultimate Tic-Tac-Toe."""
    board = create_empty_board()
    current_player = PLAYER_X
    global_board = [[EMPTY for _ in range(3)] for _ in range(3)]

    while not is_terminal(global_board):
        print("Global Board:")
        for row in global_board:
            print(" ".join(row))

        if current_player == PLAYER_X:
            print("Player X's turn.")
            move = find_best_move(global_board, True)
        else:
            print("Player O's turn.")
            move = None
            while move is None:
                try:
                    user_input = input("Enter your move as 'row col': ")
                    row, col = map(int, user_input.split())
                    if global_board[row][col] == EMPTY:
                        move = (row, col)
                    else:
                        print("Invalid move. Cell is not empty.")
                except (ValueError, IndexError):
                    print("Invalid input. Please enter row and column as two numbers between 0 and 2.")

        if move:
            x, y = move
            global_board[x][y] = current_player

        current_player = PLAYER_O if current_player == PLAYER_X else PLAYER_X

    print("Game Over!")
    winner = check_winner(global_board)
    if winner:
        print(f"Winner: {winner}")
    else:
        print("It's a draw!")

if __name__ == "__main__":
    play_game()
