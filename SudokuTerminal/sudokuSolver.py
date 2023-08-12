#!/usr/bin/python3

from sudokuGridGen import random,checkSafe

def sudokuSolver(puzzle,row=0,col=0):
    if row == 8 and col == 9:
        return True

    if col == 9:
        row += 1
        col = 0

    if puzzle[row][col] != 0:
        return sudokuSolver(puzzle,row,col+1)

    nolist = [i for i in range(1,9+1)]

    while puzzle[row][col] == 0 and len(nolist) >= 1:
        num = random.choice(nolist) 
        if checkSafe(puzzle,row,col,num):
            puzzle[row][col] = num
            if sudokuSolver(puzzle,row,col+1) == False:
                puzzle[row][col] = 0
        nolist.remove(num)

    if puzzle[row][col] == 0:
        return False

"""
#Use when executing this script only

if __name__ == "__main__": 
    #Puzzles with unique solution, for testing purposes
    #puzzle = [[2,0,0,9,4,6,8,0,1],[9,0,0,1,0,0,0,7,2],[6,1,3,7,0,8,0,0,0],[8,0,0,0,0,0,0,0,0],[1,0,6,0,0,0,0,8,4],[7,4,0,8,0,2,0,9,0],[4,0,0,5,0,0,0,6,3],[5,6,1,0,7,0,0,2,0],[0,7,8,2,0,0,4,1,0]]
    #puzzle = [[0,0,7,0,0,6,8,0,2],[0,0,0,2,0,8,7,0,0],[2,8,0,0,0,3,1,0,6],[6,7,2,5,0,0,9,0,0],[0,4,9,8,0,0,6,0,0],[0,3,1,0,4,9,0,5,0],[0,1,0,9,0,0,3,7,8],[0,6,3,0,0,5,0,2,0],[9,0,0,3,0,0,5,0,0]]

    #Puzzles with more than one solution
    puzzle = [[5,6,0,0,0,8,0,0,0],[7,0,3,0,5,0,4,8,0],[0,1,2,7,9,0,6,5,3],[2,7,9,0,1,0,5,0,6],[0,0,8,4,6,0,0,2,0],[4,0,0,5,0,0,0,0,8],[3,4,0,9,7,0,0,6,0],[0,0,7,0,0,0,9,1,4],[0,0,5,0,0,0,7,0,0]]

    sudokuSolver(puzzle)

    for row in puzzle:
        print("\n",row)
"""
