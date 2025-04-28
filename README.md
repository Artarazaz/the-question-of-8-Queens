# 8 Queens Puzzle - DNA-Inspired Solution

A novel approach to solving the classic 8 Queens problem using pair-based selection inspired by DNA base pairs.

![8 Queens Puzzle](https://github.com/Artarazaz/the-question-of-8-Queens/blob/main/a_solution_for_problem.png)

## 📋 About the Project

This project implements a solution to the classic 8 Queens puzzle using a novel algorithm inspired by DNA base-pair formation in human genetics. The 8 Queens puzzle requires placing eight chess queens on an 8×8 chessboard so that no two queens threaten each other; thus, a solution requires that no two queens share the same row, column, or diagonal.

## 🧬 DNA-Inspired Algorithm: The Biological Connection

This algorithm draws fascinating parallels with DNA formation in human biology, creating a unique approach to the classic 8 Queens problem.

### Base Pairing Mechanism

In human DNA, four nucleotide bases (Adenine, Thymine, Guanine, and Cytosine) form specific pairs (A-T and G-C) based on their molecular compatibility. This selective pairing is the foundation of genetic information storage. Similarly, this algorithm:

```python
pairs = [
    [(1, 3), (1, 4), (1, 5), (1, 6), (1, 7), (1, 8)],
    [(2, 4), (2, 5), (2, 6), (2, 7), (2, 8)],
    [(3, 1), (3, 5), (3, 6), (3, 7), (3, 8)],
    # ...and so on
]
```

- Defines potential "compatible" queen pairs similar to how DNA bases form specific pairs
- Each sublist represents possible position pairings, analogous to how specific DNA sequences encode particular genetic information
- The structure preserves the constraints necessary for a valid solution, just as DNA's structure preserves genetic integrity

### Assembly Process

DNA strand assembly occurs through sequential addition of compatible nucleotides. Our algorithm mimics this process:

1. **Initial Pair Selection**: Just as DNA replication begins at specific sites, our algorithm starts with an initial pair:

```python
ran = random.choice(stack)
lst[0], lst[1] = ran[0], ran[1]
used_numbers.add(ran[0])
used_numbers.add(ran[1])
```

2. **Sequential Growth**: DNA strands grow by adding compatible nucleotides. Similarly, our algorithm builds the solution by adding compatible pairs:

```python
# Select second pair
if stack:
    ran = random.choice(stack)
    lst[2], lst[3] = ran[0], ran[1]
    # ... and so on for remaining pairs
```

3. **Compatibility Filtering**: During DNA replication, only compatible bases can pair up. Our algorithm enforces this with:

```python
stack[:] = [pair for pair in stack if pair[0] not in used_numbers and pair[1] not in used_numbers]
```

### Stability Validation

DNA's stability depends on correct base pairing and structural integrity. Our algorithm validates solution stability:

```python
def test(result):
    # Check diagonal threats (similar to checking DNA structural integrity)
    for i in range(8):
        row = i + 1
        row_value = result[i] - 1
        while row_value != 0 and row != 8:
            if result[row] == row_value:
                return False  # Unstable configuration found
            row_value = row_value - 1
            row = row + 1
    # ... additional validation checks
    return True  # Solution is stable
```

This validation ensures that only "viable" configurations survive, similar to how enzymes in DNA replication verify correct base pairing.

### Randomness Within Constraints

DNA formation involves probabilistic molecular interactions within defined constraints. Our algorithm incorporates similar stochastic processes:

- Random selection (`random.choice()`) mimics the probabilistic nature of molecular encounters
- The pre-defined pair structure provides constraints, similar to chemical bonding rules in DNA
- Multiple iterations produce varied yet valid solutions, analogous to how DNA recombination creates genetic diversity

### Emergent Complexity

Both DNA and our algorithm demonstrate how complex patterns emerge from simpler rules:

- DNA's four-base system creates the vast complexity of the human genome
- Our algorithm's pair-selection approach produces all 92 distinct solutions to the 8 Queens problem
- The check for unique solutions (`check(result, arrays)`) ensures we capture this diversity

By drawing inspiration from one of nature's most elegant information storage and replication systems, this algorithm provides a fresh perspective on solving combinatorial problems through pattern-based rather than exhaustive search methods.
## 🚀 Features

- **Command Line Version:** Basic implementation with solution visualization
- **GUI Application:** Interactive interface to generate and view multiple solutions
- **Efficient Generation:** Quickly generates solutions through random pair selection
- **Complete Solutions:** Access to all 92 distinct solutions to the 8 Queens puzzle
- **Visualization:** Elegant representation of the chessboard and queen placements using Matplotlib

## 🛠️ Installation & Usage

```bash
# Clone the repository
git clone https://github.com/yourusername/8-queens-dna.git
cd 8-queens-dna

# Install required packages
pip install matplotlib numpy tkinter

# Run the command line version
python queens_cli.py

# Run the GUI version
python queens_gui.py
```

### GUI Instructions:

1. Select the number of solutions you want to generate (1-92)
2. Click "Generate" to visualize the solutions
3. Each solution will be displayed in a grid layout with queens marked on the chessboard

## 🧪 How It Works

The core algorithm works in these steps:

1. **Pair Definition:** Predefined pairs of positions that could potentially work together
2. **Random Selection:** Four pairs (8 queens) are randomly selected from the available options
3. **Validation:** The selected configuration is tested to ensure no queens threaten each other
4. **Unique Solutions:** Only unique solutions are kept, eventually collecting all 92 possible arrangements

### Algorithm Highlights:

```python
def create_list(lst, pairs, stack):
    # Clear the list and stack for a fresh start
    lst[:] = [0] * 8
    stack.clear()
    used_numbers = set()  # For tracking used numbers

    # Fill stack with all pairs
    for sublist in pairs:
        for pair in sublist:
            stack.append(pair)

    # Select first pair
    ran = random.choice(stack)
    lst[0], lst[1] = ran[0], ran[1]
    used_numbers.add(ran[0])
    used_numbers.add(ran[1])
    
    # Update stack: remove pairs containing used numbers
    stack[:] = [pair for pair in stack if pair[0] not in used_numbers and pair[1] not in used_numbers]
    
    # Continue selecting pairs until all 8 queens are placed
    # ...
```

## 📊 Performance

The algorithm's performance varies based on the random selection process, but typically finds all 92 solutions within seconds. The GUI provides a runtime display to track performance.

## Sample Solutions

Below is a textual representation of a sample solution:

```
Q . . . . . . .
. . . . Q . . .
. . . . . . . Q
. . . . . Q . .
. . Q . . . . .
. . . . . . Q .
. Q . . . . . .
. . . Q . . . .
```

## 👨‍💻 Contributing

Contributions are welcome! Here are some ways you can contribute:

- Improve the algorithm efficiency
- Enhance the GUI design
- Add additional features like solution export
- Create better visualizations
- Fix bugs or suggest improvements

Please feel free to submit a pull request or open an issue to discuss potential changes.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🔗 Related Links

- [Wikipedia: Eight Queens Puzzle](https://en.wikipedia.org/wiki/Eight_queens_puzzle)
- [Wikipedia: DNA Structure](https://en.wikipedia.org/wiki/DNA)

---

Created with ❤️ inspired by the elegant structures of DNA
