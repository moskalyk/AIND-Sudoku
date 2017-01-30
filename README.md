# Artificial Intelligence Nanodegree
## Introductory Project: Diagonal Sudoku Solver

# Question 1 (Naked Twins)
Q: How do we use constraint propagation to solve the naked twins problem?  
A: Constraint propogation is utilized in solving the naked twins problem, by adding new constraints that the variables must satisfy. For example, one condition that the AI agent must satisfy, is the fact that if there are 2 boxes with identical possible value pairs (e.g. 23 & 23 within the same square unit) in them, then all peer units that are connected to those twin pairs, will definitely not contain either one of thsoe values. This leads to simplification of harder sudoku problems, by eliminating more 'possible' values after simple 'elimination', 'only choice', and 'search' strategies can the reduce the board to.

# Question 2 (Diagonal Sudoku)
Q: How do we use constraint propagation to solve the diagonal sudoku problem?  
A: Similiar to question one, but in this scenario we add new domain variables containing additional unit sets to contrain the program by. For example, instead of having to have number 1-9 in each row, column, and 3x3 square, the program is also constrained by having to successfully have all 1-9 numbers in a diagonal across the board in the following box indices (A1, B2, .., I9 and A9, B8 .., I1). Therefore 2 more units were added to the list of units to also confirm when new numbers were place on the board, they abide by the diagonal rules.

### Install

This project requires **Python 3**.

We recommend students install [Anaconda](https://www.continuum.io/downloads), a pre-packaged Python distribution that contains all of the necessary libraries and software for this project. 
Please try using the environment we provided in the Anaconda lesson of the Nanodegree.

##### Optional: Pygame

Optionally, you can also install pygame if you want to see your visualization. If you've followed our instructions for setting up our conda environment, you should be all set.

If not, please see how to download pygame [here](http://www.pygame.org/download.shtml).

### Code

* `solutions.py` - You'll fill this in as part of your solution.
* `solution_test.py` - Do not modify this. You can test your solution by running `python solution_test.py`.
* `PySudoku.py` - Do not modify this. This is code for visualizing your solution.
* `visualize.py` - Do not modify this. This is code for visualizing your solution.

### Visualizing

To visualize your solution, please only assign values to the values_dict using the ```assign_values``` function provided in solution.py

### Data

The data consists of a text file of diagonal sudokus for you to solve.
