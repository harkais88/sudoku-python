#!/usr/bin/python3

import sudokuGridGen as sgg
import random

#Should Delete Random Cells from Grid
def randCellDelete(table,noOfClues):
    counter = 0
    while counter < 9*9 - noOfClues:
        chck = False
        while chck == False:
            i = random.randint(0,8)
            j = random.randint(0,8)
            if table[i][j] != 0:
                table[i][j] = 0
                chck = True
        counter += 1
    for row in table:
        print(row, "\n")


#Main Purpose here: Create a generic terminal Sudoku Game :)
if __name__ == "__main__":
    chck = 0
    while chck < 1 or chck > 4:
        diff = int(input("\n CHOOSE YOUR DIFFICULITY: 1)EASY 2)MEDIUM 3)HARD 4)IMPOSSIBLE: "))
        if diff < 1 or diff > 4:
            print("\n Try entering the number")
        chck = diff
        
    table = sgg.sudokuGridGen()

    """
    According to the minimum number of givens in Sudoku, there should be atleast 17 clues for
    a Sudoku puzzle to be solved using logic and not random guessing. Adhering to this, I am 
    setting the difficulities as follows, and note this is of personal taste:

    Impossible: 17-24 clues
    Hard: 25-30 clues
    Medium: 31-34 clues
    Easy: 35-45 clues

    May need to look into these ranges later. Plan is to randomly select between these ranges 
    based on difficulity.

    However, this may not be a guarentee that a good Sudoku Puzzle is generated. Need to develop 
    a sudoku solver that can solve the generated puzzle using logic only, and would score the puzzle if it is good. The puzzle would be best if it only has 1 solution.
    """

    if diff == 1:
         noOfClues = random.randint(35,45)
    elif diff == 2:
        noOfClues = random.randint(31,34)
    elif diff == 3:
        noOfClues = random.randint(25,30)
    else:
        noOfClues = random.randint(17,24)

    
    randCellDelete(table,noOfClues) 

