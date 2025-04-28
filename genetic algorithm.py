import random
import matplotlib.pyplot as plt
import numpy as np
import time


def __main__():
    user_input = 0
    raw_input = 0
    try:
        raw_input = input("Enter a number: \n")
        user_input = int(raw_input)
        if user_input < 0 or user_input > 92:
            print("Sorry, you have to enter a number between 0 and 92. (You entered: " + str(user_input) + ")")
            exit()
    except ValueError:
        print(f"That's not a valid input! Please try again. (You entered: {raw_input})")
        exit()

    start = time.time()

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
    while count < user_input:
        result = create_list(lst, pairs, stack)
        if result is not None:
            if test(result):
                if check(result, arrays):
                    arrays.append(result[:])
                    count += 1

    for i, sol in enumerate(arrays):
        draw_board(sol, f"Solution {i + 1}")
        plt.show()

    end = time.time()
    print("Code runtime: ", end - start)



def create_list(lst, pairs, stack):
    # پاک کردن لیست و stack برای شروع تازه
    lst[:] = [0]  * 8

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

def test(result) :
    #print("test ",result)
    for i in range(8): #0
        row = i + 1 #3
        row_value = result[i] - 1 #5
        while row_value != 0 and row != 8:
            #print("l r ", row)
            #print("l v ", row_value)
            if result[row] == row_value  :
                #print("left con", result[i], "with", result[row])
                return False
            row_value = row_value - 1
            row = row + 1

    for i in range(8):  # 2
        row = i + 1  # 7
        row_value = result[i] + 1  # 6
        while row_value != 10 and row != 8:
            #print("r r ", row)
            #print("r v ", row_value)
            if result[row] == row_value:
                #print("right con", result[i], "with", result[row])
                return False
            row_value = row_value + 1
            row = row + 1
    return True

def check(result, arrays):
    if result not in arrays:
        #arrays.append(result[:])
        return True
    return False

def draw_board(solution, title=""):
    board = np.zeros((8, 8))
    for i in range(8):
        for j in range(8):
            if (i + j) % 2 == 0:
                board[i][j] = 1

    fig, ax = plt.subplots(figsize=(5, 5))
    ax.imshow(board, cmap='gray', extent=(0.0, 8.0, 0.0, 8.0))
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title(title)

    for row, col in enumerate(solution):
        # col is 1-indexed, matplotlib uses 0-indexing
        ax.text(col - 1 + 0.5, 7 - row + 0.5, '♛', fontsize=24, ha='center', va='center', color='gray')


if __name__ == "__main__" :
    __main__()