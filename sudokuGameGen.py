#!/usr/bin/python3

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
    Edit: Successfully made a Sudoku Solver, and successfully used it to generate unique solution puzzle grids
"""

import sudokuGridGen as sgg
from sudokuSolver import sudokuSolver
from copy import deepcopy
import playsound as pls
from colorama import Fore
from colorama import Style
import threading
import sys
import time

def printGrid(table,original = []):
    for i in range(len(table)):
        if i % 3 == 0 and i != 0:
            print(" - - - - - - - - - - - -")
        for j in range(len(table[i])):
            if j % 3 == 0 and j != 0:
                print(" | ", end="")
            if not original:
                if table[i][j] != 0:
                    print(" " + Fore.BLUE + str(table[i][j]) + Style.RESET_ALL,end = "")
                else:
                    print("  ",end = "")
            else:
                if table[i][j] != 0 and table[i][j] != original[i][j]:
                    print(" " + Fore.GREEN + str(table[i][j]) + Style.RESET_ALL,end = "")
                elif table[i][j] != 0:
                    print(" " + Fore.BLUE + str(table[i][j]) + Style.RESET_ALL,end = "")
                else:
                    print("  ",end = "")
        print()

#Should Delete Random Cells from Grid
def randCellDelete(sol,noOfClues):
    counter = 0
    while counter < 9*9 - noOfClues:
        chck = False
        while chck == False:
            i = sgg.random.randint(0,8)
            j = sgg.random.randint(0,8)
            if sol[i][j] != 0:
                sol[i][j] = 0
                chck = True
        counter += 1
    return sol

def diffInput():
    chck = 0
    while chck < 1 or chck > 4:
        diff = int(input("\n CHOOSE YOUR DIFFICULITY: 1)EASY 2)MEDIUM 3)HARD 4)IMPOSSIBLE: "))
        if diff < 1 or diff > 4:
            print("\n Try entering the number")
        chck = diff

    return diff

def diffSet(diff):
    if diff == 1:
         noOfClues = sgg.random.randint(35,45)
    elif diff == 2:
        noOfClues = sgg.random.randint(31,34)
    elif diff == 3:
        noOfClues = sgg.random.randint(25,30)
    else:
        noOfClues = sgg.random.randint(17,24)

    return noOfClues

def loading():
    animation = animation = ["[■□□□□□□□□□]","[■■□□□□□□□□]", "[■■■□□□□□□□]", "[■■■■□□□□□□]", "[■■■■■□□□□□]", "[■■■■■■□□□□]", "[■■■■■■■□□□]", "[■■■■■■■■□□]", "[■■■■■■■■■□]", "[■■■■■■■■■■]"]
    counter = 0
    while True:
        time.sleep(0.2)
        sys.stdout.write("\r"+ animation[counter % len(animation)])
        sys.stdout.flush()
        counter += 1


def sudokuGameGen(diff):
    #diff = diffInput()        

    noOfClues = diffSet(diff)

    sol = sgg.sudokuGridGen() #This variable is our solution

    #For printing the solution grid, use only in terminal
    #print("\n OUR SOLUTION")
    #printGrid(sol)

    #threading.Thread(target = loading,block=False)
    u_count = 0 #For optimizing unique solution grid gen
    original = []
    try:
        while u_count < 20:
            counter = 0
            puzzle = randCellDelete(sol,noOfClues) #This variable is our puzzle
        
            original = deepcopy(puzzle)

            while True: #Attempt at Creating a unique solution puzzle
                if counter == 20:
                    break
            
                """
                #For printing the puzzle grid, use only in terminal
                print("\n OUR PUZZLE")
                printGrid(puzzle)
                """
                
                #Solving our puzzle
                sudokuSolver(puzzle)

                """
                #For printing the solved puzzle grid
                print("\n OUR SOLVED PUZZLE")
                printGrid(puzzle)
                """

                if puzzle != sol:
                    #print("\n Does not give unique solution")
                    break

                puzzle = deepcopy(original)
                """
                print("\n Should copy the original puzzle")
                printGrid(puzzle)
                """

                counter += 1

            if counter == 20: #Means it gives a unique solution everytime
                #print("\n A unique solution grid")
                #printGrid(original)
                pls.playsound('content/music/start.mp3',block=False)
                #threading.Event().set()
                return original,sol,noOfClues #This function returns a tuple of the puzzle and the solution

                #print("\n The solution to this grid")
                #printGrid(sol)

            #else:
                #print("\n Is not a unique solution grid")

            u_count += 1
            #print("\n u_count increased to ",u_count)
    except KeyboardInterrupt:
        print("I am so sorry for the trouble, if you wish, there is a good chance it will generate a good one upon re-execution. Otherwise, feel free to try out the medium or easy puzzles. Again, I am very sorry for this :(")


    if u_count == 20: #Meaning it was not able to produce a unique puzzle grid with current solution grid
        #print("\n Retrying with different solution grid")
        return sudokuGameGen(diff) #In that case, we run the same loop again

#Main Purpose here: Create a generic terminal Sudoku Game :)
#Execute this script when testing for game generation
if __name__ == "__main__":
    original,sol = sudokuGameGen()

    print("\n Puzzle Grid")
    printGrid(original)
    print("\n Solution")
    printGrid(sol)


