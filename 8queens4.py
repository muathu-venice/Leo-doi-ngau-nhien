import random
import matplotlib.pyplot as plt
import numpy as np


def is_attacking(board, i, j):
    row_i, row_j = board[i], board[j]
    return row_i == row_j or abs(i - j) == abs(row_i - row_j)


def heuristic(board):
    attacks = 0
    for i in range(8):
        for j in range(i + 1, 8):
            if is_attacking(board, i, j):
                attacks += 1
    return attacks


def generate_initial_board():
    return random.sample(range(8), 8)


def get_neighbor(board):
    new_board = board[:]
    col = random.randint(0, 7)
    new_row = random.randint(0, 7)
    while new_row == board[col]:
        new_row = random.randint(0, 7)
    new_board[col] = new_row
    return new_board


def plot_board(board, title='Chessboard'):
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.set_xlim(0, 8)
    ax.set_ylim(0, 8)
    ax.set_xticks(range(8))
    ax.set_yticks(range(8))
    ax.set_xticklabels(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'])
    ax.set_yticklabels(['1', '2', '3', '4', '5', '6', '7', '8'])
    ax.grid(True)

    for i in range(8):
        for j in range(8):
            color = 'lightgray' if (7 - i + j) % 2 == 0 else 'darkgray'
            ax.add_patch(plt.Rectangle((j, i), 1, 1, facecolor=color))

    for col, row in enumerate(board):
        ax.text(col + 0.5, 7 - row + 0.5, 'Q', fontsize=20, ha='center', va='center', color='red')

    ax.set_title(title)
    plt.show()


def stochastic_hill_climbing(max_attempts=10000):
    board = generate_initial_board()
    current_heuristic = heuristic(board)
    attempts = 0
    steps = 0

    print("=== 8 QUEENS PROBLEM WITH STOCHASTIC HILL CLIMBING ===")
    print(f"Initial state: {board}")
    print(f"Initial heuristic: {current_heuristic}\n")

    plot_board(board, 'Initial Board')

    while current_heuristic > 0 and attempts < max_attempts:
        neighbor = get_neighbor(board)
        neighbor_heuristic = heuristic(neighbor)
        if neighbor_heuristic < current_heuristic:
            board = neighbor
            current_heuristic = neighbor_heuristic
            print(f"Step {attempts}: {board} | Heuristic: {current_heuristic}")
        attempts += 1
        steps += 1

    print("\n" + (
        "Optimal solution found!" if current_heuristic == 0 else f"No solution found in {max_attempts} attempts."))
    print(f"Final state: {board}")
    print(f"Final heuristic: {current_heuristic}")
    print(f"Steps performed: {steps}")

    plot_board(board, 'Final Board')
    return board, steps


if __name__ == "__main__":
    solution, steps = stochastic_hill_climbing(max_attempts=10000)