import random


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


def stochastic_hill_climbing(max_attempts=10000):
    board = generate_initial_board()
    current_heuristic = heuristic(board)
    attempts = 0
    steps = 0

    print("=== 8 QUEENS PROBLEM WITH STOCHASTIC HILL CLIMBING ===")
    print(f"Initial state: {board}")
    print(f"Initial heuristic: {current_heuristic}\n")

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

    return board, steps, current_heuristic


def run_multiple_times(num_runs=100, max_attempts=10000):
    successes = 0
    total_success_steps = 0
    best_heuristic = float('inf')
    best_board = None

    print(f"=== RUNNING {num_runs} TIMES ===")
    print(f"Max attempts per run: {max_attempts}\n")

    for run in range(1, num_runs + 1):
        board, steps, heuristic_val = stochastic_hill_climbing(max_attempts)
        if heuristic_val == 0:
            successes += 1
            total_success_steps += steps
        if heuristic_val < best_heuristic:
            best_heuristic = heuristic_val
            best_board = board
        if run % 10 == 0 or run == num_runs:
            print(f"Completed {run}/{num_runs} runs...")

    success_rate = (successes / num_runs) * 100
    avg_steps = total_success_steps / successes if successes > 0 else 0

    print(f"\n=== SUMMARY ===")
    print(f"Successes: {successes}/{num_runs}")
    print(f"Success rate: {success_rate:.2f}%")
    print(f"Average steps for success: {avg_steps:.2f}" if successes > 0 else "No successful runs")
    print(f"Best heuristic: {best_heuristic}")
    print(f"Best state: {best_board}")

    return success_rate, successes, best_board


if __name__ == "__main__":
    run_multiple_times(num_runs=100, max_attempts=10000)