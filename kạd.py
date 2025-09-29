import random
import tkinter as tk
from tkinter import ttk
import time
from PIL import Image, ImageTk
import io
import base64


class EightQueensGame:
    def __init__(self, root):
        self.root = root
        self.root.title("8 Queens")
        self.root.geometry("1200x800")
        self.root.configure(bg='#E8F4F8')

        self.board_size = 4
        self.board = []
        self.cell_size = 80
        self.is_running = False
        self.speed = 500  # milliseconds
        self.history = []
        self.current_step = 0
        self.status_message = ""
        self.use_restart = True
        self.max_restarts = 10
        self.restart_count = 0

        self.setup_ui()

    def setup_ui(self):
        # Frame chính
        main_frame = tk.Frame(self.root, bg='#E8F4F8')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Frame trái - Bàn cờ
        left_frame = tk.Frame(main_frame, bg='white', relief=tk.RAISED, borderwidth=2)
        left_frame.pack(side=tk.LEFT, padx=(0, 20), pady=10)

        board_label = tk.Label(left_frame, text="Bàn cờ", font=('Arial', 14, 'bold'),
                               bg='#B8D4E8', fg='black', pady=5)
        board_label.pack(fill=tk.X)

        self.canvas = tk.Canvas(left_frame, width=640, height=640, bg='white',
                                highlightthickness=0)
        self.canvas.pack(padx=10, pady=10)

        # Frame phải - Khởi tạo
        right_frame = tk.Frame(main_frame, bg='#B8D4E8', relief=tk.RAISED, borderwidth=2)
        right_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=(20, 0))

        init_label = tk.Label(right_frame, text="Khởi tạo", font=('Arial', 14, 'bold'),
                              bg='#B8D4E8', fg='black', pady=10)
        init_label.pack(fill=tk.X)

        # Chiều dài bàn cờ
        size_frame = tk.Frame(right_frame, bg='#B8D4E8')
        size_frame.pack(pady=20, padx=20)

        tk.Label(size_frame, text="Chiều dài bàn cờ:", font=('Arial', 11),
                 bg='#B8D4E8').pack(anchor='w')

        self.size_var = tk.StringVar(value='4')
        size_combo = ttk.Combobox(size_frame, textvariable=self.size_var,
                                  values=['4', '5', '6', '7', '8', '9', '10', '11', '12'],
                                  state='readonly', width=15)
        size_combo.pack(pady=5)
        size_combo.bind('<<ComboboxSelected>>', self.on_size_change)

        # Kích thước bàn cờ
        self.size_label = tk.Label(size_frame, text="Kích thước bàn cờ:\n4 × 4 = 16",
                                   font=('Arial', 10), bg='#B8D4E8', justify='left')
        self.size_label.pack(pady=10, anchor='w')

        # Hình ảnh Queen
        queen_frame = tk.Frame(right_frame, bg='#B8D4E8')
        queen_frame.pack(pady=20)

        tk.Label(queen_frame, text="Click Queen để chọn ngẫu nhiên\ntrạng thái ban đầu cho bàn cờ:",
                 font=('Arial', 10), bg='#B8D4E8', justify='center').pack()

        # Tạo hình ảnh Queen đơn giản
        queen_canvas = tk.Canvas(queen_frame, width=120, height=120, bg='white',
                                 highlightthickness=1, highlightbackground='gray')
        queen_canvas.pack(pady=10)
        queen_canvas.create_text(60, 60, text='👑', font=('Arial', 60))
        queen_canvas.bind('<Button-1>', lambda e: self.generate_random_board())

        # Tốc độ
        speed_frame = tk.Frame(right_frame, bg='#B8D4E8')
        speed_frame.pack(pady=20, padx=20, fill=tk.X)

        tk.Label(speed_frame, text="Tốc độ di chuyển của Queen:",
                 font=('Arial', 10), bg='#B8D4E8').pack(anchor='w')

        self.speed_scale = tk.Scale(speed_frame, from_=100, to=2000, orient=tk.HORIZONTAL,
                                    command=self.on_speed_change, bg='#B8D4E8',
                                    length=200, sliderlength=30)
        self.speed_scale.set(500)
        self.speed_scale.pack(pady=5)

        # Random Restart
        restart_frame = tk.Frame(right_frame, bg='#B8D4E8')
        restart_frame.pack(pady=10, padx=20, fill=tk.X)

        self.restart_var = tk.BooleanVar(value=True)
        restart_check = tk.Checkbutton(restart_frame, text="Bật Random Restart",
                                       variable=self.restart_var,
                                       font=('Arial', 10), bg='#B8D4E8',
                                       command=self.toggle_restart)
        restart_check.pack(anchor='w')

        self.restart_info = tk.Label(restart_frame,
                                     text="(Tự động thử lại khi mắc kẹt - Tối đa 10 lần)",
                                     font=('Arial', 8), bg='#B8D4E8', fg='#555')
        self.restart_info.pack(anchor='w', padx=20)

        # Số bước
        self.step_label = tk.Label(speed_frame, text="Số bước hậu ăn nhau: 00",
                                   font=('Arial', 10), bg='#B8D4E8')
        self.step_label.pack(pady=10, anchor='w')

        # Số lần restart
        self.restart_label = tk.Label(speed_frame, text="Số lần restart: 0",
                                      font=('Arial', 10), bg='#B8D4E8')
        self.restart_label.pack(pady=5, anchor='w')

        # Trạng thái
        self.status_label = tk.Label(speed_frame, text="",
                                     font=('Arial', 9), bg='#B8D4E8',
                                     fg='#FF4444', wraplength=200)
        self.status_label.pack(pady=5, anchor='w')

        # Nút bắt đầu và dừng
        button_frame = tk.Frame(right_frame, bg='#B8D4E8')
        button_frame.pack(pady=20)

        self.start_button = tk.Button(button_frame, text="Bắt đầu", font=('Arial', 12, 'bold'),
                                      bg='white', fg='black', width=15, height=2,
                                      command=self.start_algorithm)
        self.start_button.pack(pady=5)

        self.stop_button = tk.Button(button_frame, text="Dừng", font=('Arial', 12, 'bold'),
                                     bg='#FFCCCC', fg='black', width=15, height=2,
                                     command=self.stop_algorithm, state=tk.DISABLED)
        self.stop_button.pack(pady=5)

        self.reset_button = tk.Button(button_frame, text="Reset", font=('Arial', 12, 'bold'),
                                      bg='#FFEEAA', fg='black', width=15, height=2,
                                      command=self.reset_board)
        self.reset_button.pack(pady=5)

        # Khởi tạo bàn cờ
        self.generate_random_board()

    def on_size_change(self, event):
        self.board_size = int(self.size_var.get())
        self.size_label.config(
            text=f"Kích thước bàn cờ:\n{self.board_size} × {self.board_size} = {self.board_size * self.board_size}")
        self.cell_size = min(80, 640 // self.board_size)
        self.generate_random_board()

    def on_speed_change(self, value):
        self.speed = int(float(value))

    def toggle_restart(self):
        self.use_restart = self.restart_var.get()

    def generate_random_board(self):
        self.board = random.sample(range(self.board_size), self.board_size)
        self.draw_board()
        attacks = self.calculate_heuristic(self.board)
        self.step_label.config(text=f"Số bước hậu ăn nhau: {attacks:02d}")

    def draw_board(self, highlight_col=None, old_row=None, new_row=None):
        self.canvas.delete('all')

        board_width = self.board_size * self.cell_size
        board_height = self.board_size * self.cell_size
        offset_x = (640 - board_width) // 2
        offset_y = (640 - board_height) // 2

        # Vẽ bàn cờ
        for i in range(self.board_size):
            for j in range(self.board_size):
                x1 = offset_x + j * self.cell_size
                y1 = offset_y + i * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size

                color = 'white' if (i + j) % 2 == 0 else 'black'
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline='gray')

        # Vẽ mũi tên di chuyển
        if highlight_col is not None and old_row is not None and new_row is not None:
            x_start = offset_x + highlight_col * self.cell_size + self.cell_size // 2
            y_start = offset_y + (self.board_size - 1 - old_row) * self.cell_size + self.cell_size // 2
            x_end = offset_x + highlight_col * self.cell_size + self.cell_size // 2
            y_end = offset_y + (self.board_size - 1 - new_row) * self.cell_size + self.cell_size // 2

            # Vẽ vị trí cũ với màu mờ
            self.canvas.create_oval(x_start - self.cell_size // 3, y_start - self.cell_size // 3,
                                    x_start + self.cell_size // 3, y_start + self.cell_size // 3,
                                    fill='#FFE6E6', outline='#FF6B6B', width=2, dash=(5, 3))

            # Vẽ mũi tên
            self.canvas.create_line(x_start, y_start, x_end, y_end,
                                    arrow=tk.LAST, fill='#FF4444', width=4,
                                    arrowshape=(16, 20, 8), smooth=True)

            # Thêm hiệu ứng pulse cho vị trí mới
            for i in range(3):
                radius = self.cell_size // 3 + i * 10
                self.canvas.create_oval(x_end - radius, y_end - radius,
                                        x_end + radius, y_end + radius,
                                        outline='#00FF00', width=2,
                                        dash=(5, 3))

        # Vẽ quân hậu
        for col, row in enumerate(self.board):
            x = offset_x + col * self.cell_size + self.cell_size // 2
            y = offset_y + (self.board_size - 1 - row) * self.cell_size + self.cell_size // 2

            # Highlight quân hậu đang di chuyển
            if highlight_col == col:
                self.canvas.create_oval(x - self.cell_size // 3, y - self.cell_size // 3,
                                        x + self.cell_size // 3, y + self.cell_size // 3,
                                        fill='#FFFF99', outline='#FFD700', width=3)

            queen_size = min(40, self.cell_size // 2)
            self.canvas.create_text(x, y, text='👑',
                                    font=('Arial', queen_size),
                                    fill='red')

    def is_attacking(self, board, i, j):
        row_i, row_j = board[i], board[j]
        return row_i == row_j or abs(i - j) == abs(row_i - row_j)

    def calculate_heuristic(self, board):
        attacks = 0
        for i in range(len(board)):
            for j in range(i + 1, len(board)):
                if self.is_attacking(board, i, j):
                    attacks += 1
        return attacks

    def get_neighbor(self, board):
        new_board = board[:]
        col = random.randint(0, len(board) - 1)
        new_row = random.randint(0, len(board) - 1)
        while new_row == board[col]:
            new_row = random.randint(0, len(board) - 1)
        new_board[col] = new_row
        return new_board, col, board[col], new_row

    def solve_hill_climbing(self):
        all_moves = []
        best_board = None
        best_h = float('inf')
        self.restart_count = 0

        for restart in range(self.max_restarts if self.use_restart else 1):
            # Tạo trạng thái ban đầu mới cho mỗi lần restart
            if restart > 0:
                board = random.sample(range(self.board_size), self.board_size)
                self.restart_count = restart
                # Thêm marker restart vào history
                all_moves.append({
                    'board': board[:],
                    'heuristic': self.calculate_heuristic(board),
                    'col': -1,
                    'restart': True,
                    'restart_num': restart
                })
            else:
                board = self.board[:]

            current_h = self.calculate_heuristic(board)
            moves = [{'board': board[:], 'heuristic': current_h, 'col': -1}]
            attempts = 0
            max_attempts = 1000
            stuck_count = 0
            max_stuck = 100

            while current_h > 0 and attempts < max_attempts:
                neighbor, col, old_row, new_row = self.get_neighbor(board)
                neighbor_h = self.calculate_heuristic(neighbor)

                if neighbor_h < current_h:
                    board = neighbor
                    current_h = neighbor_h
                    stuck_count = 0
                    moves.append({
                        'board': board[:],
                        'heuristic': current_h,
                        'col': col,
                        'old_row': old_row,
                        'new_row': new_row
                    })
                else:
                    stuck_count += 1
                    if stuck_count >= max_stuck:
                        break

                attempts += 1

            # Thêm moves của lần thử này vào tổng
            all_moves.extend(moves[1:] if restart > 0 else moves)

            # Kiểm tra xem có tìm được giải pháp không
            if current_h == 0:
                self.status_message = f"✓ Tìm được giải pháp!\nSố bước: {len(all_moves) - 1}\nSố lần restart: {restart}"
                return all_moves

            # Lưu kết quả tốt nhất
            if current_h < best_h:
                best_h = current_h
                best_board = board[:]

        # Không tìm được giải pháp sau tất cả các lần restart
        self.status_message = f"✗ Không tìm được giải pháp!\nKết quả tốt nhất: {best_h} cặp tấn công\nĐã thử {self.restart_count + 1} lần"
        return all_moves

    def start_algorithm(self):
        if self.is_running:
            return

        self.status_label.config(text="Đang tìm kiếm...")
        self.restart_label.config(text="Số lần restart: 0")
        self.is_running = True

        # Cập nhật trạng thái nút
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)

        self.history = self.solve_hill_climbing()
        self.current_step = 0
        self.animate_solution()

    def stop_algorithm(self):
        self.is_running = False
        self.status_label.config(text="Đã dừng!")

        # Cập nhật trạng thái nút
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)

    def reset_board(self):
        self.stop_algorithm()
        self.generate_random_board()
        self.status_label.config(text="")
        self.restart_label.config(text="Số lần restart: 0")

    def animate_solution(self):
        if not self.is_running or self.current_step >= len(self.history):
            self.is_running = False
            # Hiển thị thông báo kết quả
            self.status_label.config(text=self.status_message)
            self.restart_label.config(text=f"Số lần restart: {self.restart_count}")

            # Cập nhật trạng thái nút khi hoàn thành
            self.start_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)
            return

        step_data = self.history[self.current_step]

        # Kiểm tra nếu là marker restart
        if step_data.get('restart', False):
            self.board = step_data['board'][:]
            self.draw_board()
            self.step_label.config(text=f"Số bước hậu ăn nhau: {step_data['heuristic']:02d}")
            self.restart_label.config(text=f"Số lần restart: {step_data['restart_num']}")
            # Hiển thị thông báo restart
            self.canvas.create_text(320, 320,
                                    text=f"🔄 RESTART #{step_data['restart_num']}",
                                    font=('Arial', 24, 'bold'),
                                    fill='#FF4444')
            self.current_step += 1
            self.root.after(self.speed * 2, self.animate_solution)  # Dừng lâu hơn khi restart
            return

        self.board = step_data['board'][:]

        highlight_col = step_data.get('col', -1)
        old_row = step_data.get('old_row', None)
        new_row = step_data.get('new_row', None)

        self.draw_board(highlight_col, old_row, new_row)
        self.step_label.config(text=f"Số bước hậu ăn nhau: {step_data['heuristic']:02d}")

        self.current_step += 1
        self.root.after(self.speed, self.animate_solution)


if __name__ == "__main__":
    root = tk.Tk()
    app = EightQueensGame(root)
    root.mainloop()