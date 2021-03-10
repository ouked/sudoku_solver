import copy
import numpy as np
from enum import Enum


class SudokuState:
    def __init__(self, values: np.ndarray):
        """
        Create a new Sudoku State.
        Calculates matrix A from passed values
        :param values: 9x9 grid of initial state
        """
        self.solvable = True
        self.solution = {}
        self.values = values

        # Matrix A
        self.a = {
            c: set() for c in (
                # Every cell must have a value, (x, y)
                    [("Cell", (x, y)) for x in range(9) for y in range(9)] +
                    # Every row must contain each value, (row, val)
                    [("Row", (row, val)) for row in range(9) for val in range(1, 10)] +
                    # Every column must contain each value, (column, val)
                    [("Col", (col, val)) for col in range(9) for val in range(1, 10)] +
                    # Every block must contain each value, (block, val)
                    [("Block", (block, val)) for block in range(9) for val in range(1, 10)]
            )
        }

        for rcv, consts in self.b.items():
            [self.a[c].add(rcv) for c in consts]

        # Update constraints to reflect initial state
        for (y, x), value in np.ndenumerate(values):
            if value != 0:
                try:
                    self.select_row((y, x, value))
                except KeyError:
                    self.solvable = False

    def select_row(self, rcv: (int, int, int)):
        """
        Select the corresponding row to the rcv. Removes rcv from other columns
        :param rcv: Row, Column, Value tuple to look up
        :return: None
        """
        # This is pretty nasty, but can't think of another way of doing it. Maybe pd.dataframes?

        # Popped columns
        columns = []

        # For constraint this rcv is associated with
        for c in SudokuState.b[rcv]:

            # For other rcv that satisfy c
            for other_rcv in self.a[c]:

                # For other constraints that the other rcv satisfies
                for other_c in self.b[other_rcv]:

                    if other_c != c:
                        self.a[other_c].remove(other_rcv)

            # Pop column from this row, and save for later
            columns.append(self.a.pop(c))
        return columns

    def deselect_row(self, rcv: (int, int, int), columns):
        """
        Deselect the given row. Adds the rcv from other columns
        :param rcv: Row, Column, Value to deselect
        :param columns: Columns to restore
        :return: None
        """
        # Undo the actions of select

        # Columns is an ordered list, so we must work backwards
        for c in reversed(SudokuState.b[rcv]):
            # Get column from list
            self.a[c] = columns.pop()
            # For other rcv that satisfy c
            for other_rcv in self.a[c]:
                # For other constraints that the other rcv satisfies
                for other_c in self.b[other_rcv]:
                    self.a[other_c].add(other_rcv)

    def add_solution(self, rcv: (int, int, int)):
        """
        Add the given rcv to solutions
        :param rcv: Row, Column, Value tuple to add to solution
        :return: Updated solutions
        """
        r, c, v = rcv
        self.solution[(r, c)] = v
        return self.solution

    def remove_solution(self, rcv: (int, int, int)):
        """
        Remove the given rcv from solutions
        :param rcv: Row, Column, Value tuple to add to solution
        :return: Updated solutions
        """
        r, c, v = rcv
        del self.solution[r, c]

    def pick_constraint(self) -> ((str, (int, int, int)), set):
        """
        Picks a non-empty constraint
        :return: Constraint, {related RCVs}
        """
        # Get all non-empty constraints
        consts = [v for v in self.a if self.a[v]]

        # Check there are constraints left
        if not consts:
            # self.solvable = False
            return

        # Get constraint with shortest number of possible RCVs
        result = min(consts, key=lambda k: len(self.a[k]))

        return result, self.a[result]

    def is_goal(self):
        """
        Is this state a goal?
        :return: True if this state is a goal
        """
        # An unsolvable state can't be a goal
        if not self.solvable:
            return False

        # A goal state will have no constraints left in self.a
        return all(item is None for item in self.a)

    def apply_solution(self):
        """
        Blindly apply the solution set to the initial values
        :return: updated values array
        """
        for key in self.solution:
            # Get X, Y, and value of cell
            value = self.solution[key]
            y, x = key

            self.values[y][x] = value

        return self.values

    entries = (
        (r, c, v)
        # Row (0-8)
        for r in range(9)
        # Column (0-8)
        for c in range(9)
        # Value (1-9)
        for v in range(1, 10))

    # Dict relating rcv values to their associated constraints
    b = {}
    for (r, c, v) in entries:
        # Get block x, y from "global" x, y. Rounds x, y down to nearest 3.
        block_y, block_x = map(lambda x: (x // 3), (r, c))

        # Get block id. 3 blocks in a row.
        block = (block_y * 3) + block_x

        b[(r, c, v)] = [
            # Every cell must have a value, (x, y)
            ("Cell", (r, c)),
            # Every row must contain each value, (row, val)
            ("Row", (r, v)),
            # Every column must contain each value, (column, val)
            ("Col", (c, v)),
            # Every block must contain each value, (block, val)
            ("Block", (block, v))
        ]

    error_grid = np.array([[-1 for _ in range(9)] for _ in range(9)])


def sudoku_solver(state: np.ndarray) -> np.ndarray:
    """
    Solves the given sudoku.
    :param state: 9x9 sudoku grid to solve
    :return: 9x9 solved sudoku grid, or error grid
    """
    result = backtrack(SudokuState(state))

    # Return result if valid
    if result is not None:
        return result.apply_solution()
    else:
        return SudokuState.error_grid


def backtrack(state: SudokuState) -> SudokuState or None:
    """
    Solve sudoku using backtracking
    :param state: State to solve
    :return: Solved state
    """
    # Pick a column
    pick = state.pick_constraint()

    # No more constraints to satisfy
    if pick is None:
        return None

    const, rows = pick
    values = sorted(list(rows))

    for rcv in values:
        # Using select_row and deselect_row means that we don't need to make (deep) copies of the state, which are
        # expensive.

        # Select the row, get and remove the associated columns
        columns = state.select_row(rcv)
        # Add rcv of row to solutions
        state.add_solution(rcv)

        # Return this state if it's correct
        if state.is_goal():
            return state

        # Continue working on this state
        deep_state = backtrack(state)
        if deep_state is not None and deep_state.is_goal():
            return deep_state

        # Deselect and remove rcv from solution, so that we can try the next rcv
        state.deselect_row(rcv, columns)
        state.remove_solution(rcv)
