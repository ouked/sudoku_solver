import exact_cover as ec
import time
import numpy as np

# Provided testing code, from University of Bath

def run_tests(difficulties=None, limit=None):
    sudoku_solver = ec.sudoku_solver

    if difficulties is None:
        difficulties = ['very_easy', 'easy', 'medium', 'hard']

    if limit is None:
        limit = float('inf')

    whole_start_time = time.process_time()

    for difficulty in difficulties:
        print(f"Testing {difficulty} sudokus")

        sudokus = np.load(f"data/{difficulty}_puzzle.npy")
        solutions = np.load(f"data/{difficulty}_solution.npy")

        count = 0
        for i in range(min(limit, len(sudokus))):
            # for i in range(1):
            sudoku = sudokus[i].copy()
            print(f"This is {difficulty} sudoku number", i)
            print(sudoku)

            start_time = time.process_time()
            your_solution = sudoku_solver(sudoku)
            end_time = time.process_time()

            print(f"This is your solution for {difficulty} sudoku number", i)
            print(your_solution)

            print("Is your solution correct?")
            if np.array_equal(your_solution, solutions[i]):
                print("Yes! Correct solution.")
                count += 1
            else:
                print("No, the correct solution is:")
                print(solutions[i])

            print("This sudoku took", end_time - start_time, "seconds to solve.\n")

        print(f"{count}/{len(sudokus)} {difficulty} sudokus correct")
        if count < len(sudokus):
            break

    whole_end_time = time.process_time()
    print("\nAll puzzles took", whole_end_time - whole_start_time, "seconds to solve.\n")


if __name__ == "__main__":
    run_tests()
