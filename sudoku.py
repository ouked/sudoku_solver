import copy

import numpy as np


def count_occ(arr, i): return np.count_nonzero(arr == i)


class SudokuState:
    def __init__(self, state, n=9, block_size=3):
        self.state = state
        self.n = n
        self.block_size = block_size

        # Produce a 2d array containing sets of 1-9 for each cell.
        self.possible_values = [
            [set(i for i in range(1, 10)) for _ in range(n)] for _ in range(n)
        ]

        # Remove impossible values
        # todo: Is there a better way of doing this?
        for x in range(self.n):
            for y in range(self.n):
                value = state[y][x]
                if value != 0:
                    self.possible_values = self.set_value((x, y), value).possible_values

    def rows(self):
        """Returns list of rows in this state"""
        return self.state

    def columns(self):
        """Returns list of columns in this state"""
        return self.state.T

    def is_valid(self, verbose=False):
        """Returns ``True`` if the state doesn't contain any illegal combinations of numbers"""
        # Check numbers 1-9
        for i in range(1, 10):
            # Check rows, columns, and blocks
            for direction in [self.rows(), self.columns(), self.get_blocks()]:
                # return False if any row, column or block has more than one occurrence of a number
                if any(count_occ(item, i) > 1 for item in direction):
                    return False
        return True

    def is_goal(self):
        """Returns ``True`` if the state is a 'goal' or 'winning' state"""
        return self.is_valid() and (count_occ(self.state, 0) == 0)

    def get_blocks(self):
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
            self.state[i: i + size, j: j + size].flatten().tolist()
            for i in block_idx
            for j in block_idx
        ]

    def set_value(self, pos: (int, int), new_value: int, deep_copy=True):
        """Creates a new state with new_value at the given pos. Check for validity and updates possible states.
        set deep_copy to False if the new state will be used to update this state.
        """

        (x, y) = pos

        # Check if new_value is possible
        if new_value not in self.possible_values[y][x]:
            raise ValueError(f"New value {new_value} not in possible values for cell position {pos}:"
                             f" {self.possible_values[y][x]}")

        # Make new state, update value and change possible_values
        state = copy.deepcopy(self)

        state.state[y, x] = new_value
        state.possible_values[y][x] = set()

        # Remove new value from row and column it exists in
        for i in range(state.n):
            # Remove new value from column
            state.possible_values[i][x].discard(new_value)

            # Remove new value from row
            state.possible_values[y][i].discard(new_value)

        size = self.block_size

        # Round pos down to nearest multiple of block_size (get 0,0 of block)
        (block_x, block_y) = map(lambda a: (a // size) * size, pos)

        # Remove new value from block it exists in
        for x in range(block_x, block_x + size):
            for y in range(block_y, block_y + size):
                state.possible_values[y][x].discard(new_value)

        return state

    def __str__(self):
        return f"{self.state}\nValid: {self.is_valid()}, Goal: {self.is_goal()}"


def pick_next_column(state):
    pass


def order_values(state, pos):
    pass


def sudoku_solver(sudoku):
    """
    Solves a Sudoku puzzle and returns its unique solution.

    Input
        sudoku : 9x9 numpy array
            Empty cells are designated by 0.

    Output
        9x9 numpy array of integers
            It contains the solution, if there is one. If there is no solution, all array entries should be -1.
    """

    ### YOUR CODE HERE

    return solved_sudoku


# Load sudokus
sudoku = np.load("data/very_easy_puzzle.npy")
print("very_easy_puzzle.npy has been loaded into the variable sudoku")
print(f"sudoku.shape: {sudoku.shape}, sudoku[0].shape: {sudoku[0].shape}, sudoku.dtype: {sudoku.dtype}")

# Load solutions for demonstration
solutions = np.load("data/very_easy_solution.npy")
print()

# Print the first 9x9 sudoku...
print("First sudoku:")
# print(sudoku[0], "\n")
s = SudokuState(sudoku[0])
print(s)

# ...and its solution
print("Solution of first sudoku:")
# print(solutions[0])

w = SudokuState(solutions[0])
print(w)
