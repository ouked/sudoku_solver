# Sudoku Solver 🧩

An agent to solve sudoku puzzles by approaching them as exact cover problems. This was coursework for my Artificial
Intelligence module at University of Bath.

## Previous & Current  Performance

Previous attempts to write agents to solve sudokus yielded a **single hard solution** in around **40 seconds**, using
backtracking and naive constraint propagation. After a variety of optimisations (such as caching, forward checking,
predictions via distribution of numbers and writing my own `deepcopy` function), this was reduced to about **2 seconds**
. With the given target of under one second, I still wasn't satisfied.

After learning how to approach sudokus as **exact cover** problems, and implementing Donald Knuth's Algorithm X, what
was taking 40 seconds before, now only takes **0.03 seconds**.

## Usage

To obtain a solution, pass `sudoku_solver` a `numpy.ndarray((9,9), ...)`. Examples of input can be found in `/data`.

```python
import numpy as np

sudoku_state = np.ndarray((9, 9), ...)  # Set values to sudoku grid to solve.
solution = sudoku_solver(state=sudoku_state)

print(solution)  # This will print the solution, or a 9x9 grid of '-1'.
```

## Introduction

This was a deeply engaging and educative challenge that I spent a lot of time on. I'm very proud of the results my work
has yielded.

## Exact Covers

### What is an Exact Cover?

An **exact cover** is a collection of subsets of `S` such that every element in `S` is found in _exactly one_ of the
subsets.

#### Example

Given a set `S` and the subsets `A`, `B`, `C`, `D`, `E`:

- `S = {1, 2, 3, 4, 5, 6, 7}`


- `A = {1, 6, 7}`

- `B = {1, 3, 5}`

- `C = {2}`

- `D = {3, 4, 5}`

- `E = {1, 2, 3, 4}`

Then the exact cover of `S` is the sets `A`, `C`, `D`:

- ```A ∪ C ∪ D = S``` (The subsets cover _every_ element in `S`)


- ```A ∩ C ∩ D = {}``` (Every element in `S` is covered by _only one_ set)

### Solving Exact Cover Problems with Donald Knuth's Algorithm X

Before we discuss how we solve sudokus specifically, let's explore how to solve a _general_ exact cover problem.

**Algorithm X** solves exact cover problems by using a matrix `A`, consisting of 1s and 0s. Let's put the above example
such a matrix.

|     | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|:---:|---|---|---|---|---|---|---|
| A   | 1 | 0 | 0 | 0 | 0 | 1 | 1 |
| B   | 1 | 0 | 1 | 0 | 1 | 0 | 0 |
| C   | 0 | 1 | 0 | 0 | 0 | 0 | 0 |
| D   | 0 | 0 | 1 | 1 | 1 | 0 | 0 |
| E   | 1 | 1 | 1 | 1 | 0 | 0 | 0 |

Taken from the [Wikipedia Page](https://en.wikipedia.org/wiki/Knuth%27s_Algorithm_X):
> 1) If the matrix A has no columns, the current partial solution is a valid solution; terminate successfully.
> 2) Otherwise choose a column c (deterministically).
> 3) Choose a row r such that Ar, c = 1 (nondeterministically).
> 4) Include row r in the partial solution.
> 5) For each column j such that Ar, j = 1,
     >

1) for each row i such that Ai, j = 1,
   >
1) delete row i from matrix A.

>     2) delete column j from matrix A.
> 6) Repeat this algorithm recursively on the reduced matrix A.

In simpler terms, the algorithm takes an element `e` to cover, and finds a row which does this. This row is added to our
solution, and every row that also covers `e` is removed from `A`, along with every column that the chosen row also
satisfies.

Selecting row `A`, and doing this described reduction leads to the reduced matrix `A`:

|     | 2 | 3 | 4 | 5 |
|:---:|---|---|---|---|
| C   | 1 | 0 | 0 | 0 |
| D   | 0 | 1 | 1 | 1 |

`Solution = {A}`

- Row `A` was removed and **added to our solution**.
- Rows `B` and `E` were removed because they also covered `1`.
- Columns `1`, `6`, `7` were removed because they were covered by row `A`.

You can see how doing the same steps again will reduce this matrix further, and will lead to a valid solution being
found.

### Sudoku as an Exact Cover Problem

To approach sudoku as an exact cover problem, you must step back from the sudoku grid, and think about what a solved
sudoku contains:

- A set of **filled cells**
- A set of **rows**, each with one of each number `1-9`
- A set of **columns**, each with one of each number `1-9`
- A set of **blocks**, each with one of each number `1-9`

... and we can also think about what it means to write a value `v` to a cell `(row, col)` in the grid:

- This unique combination of parameters (row, column and value) will contribute to satisfying a unique combination of
  the constraints listed above.
- No other cell in the row, column, or block that this cell exists in, can hold the same value `v`.

From what we've realised from the nature of sudoku puzzles, we can construct our matrix `A`, to represent our
constraints and associated **row, column, value** (RCV) combinations. The following is a few rows and columns from the
expansive matrix:

|                      | 0,0,1 | 0,0,2 |   | 4,4,1 |
|----------------------|-------|-------|---|-------|
| Cell 0,0 has a value | 1     | 0     |   |   0   |
| Cell 0,1 has a value | 1     | 0     |   |   0   |
||
| Row 0 contains a 1   | 1     | 0     |   |   0   |
| Row 0 contains a 2   | 0     | 1     |   |   0   |
||
| Col 0 contains a 1   | 1     | 0     |   |   0   |
| Col 0 contains a 2   | 0     | 1     |   |   0   |
||
| Block 4 contains a 1 | 0     | 0     |   |   1   |

Now that we have our matrix `A`, we can apply Algorithm X to generate solutions.

## My Implementation of Algorithm X

After `sudoku_solver` is passed the initial state, it passes it on to `backtrack`, which is the main driver function.
This is where Algorithm X is executed.

Due to python naming conventions, the matrix `A` is referred to as `a` throughout my code.

`pick_constraint` will find the constraint with the smallest number of satisfying RCV tuples, which relate to rows in
matrix `A`. These rows are tried in term, just as described before.

### Backtracking

As the first series of rows that are tried will likely **not** be the solution, eventually the algorithm will backtrack.
Initially this was facilitated by creating a deep copy of the `SudokuState` object at each level of the recursion,
creating independent copies of mutable fields (namely `A`), to allow changes to be undone. However, creating these
copies was inefficient and slowed the algorithm down significantly.

After attempting to fix this by overriding `SudokuState`'s `deepcopy` function with a specialised and therefore faster
function, I decided it would be better to use the same object, and instead store changes to the matrix in the
appropriate recursion level in the list named `columns`. As the algorithm works back up the recursion levels, it will
undo these changes, restoring the matrix back to how it was for the level above it.

### Constraint Propagation

The act of removing rows and columns after a row is selected is a strict and efficient way of propagating constraints.

## Optimisations

Not all the following are in my final solution, but they should still be mentioned.

### Caching

Before using Algorithm X, I decreased the processing time significantly by caching rows, column and blocks that had
already been validated in a shared dictionary for all puzzles. Rows, columns and blocks can all be considered
equivalent, as they all require one of each value `1-9`, regardless of order. Blocks were **flattened** to make them
compatible with the rows and columns.

Part of the success of this optimisation was the fact that the algorithm would spend slightly longer on the faster
puzzles, such as those classed as "very_easy", "easy", or "medium", to speed up the processing of the slower puzzles.

It was faster to store the permutations (where order matters) instead of the combinations (where order doesn't matter),
so the algorithm would generate 24806 permutations from the testing data, compared to the 520 possible combinations.
This obviously increased space complexity of the algorithm dramatically, but I was just trying to reduce the processing
time.

Now that the code uses Algorithm X, there is no need to check for valid combinations of numbers, so there currently is
no caching.

### Specialised `deepcopy` method

Profiling my code uncovered the fact that `deepcopy` was taking up the most processing time, so I needed to reduce the
time it took.

As the `copy.deepcopy` function is made to make an independent copy of an arbitrary object, it will be doing a lot of
unnecessary processing in this context. Looking in `copy.py` shows the amount of checks that occur everytime a copy is
needed. These checks would be necessary if the object I was copying contained references to itself, however it doesn't.

Writing a new `deepcopy` method was as simple as creating a new object of the same class, and setting the fields to the
values of the copied object.

Here is what the specialised `deepcopy` looked like.

```python
def __deepcopy__(self, memodict={}):
    """
    Perform a deepcopy on SudokuState.
    IMPORTANT: New fields added to the class SudokuState also need to be added here.
    :return: New object
    """

    cls = self.__class__
    state = cls.__new__(cls)
    state.values = self.values
    state.a = {k: set(self.a[k]) for k in self.a.keys()}  # set() is quicker than copy()
    state.solvable = self.solvable
    state.solution = self.solution
    return state
```

> **Note**: This is a precise, fast and error-prone way of copying an object. This approach requires you to update `deepcopy`
> everytime a new field is added to the class that is being copied.


This was being used for a while in my new exact cover solution, though now it uses the `select_row`,  `deselect_row`,
`add_solution` and `remove_solution` functions to make and undo changes made to the same object through the recursions.

### Selecting and Deselecting Rows

Instead of making a whole copy of an object just to change a few values in the huge matrix, it is much faster to use the
same object throughout the algorithm and keep track of the changes that you have made, and then reverting these changes
before returning.

### Removed Enums

To reduce bugs and improve readability, I was using enums for constraints. This meant that typos would be instantly
recognised. However, after investigating, I found that just using strings is much faster.

As this change was made after the majority of development, it meant that no typo-induced bugs were introduced.

## Learning Outcomes

### Depth-First Search, Constraint Propagation and Forward Checking

### Exact Cover Problems and Knuth's Algorithm X

### Implementing Previously-Theoretical Ideas

### Python's Enums are Slow

### How to Spell "Sudoku"

My poor spell checker.

## Future Development

## References
