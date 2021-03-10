# Sudoku Solver 🧩
An agent to solve sudoku puzzles using backtracking and constraint propagation. 
Coursework for my Artificial Intelligence module at University of Bath.

## Usage
How to run my code

### Input
Call `sudoku_solver(numpy.array)` the argument representing the state to solve from as a 2D array. This  converts the 
array to a `SudokuState` object and calls `backtrack(state)`.

Alternatively, call `backtrack(SudokuState)` directly, when using a `SudokuState` object as an argument.

### Output
`sudoku_solver(numpy.array)` returns a `numpy.array` containing either the solution in a 9x9 2D `numpy.array`, or the 
same format containing only the value `-1`.

## Introduction
Other than a simple state space search to solve a river-crossing problem [1], this was my first Artificial Intelligence
project. Considering that my solution can solve even the harder sudoku puzzles, I'm quite proud of it.

## What is Sudoku?
Sudoku is a number based puzzle where numbers are placed in a 9x9 grid in such a way that each column, row and subregion
(or "cube") contains exactly one of each digit between 1-9 (inclusively). The group of cells that a single cell is related
to (those in its row, column and cube) will be called the cell's **family** throughout this document.

**An unsolved sudoku puzzle**

![Example of unsolved sudoku puzzle](https://upload.wikimedia.org/wikipedia/commons/e/e0/Sudoku_Puzzle_by_L2G-20050714_standardized_layout.svg)

_Tim Stellmach, CC0, via Wikimedia Commons_

**The same sudoku puzzle, solved**

![Example of solved sudoku puzzle](https://upload.wikimedia.org/wikipedia/commons/1/12/Sudoku_Puzzle_by_L2G-20050714_solution_standardized_layout.svg)

_en:User:Cburnett, CC BY-SA 3.0 <https://creativecommons.org/licenses/by-sa/3.0>, via Wikimedia Commons_

## Techniques Used
In this section I will explain the techniques I have used in my submission.

### Backtracking
**Backtracking** is the algorithm that I used for my solution, as there is a lot of information about it throughout the
module, and proved to be efficient enough to solve the puzzles in an acceptable time.

#### What is Backtracking?
Backtracking starts with a state, and according to a chosen criteria (in this case, the `pick_next_cell` function: discussed further in _Constraint Propagation_), tries a
new state, with different values. This continues until a solution is found, or string of solutions is found to end
with a "losing" state (i.e. the goal state can't be reached from it). The algorithm then tries propagating other states,
working back up the string of states that has been produced.

#### Application
The algorithm starts with the provided sudoku state, and generates constraints based on the values already in place. 
Following these constraints, the next state is then generated based on criteria described later on. The algorithm then propagates
new constraints following the rules of sudoku and the state of the family, and a new, conforming state is made, with 
a new value in a new position. This continues as described before.

### Constraint Propagation
In order significantly reduce the search space for this problem, I implemented **Constraint Propagation** into my solution.
This means that the algorithm won't waste time trying values that are currently known to be impossible (i.e. the value 
`1` in a row that already contains an instance of the value `1`).

This was very natural to do, as a human would intuitively process the puzzle in a very similar manner.

#### What is Constraint Propagation?
Constraint Propagation is the process of continually reducing the set of valid actions, based on what you know about the 
problem you're trying to solve. This is done after each valid action, increasingly reducing the available paths that the
backtracking algorithm could take down an otherwise vast problem tree. 

#### Application
Upon loading the initial state, the algorithm will update the `possible_values` set for each cell on the grid. This is a 
set containing at most the numbers 1 through 9, and at least nothing (an empty set). Similarly, when any cell's value is
set, the `possible_values` set for all cells in the updated cell's family is updated by running the `update_possible_values`
method. 

An empty set indicates that there are no possible values for the given cell. If this is the case, and the cell is 
contains the value `0`, the sudoku is known to be unsolvable.

To pick the next cell to solve, my solution finds the cell with the least number of possible values, as solving the cheaper
cells first will ideally reduce the cost of the more expensive cells by increasing their constraints (and reducing the
length of their `possible_values` set). This is obvious in the direct application of cells in the same family, but is also
true for cross-family cases, causing a domino-effect throughout the board. 

### Forward Checking
To further reduce the time that my program takes to find a solution (particularly those to be considered "hard"), I 
implemented forward checking in the `order_values` function.

#### What is Forward Checking?
Forward checking is the act of checking whether a generated state is worth operating further on. The idea of this is for
the "forward checking" procedure to be cheaper than regular processing, so that resources are saved by not processing a
pre-determined "bad" state.

#### Application
In the context of my program, forward checking is performed on the resulting states from the `possible_values` set for 
each cell. Before a value is chosen to be placed in a cell, it is checked whether placing the generated state would be
solvable.

Deciding whether a given state is solvable is done by simply making sure that every `0` cell has a `possible_values` set
of non-zero length. This is done during the `update_possible_values` method. If a cell is unsolved and has no possible
values, we know the sudoku is impossible to solve.
## Optimisations
### Caching
### Frequency Checking
## Future Development
## References
[1] River Crossing Problem
