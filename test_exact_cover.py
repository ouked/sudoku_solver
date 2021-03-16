import exact_cover as ec
import time
import numpy as np


# Provided testing code, from University of Bath

def run_tests(difficulties=None, limit=None) -> None:
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
        maximum_time = 0
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
            maximum_time = max(end_time - start_time, maximum_time)
        print(f"{count}/{len(sudokus)} {difficulty} sudokus correct")
        if count < len(sudokus):
            break

    whole_end_time = time.process_time()
    print("\nAll puzzles took", whole_end_time - whole_start_time, "seconds to solve.\n")
    print("\nMax time:", maximum_time)


def solve_fiend() -> None:
    """
    Test sudoku from local newspaper
    :return: None
    """
    state = np.array([
        [0, 9, 0, 6, 2, 7, 0, 0, 0],
        [0, 0, 8, 0, 0, 0, 0, 0, 0],
        [2, 0, 1, 0, 0, 0, 0, 0, 0],

        [0, 0, 3, 9, 0, 0, 0, 5, 0],
        [8, 0, 0, 0, 0, 0, 0, 7, 0],
        [0, 4, 0, 5, 0, 0, 0, 0, 1],

        [3, 0, 5, 8, 0, 0, 0, 0, 7],
        [0, 0, 0, 0, 0, 0, 6, 0, 0],
        [0, 7, 0, 0, 0, 4, 0, 2, 0]
    ])
    start_time = time.process_time()
    your_solution = ec.sudoku_solver(state)
    end_time = time.process_time()
    print(your_solution)
    print(end_time - start_time)


def extra_tests():
    """
    Extra tests to make sure the current approach is indeed correct.
    :return:
    """
    quizzes = np.zeros((1000000, 81), np.int32)
    solutions = np.zeros((1000000, 81), np.int32)
    for i, line in enumerate(open('data/sudoku.csv', 'r').read().splitlines()[1:]):
        quiz, solution = line.split(",")
        for j, q_s in enumerate(zip(quiz, solution)):
            q, s = q_s
            quizzes[i, j] = q
            solutions[i, j] = s
    quizzes = quizzes.reshape((-1, 9, 9))
    solutions = solutions.reshape((-1, 9, 9))
    print("Size: ", quizzes.size)
    # input("okay?")
    puzzles_num = 10000
    times, count = 0, 0
    very_start_time = time.process_time()
    for quiz, solution in zip(quizzes[:puzzles_num], solutions[:puzzles_num]):

        # print(quiz)
        start_time = time.process_time()
        your_solution = ec.sudoku_solver(quiz.copy())
        end_time = time.process_time()

        times += end_time - start_time
        count += 1
        # print(your_solution)
        if not np.array_equal(your_solution, solution):
            print("Wrong solution for: ", quiz)
            break  # TODO REMOVE
        # print("Time to solve: ", end_time-start_time, " seconds")

    very_end_time = time.process_time()
    print("===========================\n")
    print("THE ENTIRE SOLUTION TAKES: ", very_end_time - very_start_time, " seconds")
    print("===========================\n")
    print("Average solve time: ", times / count, " seconds")

def test_extreme():
    empty = np.full(shape=(9, 9), fill_value=0, dtype=int)
    start_time = time.process_time()
    your_solution = ec.sudoku_solver(empty)
    end_time = time.process_time()
    print(your_solution)
    print(end_time - start_time)

    full = np.full(shape=(9,9), fill_value=9, dtype=int)
    start_time = time.process_time()
    your_solution = ec.sudoku_solver(your_solution)
    end_time = time.process_time()
    print(your_solution)
    print(end_time - start_time)

if __name__ == "__main__":
    # solve_fiend()
    # extra_tests()
    # test_extreme()

    run_tests()

