import random
import time
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle


# Parameters for genetic algorithm
POPULATION_SIZE = 100
MUTATION_RATE = 0.1
NUM_GENERATIONS = 100
TOURNAMENT_SIZE = 5
N_QUEENS = 8  # 8x8 board with 8 queens


def create_individual():
    """Create a random individual (solution)"""
    # Each queen is placed in a different column, row position is random
    return [random.randint(0, N_QUEENS - 1) for _ in range(N_QUEENS)]


def initialize_population(size):
    """Create initial population of random individuals"""
    return [create_individual() for _ in range(size)]


def fitness(individual):
    """
    Calculate fitness of an individual
    Higher fitness is better, max fitness means no conflicts
    """
    conflicts = 0
    for i in range(N_QUEENS):
        for j in range(i + 1, N_QUEENS):
            # Check if queens are in same row
            if individual[i] == individual[j]:
                conflicts += 1
            # Check if queens are in same diagonal
            elif abs(individual[i] - individual[j]) == abs(i - j):
                conflicts += 1

    # Max conflicts would be n(n-1)/2 for worst case
    max_conflicts = N_QUEENS * (N_QUEENS - 1) // 2
    return max_conflicts - conflicts


def tournament_selection(population, fitnesses):
    """Select individual using tournament selection"""
    tournament_indices = random.sample(range(len(population)), TOURNAMENT_SIZE)
    tournament = [(population[i], fitnesses[i]) for i in tournament_indices]
    return max(tournament, key=lambda x: x[1])[0]


def crossover(parent1, parent2):
    """Create a new individual by crossing over two parents"""
    # Single point crossover
    crossover_point = random.randint(1, N_QUEENS - 1)
    child = parent1[:crossover_point] + parent2[crossover_point:]
    return child


def mutate(individual):
    """Mutate an individual by changing random positions"""
    for i in range(N_QUEENS):
        if random.random() < MUTATION_RATE:
            individual[i] = random.randint(0, N_QUEENS - 1)
    return individual


def genetic_algorithm():
    """Run genetic algorithm to solve 8 queens problem"""
    # Initialize population
    population = initialize_population(POPULATION_SIZE)

    for generation in range(NUM_GENERATIONS):
        # Calculate fitness for each individual
        fitnesses = [fitness(ind) for ind in population]

        # Check if we have a solution
        max_fitness = N_QUEENS * (N_QUEENS - 1) // 2
        best_fitness = max(fitnesses)
        best_index = fitnesses.index(best_fitness)
        best_individual = population[best_index]

        if best_fitness == max_fitness:
            print(f"حل در نسل {generation} پیدا شد")
            return best_individual

        # Create new population
        new_population = []

        # Elitism: keep best individual
        new_population.append(best_individual)

        # Create rest of new population
        while len(new_population) < POPULATION_SIZE:
            # Selection
            parent1 = tournament_selection(population, fitnesses)
            parent2 = tournament_selection(population, fitnesses)

            # Crossover
            child = crossover(parent1, parent2)

            # Mutation
            child = mutate(child)

            new_population.append(child)

        population = new_population

        if generation % 100 == 0:
            print(f"نسل {generation}، بهترین امتیاز: {best_fitness}/{max_fitness}")

    # If solution not found within generations, return best individual
    fitnesses = [fitness(ind) for ind in population]
    best_index = fitnesses.index(max(fitnesses))
    best_individual = population[best_index]
    print("بهترین جواب پیدا شده:")
    return best_individual


def print_board(solution):
    """Print the chessboard with queens in text format"""
    print("┌" + "─" * (N_QUEENS * 2) + "┐")
    for row in range(N_QUEENS):
        print("│", end="")
        for col in range(N_QUEENS):
            if solution[col] == row:
                print("♛ ", end="")
            else:
                # Use different background for black/white squares
                if (row + col) % 2 == 0:
                    print("□ ", end="")
                else:
                    print("■ ", end="")
        print("│")
    print("└" + "─" * (N_QUEENS * 2) + "┘")


def plot_board(solution, title="Solution 1"):
    """Plot the chessboard with queens using matplotlib"""
    fig, ax = plt.subplots(figsize=(6, 6))

    # Draw checkerboard pattern
    for i in range(N_QUEENS):
        for j in range(N_QUEENS):
            color = 'white' if (i + j) % 2 == 0 else 'black'
            ax.add_patch(Rectangle((j, N_QUEENS - i - 1), 1, 1, color=color))

    # Add queens
    for col, row in enumerate(solution):
        # Use queen symbol (♕)
        queen_x, queen_y = col + 0.5, N_QUEENS - row - 0.5
        ax.text(queen_x, queen_y, '♕', fontsize=24, ha='center', va='center',
                color='gray' if (col + row) % 2 == 0 else 'white')

    # Set limits and title
    ax.set_xlim(0, N_QUEENS)
    ax.set_ylim(0, N_QUEENS)
    ax.set_title(title)
    ax.set_aspect('equal')

    # Remove ticks
    ax.set_xticks([])
    ax.set_yticks([])

    plt.savefig('8queens_solution.png', bbox_inches='tight')
    plt.show()


def is_solution_valid(solution):
    """Check if a solution is valid (no conflicts)"""
    # Check for row conflicts
    for i in range(N_QUEENS):
        for j in range(i + 1, N_QUEENS):
            # Check if queens are in same row
            if solution[i] == solution[j]:
                return False
            # Check if queens are in same diagonal
            elif abs(solution[i] - solution[j]) == abs(i - j):
                return False
    return True


def run_genetic_algorithm_multiple_times(num_runs=5):
    """Run genetic algorithm multiple times to find different solutions"""
    solutions = []
    valid = False
    while not valid:
        i = 0
        print(f"اجرای {i + 1}:")
        solution = genetic_algorithm()
        solutions.append(solution)
        print(f"جواب {i + 1}: {solution}")

        # Verify solution
        valid = is_solution_valid(solution)
        if valid:
            valid = True
        print(f"آیا جواب معتبر است؟ {'بله' if valid else 'خیر'}")

        # Print text-based board
        print_board(solution)

        # Display graphical board
        plot_board(solution, f"Solution {i + 1}")
        i = i + 1

    return solutions


# Run the algorithm
s = time.time()
if __name__ == "__main__":
    # Set random seed for reproducibility
    random.seed(int(time.time()))
    solutions = run_genetic_algorithm_multiple_times(1)
e = time.time()
print("run" , e - s, "seconds")

# برای اجرای این برنامه، کتابخانه matplotlib را نصب کنید:
# pip install matplotlib