# Sudoku Solver 🧩
An agent to solve sudoku puzzles by approaching them as exact cover problems.
This was coursework for my Artificial Intelligence module at University of Bath.
## Previous and Current  Performance
Previous attempts to write agents to solve sudokus yielded a **single hard solution** in around **40 seconds**, using backtracking and constriaint
propagation. After a variety of optimisations (such as caching, forward checking, predictions via distribution of 
numbers and writing my own `copy.deepcopy` function), this was reduced to about **2 seconds**. With the given target of 
under one second, I still wasn't satisfied.

After learning how to approach sudokus as **Exact Cover** Problems, and implementing what I'd learnt, what was taking 40
seconds before, now only takes **0.05 seconds**. 

## Usage
To obtain a solution, pass `sudoku_solver` a `numpy.ndarray((9,9), ...)`. Examples of input can be found in `/data`.
```python
import numpy as np

sudoku_state = np.ndarray(9,9) # Set values to sudoku grid to solve.
solution = sudoku_solver(state=sudoku_state)

print(solution) # This will print the solution, or a 9x9 grid of '-1'.
```

## Introduction
## Exact Cover Problems
### What is an Exact Cover Problem?
### Sudoku as an Exact Cover Problem
### Solving Exact Cover Problem
## Backtracking
## Optimisations
## Future Development
## References
