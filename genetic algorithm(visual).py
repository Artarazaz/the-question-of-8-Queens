import random
import matplotlib.pyplot as plt
import numpy as np
import time
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def __main__():
    # Create the GUI and run it
    app = QueensGUI()
    app.mainloop()


class QueensGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("8 Queens Answers")
        self.geometry("1000x800")

        # Frame for controls
        control_frame = ttk.Frame(self)
        control_frame.pack(pady=10)

        # Number selection
        self.number_options = [str(i) for i in range(1, 93)]
        ttk.Label(control_frame, text="Number of solutions (1-92):").grid(row=0, column=0, padx=5)
        self.num_var = tk.StringVar(value="0")
        self.num_spinner = ttk.Combobox(control_frame, textvariable=self.num_var,values=self.number_options, width=5)
        self.num_spinner.grid(row=0, column=1, padx=5)

        # Generate button
        generate_btn = ttk.Button(control_frame, text="Generate", command=self.generate_solutions)
        generate_btn.grid(row=0, column=2, padx=10)

        # Runtime display
        self.runtime_var = tk.StringVar(value="Runtime: 0.0 seconds")
        ttk.Label(control_frame, textvariable=self.runtime_var).grid(row=0, column=3, padx=10)

        # Frame for visualizations
        self.display_frame = ttk.Frame(self)
        self.display_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Initial empty canvas
        self.fig = plt.figure(figsize=(7, 5))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.display_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Store solutions when generated
        self.all_solutions = []

    def generate_solutions(self):
        # Clear the previous figure
        plt.close(self.fig)
        self.fig = plt.figure(figsize=(7, 5))

        try:
            num_solutions = int(self.num_var.get())
            if num_solutions < 1 or num_solutions > 92:
                raise ValueError("Number must be between 1 and 92")
        except ValueError:
            # Show error message
            plt.text(0.5, 0.5, "Please enter a valid number between 1 and 92",
                     ha='center', va='center', transform=self.fig.transFigure)
            self.canvas.figure = self.fig
            self.canvas.draw()
            return

        # Generate solutions
        start = time.time()

        # If we haven't generated all 92 solutions yet, do it now
        if not self.all_solutions:
            self.all_solutions = self.generate_all_solutions()

        # Choose the requested number of solutions
        solutions = random.sample(self.all_solutions, num_solutions)

        end = time.time()
        runtime = end - start
        self.runtime_var.set(f"Runtime: {runtime:.4f} seconds")

        # Create subplots based on number of solutions
        cols = min(3, num_solutions)
        rows = (num_solutions + cols - 1) // cols

        for i, sol in enumerate(solutions):
            ax = self.fig.add_subplot(rows, cols, i + 1)
            self.draw_board(sol, f"Solution {i + 1}", ax)

        plt.tight_layout()
        self.canvas.figure = self.fig
        self.canvas.draw()

    def generate_all_solutions(self):
        lst = [0] * 8
        stack = []
        arrays = []
        pairs = [
            [(1, 3), (1, 4), (1, 5), (1, 6), (1, 7), (1, 8)],
            [(2, 4), (2, 5), (2, 6), (2, 7), (2, 8)],
            [(3, 1), (3, 5), (3, 6), (3, 7), (3, 8)],
            [(4, 1), (4, 2), (4, 6), (4, 7), (4, 8)],
            [(5, 1), (5, 2), (5, 3), (5, 7), (5, 8)],
            [(6, 1), (6, 2), (6, 3), (6, 4), (6, 8)],
            [(7, 1), (7, 2), (7, 3), (7, 4), (7, 5)],
            [(8, 1), (8, 2), (8, 3), (8, 4), (8, 5), (8, 6)]
        ]
        count = 0
        while count < 92:
            result = create_list(lst, pairs, stack)
            if result is not None:
                if test(result):
                    if check(result, arrays):
                        arrays.append(result[:])
                        count += 1
        return arrays

    def draw_board(self, solution, title="", ax=None):
        if ax is None:
            ax = plt.gca()

        board = np.zeros((8, 8))
        for i in range(8):
            for j in range(8):
                if (i + j) % 2 == 0:
                    board[i][j] = 1

        ax.imshow(board, cmap='gray', extent=(0, 8, 0, 8))
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_title(title)

        for row, col in enumerate(solution):
            # col is 1-indexed, matplotlib uses 0-indexing
            ax.text(col - 1 + 0.5, 7 - row + 0.5, '♛', fontsize=24, ha='center', va='center', color='red')


def create_list(lst, pairs, stack):
    # پاک کردن لیست و stack برای شروع تازه
    lst[:] = [0] * 8

    stack.clear()
    used_numbers = set()  # برای ردیابی اعداد استفاده‌شده

    # پر کردن stack با تمام جفت‌ها
    for sublist in pairs:
        for pair in sublist:
            stack.append(pair)

    # انتخاب جفت اول
    ran = random.choice(stack)
    lst[0], lst[1] = ran[0], ran[1]
    used_numbers.add(ran[0])
    used_numbers.add(ran[1])

    # به‌روزرسانی stack: حذف جفت‌هایی که شامل اعداد استفاده‌شده هستند
    stack[:] = [pair for pair in stack if pair[0] not in used_numbers and pair[1] not in used_numbers]
    # انتخاب جفت دوم
    if stack:
        ran = random.choice(stack)
        lst[2], lst[3] = ran[0], ran[1]
        used_numbers.add(ran[0])
        used_numbers.add(ran[1])
        stack[:] = [pair for pair in stack if pair[0] not in used_numbers and pair[1] not in used_numbers]

    # انتخاب جفت سوم
    if stack:
        ran = random.choice(stack)
        lst[4], lst[5] = ran[0], ran[1]
        used_numbers.add(ran[0])
        used_numbers.add(ran[1])
        stack[:] = [pair for pair in stack if pair[0] not in used_numbers and pair[1] not in used_numbers]
    # انتخاب جفت چهارم
    if not stack:
        return
    else:
        ran = random.choice(stack)
        lst[6], lst[7] = ran[0], ran[1]
        used_numbers.add(ran[0])
        used_numbers.add(ran[1])
    return lst


def test(result):
    for i in range(8):
        row = i + 1
        row_value = result[i] - 1
        while row_value != 0 and row != 8:
            if result[row] == row_value:
                return False
            row_value = row_value - 1
            row = row + 1

    for i in range(8):
        row = i + 1
        row_value = result[i] + 1
        while row_value != 10 and row != 8:
            if result[row] == row_value:
                return False
            row_value = row_value + 1
            row = row + 1
    return True


def check(result, arrays):
    if result not in arrays:
        return True
    return False


def draw_board(solution, title=""):
    board = np.zeros((8, 8))
    for i in range(8):
        for j in range(8):
            if (i + j) % 2 == 0:
                board[i][j] = 1

    fig, ax = plt.subplots(figsize=(5, 5))
    ax.imshow(board, cmap='gray', extent=(0, 8, 0, 8))
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title(title)

    for row, col in enumerate(solution):
        # col is 1-indexed, matplotlib uses 0-indexing
        ax.text(col - 1 + 0.5, 7 - row + 0.5, '♛', fontsize=20, ha='center', va='center', color='gray')


if __name__ == "__main__":
    __main__()