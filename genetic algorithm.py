import random
import matplotlib.pyplot as plt
import numpy as np
import time


def count_threats(solution):
    threats = 0
    n = len(solution)
    for i in range(n):
        for j in range(i + 1, n):
            if solution[i] == solution[j]:
                threats += 1
            elif abs(i - j) == abs(solution[i] - solution[j]):
                threats += 1
    return threats


def get_pairs_from_list(lst):
    pairs = []
    i = 0
    while i < len(lst) - 1:
        pairs.append((lst[i], lst[i + 1]))
        i += 2
    return pairs


def weighted_random_select(pool, threats_list):
    min_threats = min(threats_list)
    weights = [1.0 / (t - min_threats + 1) for t in threats_list]
    total_weight = sum(weights)
    probabilities = [w / total_weight for w in weights]

    selected_indices = []
    indices = list(range(len(pool)))

    while len(selected_indices) < 2:
        rand = random.random()
        cumulative = 0
        for i, prob in enumerate(probabilities):
            cumulative += prob
            if rand <= cumulative:
                if i not in selected_indices:
                    selected_indices.append(i)
                break

    return pool[selected_indices[0]], pool[selected_indices[1]]


def crossover(parent1, parent2, board_size):
    board_size = int(board_size)
    pairs1 = get_pairs_from_list(parent1)
    pairs2 = get_pairs_from_list(parent2)

    num_pairs_needed = board_size // 2

    random.shuffle(pairs1)
    random.shuffle(pairs2)

    used_numbers = set()
    child_pairs = []

    all_pairs = pairs1 + pairs2
    random.shuffle(all_pairs)

    for pair in all_pairs:
        if len(child_pairs) >= num_pairs_needed:
            break
        if pair[0] not in used_numbers and pair[1] not in used_numbers:
            child_pairs.append(pair)
            used_numbers.add(pair[0])
            used_numbers.add(pair[1])

    child = []
    for pair in child_pairs:
        child.append(pair[0])
        child.append(pair[1])

    if board_size % 2 != 0:
        available = [i for i in range(1, board_size + 1) if i not in used_numbers]
        if available:
            child.append(random.choice(available))

    return child


def __main__():
    board_size = input("Enter a board size: \n")

    try:
        pool_size = input("Enter pool size (number of lists): \n")
        pool_size = int(pool_size)
        if pool_size <= 0:
            print("Pool size must be positive!")
            exit()
    except ValueError:
        print(f"That's not a valid input!")
        exit()

    try:
        generations = input("Enter number of generations (cycles): \n")
        generations = int(generations)
        if generations < 0:
            print("Generations must be non-negative!")
            exit()
    except ValueError:
        print(f"That's not a valid input!")
        exit()

    start = time.time()

    pairs_checker_result = pairs_checker(board_size)
    pairs = pairs_checker_result

    pool = []

    print(f"\n{'='*60}")
    print("INITIAL POOL - Filling with random lists")
    print(f"{'='*60}")

    attempts = 0
    max_attempts = pool_size * 100

    best_solution = None
    best_threats = None

    while len(pool) < pool_size and attempts < max_attempts:
        result = create_list(pairs, board_size)
        if result is not None:
            if check(result, pool):
                pool.append(result[:])
                print(f"Added list {len(pool)}: {result}")

                result_threats = count_threats(result)
                if best_threats is None or result_threats < best_threats:
                    best_solution = result[:]
                    best_threats = result_threats

                if best_threats == 0:
                    print("\n*** PERFECT SOLUTION FOUND IN INITIAL POOL! ***")
                    break
        attempts += 1

    if best_threats != 0:
        for gen in range(generations):
            if best_threats == 0:
                break

            print(f"\n{'='*60}")
            print(f"GENERATION {gen + 1}")
            print(f"{'='*60}")

            threats_list = [count_threats(s) for s in pool]
            print(f"Current threats: {threats_list}")

            new_pool = []
            while len(new_pool) < pool_size:
                if len(pool) >= 2:
                    parent1, parent2 = weighted_random_select(pool, threats_list)
                    child = crossover(parent1, parent2, board_size)
                    if child not in new_pool:
                        new_pool.append(child)
                        child_threats = count_threats(child)
                        print(f"Generated child {len(new_pool)}: {child} (Threats: {child_threats})")

                        if child_threats < best_threats:
                            best_solution = child[:]
                            best_threats = child_threats

                        if best_threats == 0:
                            print("\n*** PERFECT SOLUTION FOUND! ***")
                            break

            pool = new_pool

    end = time.time()

    print(f"\n{'='*60}")
    print("BEST SOLUTION FOUND")
    print(f"{'='*60}")
    print(f"Solution: {best_solution}")
    print(f"Threats: {best_threats}")

    if best_threats == 0:
        print("*** VALID SOLUTION - No queens threaten each other! ***")
    else:
        print(f"(No perfect solution found - this is the minimum threats possible)")

    print(f"\nCode runtime: {end - start:.4f} seconds")



def create_list(pairs, board_size):
    # پاک کردن لیست و stack برای شروع تازه
    lst = []
    board_size = int(board_size)
    stack = pairs.copy()
    #print(stack)
    used_numbers = set()
      # برای ردیابی اعداد استفاده‌شده
    for j in range(int(board_size / 2)):
        if stack:
            ran2 = random.choice(stack)
            #print(ran2, "ran")
            lst.append(ran2[0])
            lst.append(ran2[1])
            #used_numbers = set()
            # print(result, "r")

            used_numbers.add(ran2[0])
            used_numbers.add(ran2[1])
            #print(used_numbers, "used")
            stack[:] = [pair for pair in stack if pair[0] not in used_numbers and pair[1] not in used_numbers]
            #print(len(stack), "stack length")
            #print(stack, "stack")
        else:
            return None
    #print(lst, "lst")
    if board_size % 2 != 0:
        lst.append(random.randint(1, board_size))
    #print(lst, "append")
    return lst

def test(lst, board_size) :
    # Use a set to track diagonals for O(1) lookups
    diagonals1 = set()  # For i+lst[i] diagonals
    diagonals2 = set()  # For i-lst[i] diagonals

    for i, val in enumerate(lst):
        # Check if this position shares a diagonal with any previous position
        if (i + val) in diagonals1 or (i - val) in diagonals2:
            return False

        # Add this position's diagonals to our sets
        diagonals1.add(i + val)
        diagonals2.add(i - val)

    return True

def check(result, arrays):
    if result not in arrays:
        #arrays.append(result[:])
        return True
    return False

def draw_board(solution, board_size, title=""):
    board_size = int(board_size)
    board = np.zeros((board_size, board_size))
    for i in range(board_size):
        for j in range(board_size):
            if (i + j) % 2 == 0:
                board[i][j] = 1

    fig, ax = plt.subplots(figsize=(board_size * 0.6, board_size * 0.6))
    ax.imshow(board, cmap='gray', extent=(0, board_size, 0, board_size))
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title(title)

    for row, col in enumerate(solution):
        # col is 1-indexed, matplotlib uses 0-indexing
        ax.text(col - 1 + 0.5, board_size - 1 - row + 0.5, '♛', fontsize=24 * (8 / board_size), ha='center', va='center', color='red')

def pairs_checker(board_size):
    output = []
    for j in range(int(board_size) + 1):
        #row = []
        for i in range(int(board_size) + 1):
            if j != i and j != i + 1 and j != i - 1 and i != 0 and j != 0:
                output.append((j, i))
        #if row:
        #    output.append(row)
    print(output, 'pairs checked')
    #print(len(output), 'length of pairs')
    return output

if __name__ == "__main__" :
    __main__()