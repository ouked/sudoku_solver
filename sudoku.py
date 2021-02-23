import numpy as np


def count_occ(arr, i): return np.count_nonzero(arr == i)


class SudokuState:
    def __init__(self, state, n=9):
        self.state = state
        self.n = n

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
        size = 3
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

    def update_cell(self, pos, new_value):
        """Change value at position (x, y) to new_value, with no checking for validity."""
        self.state[pos[1], pos[0]] = new_value

    def __str__(self):
        return f"{self.state}\nValid: {self.is_valid()}, Goal: {self.is_goal()}"


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
# s.update_cell((0, 1), 1)
print(s)

# ...and its solution
print("Solution of first sudoku:")
# print(solutions[0])

w = SudokuState(solutions[0])
print(w)
