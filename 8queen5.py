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


def stochastic_hill_climbing_with_restarts(max_attempts=10000, max_restarts=10):
    restarts_used = 0
    for restart in range(max_restarts):
        board = generate_initial_board()
        current_heuristic = heuristic(board)
        attempts = 0
        steps = 0

        print(f"Lần khởi động {restart + 1}/{max_restarts}")
        print(f"Trạng thái ban đầu: {board}")
        print(f"Heuristic ban đầu: {current_heuristic}\n")

        while current_heuristic > 0 and attempts < max_attempts:
            neighbor = get_neighbor(board)
            neighbor_heuristic = heuristic(neighbor)
            if neighbor_heuristic < current_heuristic:
                board = neighbor
                current_heuristic = neighbor_heuristic
                print(f"Bước {attempts}: {board} | Heuristic: {current_heuristic}")
            attempts += 1
            steps += 1

        restarts_used = restart + 1
        if current_heuristic == 0:
            print("\nTìm thấy giải pháp tối ưu!")
            print(f"Số lần khởi động đã dùng: {restarts_used}")
            print(f"Trạng thái cuối: {board}")
            print(f"Heuristic cuối: {current_heuristic}")
            print(f"Số bước thực hiện: {steps}")
            return board, steps, restarts_used, True

    print("\nKhông tìm thấy giải pháp sau tất cả lần khởi động.")
    print(f"Số lần khởi động đã dùng: {restarts_used}")
    print(f"Trạng thái cuối: {board}")
    print(f"Heuristic cuối: {current_heuristic}")
    print(f"Số bước thực hiện: {steps}")
    return board, steps, restarts_used, False


def run_multiple_times(num_runs=100, max_attempts=10000, max_restarts=10):
    successes = 0
    total_steps = 0
    total_restarts = 0

    print(f"=== CHẠY {num_runs} LẦN VỚI KHỞI ĐỘNG LẠI ({max_restarts} tối đa mỗi lần) ===")
    print(f"Số lần thử tối đa mỗi lần leo đồi: {max_attempts}\n")

    for run in range(1, num_runs + 1):
        board, steps, restarts_used, success = stochastic_hill_climbing_with_restarts(max_attempts, max_restarts)
        if success:
            successes += 1
            total_steps += steps
            total_restarts += restarts_used
        if run % 10 == 0 or run == num_runs:
            print(f"Hoàn thành {run}/{num_runs} lần chạy...")

    success_rate = (successes / num_runs) * 100 if num_runs > 0 else 0
    avg_steps = total_steps / successes if successes > 0 else 0
    avg_restarts = total_restarts / successes if successes > 0 else 0

    print(f"\n=== TÓM TẮT ===")
    print(f"Số lần thành công: {successes}/{num_runs}")
    print(f"Tỷ lệ thành công: {success_rate:.2f}%")
    print(
        f"Số lần khởi động lại trung bình khi thành công: {avg_restarts:.2f}" if successes > 0 else "Không có lần chạy thành công")
    print(f"Số bước trung bình khi thành công: {avg_steps:.2f}" if successes > 0 else "Không có lần chạy thành công")

    return success_rate, avg_steps, avg_restarts


if __name__ == "__main__":
    run_multiple_times(num_runs=100, max_attempts=10000, max_restarts=10)