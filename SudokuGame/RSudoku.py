#!/usr/bin/python3

"""Acts as an revised version of my previous code, as I see that there are a lot of things that can be improved"""

import numpy as np
from copy import deepcopy
from timeit import default_timer

class sudoku:
    """
    sudoku(choice = 1)
    
    Class for generating a 9x9 sudoku grid and puzzle
    
    Notable Variables:
    grid - Is the Generated Complete Sudoku Grid
    puzzle - Is a valid unique puzzle created out of the grid
    choice - Is the Difficulity Choice
        1 - Easy
        2 - Medium
        3 - Hard (Generates after a long time)
        4 - Impossible (Does not generate anything)
    """

    def __init__(self,choice = 1):
        if choice == 0:
            self.grid = np.empty([9,9])
            self.puzzle = np.empty([9,9])
        else:
            self.grid = self.initGrid()
            self.choice = choice
            self.uniquePuzzle()

    @staticmethod
    def diffSet(choice: int):
        """Sets number of cells that will be deleted from the grid"""
        diffMap = {1: np.random.randint(35,46), 2: np.random.randint(31,35), 3: np.random.randint(25,31),
                   4: np.random.randint(17,25)}
        return diffMap[choice]

    def initGrid(self):
        """Generates a valid sudoku grid"""
        self.table = np.zeros((9,9),dtype=int)
        for i in range(0,9,3): self.cellFill(self.table,i);
        self.solver(self.table,0,3)
        return self.table

    @staticmethod
    def cellFill(table,i: int):
        """Fills in the left diagonal groups in the grid"""
        nums = np.random.choice(np.arange(1,10),9,replace=False)
        count = 0
        for j in range(3):
            for k in range(3): table[i+j][i+k] = nums[count]; count += 1;

    def solver(self,table,row = 0,col = 0):
        """Solves a sudoku puzzle using backtracking"""
        if row == 8 and col == 9: return True;    
        if col == 9: row += 1; col = 0;
        if table[row][col] != 0: return self.solver(table,row,col+1);

        for i in np.random.choice(np.arange(1,10),9,replace = False):
            if self.checkSafe(table,row,col,i):
                table[row][col] = i
                if self.solver(table,row,col+1): return True;
                table[row][col] = 0

        return False;

    def checkSafe(self,table,row,col,num):
        """Checks if a number is safe to place in a cell specified by row and col"""
        # Row Check
        for i in range(9):
            if table[row][i] == num: return False;

        # Col Check
        for i in range(9):
            if table[i][col] == num: return False;

        return self.cellCheck(table,row - row%3,col - col%3,num)
    
    @staticmethod
    def cellCheck(table,row,col,num):
        """Checks to see if number is safe to place in a group specified by row and col"""
        for i in range(3):
            for j in range(3):
                if table[row+i][col+j] == num: return False;
        return True

    def uniquePuzzle(self):
        """Generates a unique puzzle from a completed grid"""
        while True:
            self.puzzle = self.puzzleGen()
            counter = 0

            while counter < 20:
                t_puzzle = np.array(self.puzzle)
                self.solver(t_puzzle)
                if not np.all(np.equal(t_puzzle,self.grid)): break;
                counter += 1

            if counter == 20: break;
    
    def puzzleGen(self):
        """Deletes random cells from the grid and presents a puzzle with one or more solutions"""
        puzzle = deepcopy(self.grid)
        count = 0
        while count < 81 - self.diffSet(self.choice):
            i,j = np.random.randint(0,9),np.random.randint(0,9) 
            if puzzle[i][j] != 0: puzzle[i][j] = 0; count += 1;
        return puzzle

    @staticmethod
    def printTable(table):
        """Prints the table in sudoku format"""
        print()
        for i in range(9):
            for j in range(9):
                if table[i][j] != 0: print(" " + str(table[i][j]) + " ",end = "");
                else: print("   ",end = "");
                if (j+1) % 3 == 0 and j != 8: print(" | ",end="");
            print()
            if (i+1) % 3 == 0 and i != 8: print(" - - - - - - - - - - - - - - - - -");
        print()

if __name__ == "__main__":
    start = default_timer()
    try:
        puzzle = sudoku(3) #For a hard puzzle
        print("Total Time Execution: ",default_timer() - start)
        print("\n Generated Grid")
        puzzle.printTable(puzzle.grid)
        print("\n Generated Puzzle")
        puzzle.printTable(puzzle.puzzle)
    except KeyboardInterrupt:
        print("Total Time passed: ",default_timer() - start)