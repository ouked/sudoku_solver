import copy
import time
import numpy as np
from collections import Counter

# !!! Previous, outdated attempt. exact_cover.py is faster. This is here for archival purposes.

class SudokuState:
    valid_row_cache = {}

    def __init__(self, state, n=9, block_size=3):
        self.values = state
        self.n = n
        self.block_size = block_size
        self.solvable = True
        self.valid = True

        self.value_freq = {d: 0 for d in range(1, 10)}
        self.saturated_values = set()

        # Produce a 2d array containing sets of 1-9 for each cell.
        self.possible_values = [
            [{1, 2, 3, 4, 5, 6, 7, 8, 9} for _ in range(n)] for _ in range(n)
        ]

        # Remove impossible values
        for (y, x), value in np.ndenumerate(self.values):
            if value != 0:
                if value not in self.possible_values[y][x]:
                    self.solvable = False
                    return

                self.possible_values[y][x] = set()
                self.update_possible_values(x, y, value)

                if value != -1:
                    self.count(value)

        self.update_valid()

    def count(self, val):
        self.value_freq[val] += 1

        if self.value_freq[val] == self.n:
            self.saturated_values.add(val)

        elif self.value_freq[val] > self.n:
            self.solvable = False

    def set_value(self, pos: (int, int), new_value: int):
        """
        Creates a new state with new_value at the given pos. Check for validity and updates possible states.
        set deep_copy to False if the new state will be used to update this state.
        """

        (pos_x, pos_y) = pos

        # Check if new_value is possible
        if new_value not in self.possible_values[pos_y][pos_x]:
            raise ValueError(f"New value {new_value} not in possible values for cell position {pos}:"
                             f" {self.possible_values[pos_y][pos_x]}")

        # Make new state, update value and change possible_values
        state = copy.deepcopy(self)

        state.values[pos_y][pos_x] = new_value
        state.update_valid()

        state.count(new_value)

        state.possible_values[pos_y][pos_x] = set()
        state.update_possible_values(pos_x, pos_y, new_value)

        return state

    def update_possible_values(self, x, y, val):
        def remove_possible_value(n, m):
            nonlocal val
            try:
                self.possible_values[m][n].remove(val)

                if len(self.possible_values[m][n]) == 0 and self.values[m][n] == 0:
                    self.solvable = False
            except KeyError:
                pass
            return self.solvable

        # Remove new value from row and column it exists in
        for i in range(self.n):
            # Remove possible value from the new value's row
            if not remove_possible_value(i, y) or not remove_possible_value(x, i):
                return
        # Remove possible value from the new value's column

        size = self.block_size

        # Round pos down to nearest multiple of block_size (get top left position of block)
        (block_x, block_y) = map(lambda coord: (coord // size) * size, (x, y))

        # Remove new value from block it exists in
        for a in range(block_x, block_x + size):
            for b in range(block_y, block_y + size):
                if not remove_possible_value(a, b):
                    return

    def rows(self):
        """Returns list of rows in this state"""
        return self.values

    def columns(self):
        """Returns list of columns in this state"""
        return self.values.T

    def blocks(self) -> list:
        """ Returns an array of all blocks in this state as flat arrays."""
        size = self.block_size

        block_idx = range(0, self.n, size)
        # Splice flattened (size x size) blocks from board.

        # Example:
        # |    9 x 9 numpy array
        # |        [i: i + size, j: j + size]
        # |    3 x 3 numpy array
        # |        flatten()
        # |    1 x 3 numpy array
        # |        tolist()
        # V    1 x 3 python array
        #
        return [
            self.values[i: i + size, j: j + size].flatten().tolist()
            for i in block_idx
            for j in block_idx
        ]

    def has_duplicate_non_zero_elements(self, arr: list) -> bool:
        # result = bool([item for item, c in Counter(arr).items() if c > 1 and item != 0])
        # return result

        t = tuple(arr)
        if t in SudokuState.valid_row_cache:
            return SudokuState.valid_row_cache[t]
        result = bool([item for item, c in Counter(arr).items() if c > 1 and item != 0])
        SudokuState.valid_row_cache[t] = result
        return result

    def update_valid(self):
        pass
        # if not self.solvable:
        #     self.valid = False
        #
        # # Check rows, columns, and blocks
        # for direction in [self.rows(), self.columns(), self.blocks()]:
        #     # return False if any row, column or block has more than one occurrence of a number
        #     for item in direction:
        #         if self.has_duplicate_non_zero_elements(item):
        #             self.valid = False
        #
        # self.valid = True

    def is_valid(self) -> bool:
        """Returns ``True`` if the state doesn't contain any illegal combinations of numbers"""
        # return self.solvable and self.valid

        if not self.solvable:
            return False

            # Check rows, columns, and blocks
        for direction in [self.rows(), self.columns(), self.blocks()]:
            # return False if any row, column or block has more than one occurrence of a number
            for item in direction:
                if self.has_duplicate_non_zero_elements(item):
                    return False

        return True

    def is_goal(self):
        """Returns ``True`` if the state is a 'goal' or 'winning' state"""
        return (np.count_nonzero(self.values == 0) == 0) and self.is_valid()

    def __str__(self):
        return f"{self.values}\nValid: {self.is_valid()}, Goal: {self.is_goal()}"

    def __deepcopy__(self, memodict={}):
        cls = self.__class__
        state = cls.__new__(cls)
        state.values = self.values.copy()
        state.n = self.n
        state.block_size = self.block_size
        state.solvable = self.solvable
        state.possible_values = [[cell.copy() for cell in row] for row in self.possible_values]
        state.value_freq = self.value_freq.copy()
        state.saturated_values = self.saturated_values.copy()
        state.valid = self.valid

        return state


def pick_next_cell(state: SudokuState):
    """
    Get the next cell to try and solve
    :param state: State to get cell from
    :return: Next cell to try and solve
    """

    pos = (0, 0)
    minimum = 10

    # todo Do this as you go?
    for (y, x), values in np.ndenumerate(state.values):
        n_poss_values = len(state.possible_values[y][x])
        if 0 < n_poss_values < minimum:
            if n_poss_values == 1:
                return x, y

            pos = (x, y)
            minimum = n_poss_values
    return pos


def order_values(state: SudokuState, pos: (int, int)):
    """
    Get the values for position in the order to try them in.
    :param state: State to get possible values from
    :param pos: Cell for the values to be substituted into
    :return: List of values to try
    """
    (x, y) = pos
    # return [val for val in list(state.possible_values[y][x]) if state.set_value(pos, val).solvable]
    result = sorted(
        [val for val in list(state.possible_values[y][x]) if
         val not in state.saturated_values and state.set_value(pos, val).solvable],
        key=lambda item: state.value_freq[item], reverse=False
    )
    return result


def backtrack(state: SudokuState) -> SudokuState:
    """
    Solves sudoku using depth_first_search
    :param state: State to solve from
    :return: Solved state or 9x9 grid of -1 if there are no solutions
    """
    solved_sudoku = SudokuState(np.array([[-1 for _ in range(state.n)] for _ in range(state.n)]))

    pos = pick_next_cell(state)

    values = order_values(state, pos)

    for val in values:

        new_state = state.set_value(pos, val)

        if new_state.is_goal():
            solved_sudoku = new_state
            break

        if new_state.is_valid():
            deep_state = backtrack(new_state)

            if deep_state is not None and deep_state.is_goal():
                solved_sudoku = deep_state
                break

    return solved_sudoku


def sudoku_solver(state: np.ndarray) -> np.ndarray:
    """
    Solves a Sudoku puzzle and returns its unique solution.

    Input
        sudoku : 9x9 numpy array
            Empty cells are designated by 0.

    Output
        9x9 numpy array of integers
            It contains the solution, if there is one. If there is no solution, all array entries should be -1.
    """
    return backtrack(SudokuState(state)).values


if __name__ == "__main__":
    SKIP_TESTS = False

    if not SKIP_TESTS:
        difficulties = ['very_easy', 'easy', 'medium', 'hard']

        for difficulty in difficulties:
            print(f"Testing {difficulty} sudokus")

            sudokus = np.load(f"data/{difficulty}_puzzle.npy")
            solutions = np.load(f"data/{difficulty}_solution.npy")

            count = 0
            for i in range(len(sudokus)):
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
