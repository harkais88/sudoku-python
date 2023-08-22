#!/usr/bin/python3

import math
import random
import copy
import time
#import art

class sudoku:
    def __init__(self, n, choice):
        self.n = n
        self.table = [[0 for i in range(n)] for i in range(n)]
        self.grid = [row[:] for row in self.sudokuGridGen()]
        self.diff = self.diffset(choice)
        self.puzzle = self.sudokuPuzzleGen()
        #print("\n Printing the grid")
        #self.printTable(self.grid)
        #print("\n Printing the puzzle")
        #self.printTable(self.puzzle)

    def i_sqrt(self):
        return int(math.sqrt(self.n))

    def sudokuGridGen(self):
        self.initGroupGen()
        self.sudokuSolver(self.table,0,3)
        return self.table

    def initGroupGen(self):
        for i in range(0,self.n,self.i_sqrt()):
            self.initGroupFill(i,i)
        
    def initGroupFill(self, row, col):
        numbers = [i for i in range(1,self.n +1)]
        numbers_cp = numbers.copy()
        
        num = 0

        for i in range(self.i_sqrt()):
            for j in range(self.i_sqrt()):
                while True:
                    if len(numbers_cp) < 2:
                        num = numbers_cp[0]
                        break
                    else:
                        num = random.choice(numbers_cp)

                    if self.unUsedNum(self.table,row,col,num):
                        break
                    else:
                        numbers_cp.remove(num)

                self.table[row+i][col+j] = num
                numbers.remove(num)
                numbers_cp = numbers.copy()

    def unUsedNum(self,table,row,col,num):
        for i in range(self.i_sqrt()):
            for j in range(self.i_sqrt()):
                if table[row+i][col+j] == num:
                    #print("\n {} cannot be placed in group starting with {},{}".format(num,row,col))
                    return False
        return True

    def printTable(self, table): #For testing purpose only
        print()
        for i in range(self.n):
            for j in range(self.n):
                if table[i][j] != 0:
                    print(" " + str(table[i][j]) + " ",end = "")
                else:
                    print("   ",end = "")
                if (j+1) % self.i_sqrt() == 0 and j != self.n - 1:
                    print(" | ",end="")
            print()
            if (i+1) % self.i_sqrt() == 0 and i != self.n - 1:
                print(" - - - - - - - - - - - - - - - - -")
        print()

    def sudokuSolver(self, table, row = 0, col = 0):
        #print("Checking with {},{}".format(row,col))
        if row == self.n - 1 and col == self.n:
            return True

        if col == self.n:
            row += 1
            col = 0

        if table[row][col] != 0:
            return self.sudokuSolver(table,row,col+1)

        numbers = [i for i in range(1,self.n + 1)]

        num = 0
        while len(numbers) > 0:
            #print("\n Enters loop")
            if len(numbers) < 2:
                num = numbers[0]
            else:
                num = random.choice(numbers)

            if self.checkSafe(table,row,col,num):
                #print("\n Placing {} at {},{}".format(num,row,col))
                table[row][col] = num
                if self.sudokuSolver(table,row,col+1) == False:
                    #print("\n Cannot work at placing {} at {},{}".format(num,row,col))
                    table[row][col] = 0
            #print("\n Failed checkSafe")
            numbers.remove(num)

        if table[row][col] == 0:
            return False
        
    def checkSafe(self,table,row,col,num):
        for i in range(self.n):
            if table[row][i] == num:
                #print("\n {} cannot be placed in row {}".format(num,row))
                return False

        for j in range(self.n):
            if table[j][col] == num:
                #print("\n {} cannot be placed in col {}".format(num,col))
                return False

        return self.unUsedNum(table, row - (row % self.i_sqrt()), col - (col % self.i_sqrt()), num)

    def diffset(self,choice):
        if choice == 1:
            return (self.n+2)*self.i_sqrt() + random.randint(2,4*self.i_sqrt())
        elif choice == 2:
            return (self.n+1)*self.i_sqrt() + random.randint(1,self.i_sqrt() + 1)
        elif choice == 3:
            return (2*self.n) + (2*self.i_sqrt()) + random.randint(1,2*self.i_sqrt())
        elif choice == 4:
            return (self.i_sqrt() + 2)*self.i_sqrt() + random.randint(2,self.n)
        else:
            return -1

    def randomCellDelete(self,grid):
        table = [row[:] for row in grid]
        chck = 0
        while chck < (math.pow(self.n,2) - self.diff):
            row = random.randint(0,self.n - 1)
            col = random.randint(0,self.n - 1)

            if table[row][col] != 0:
                table[row][col] = 0
                chck += 1

        return table

    def sudokuPuzzleGen(self):
        puzzle_log = []
        self.puzzle = []

        try:
            while True:
                #print(art.text2art("Puzzle Gen",font="block"))
                #print("\n Starting our puzzle gen")
                puzzle = self.randomCellDelete(self.grid)

                if puzzle in puzzle_log:
                    continue

                self.puzzle = [row[:] for row in puzzle]
                #print("Our Puzzle")
                #self.printTable(self.puzzle)
                #time.sleep(2)

                counter = 0

                while counter < 20:
                    puzzle = [row[:] for row in self.puzzle]
                    self.sudokuSolver(puzzle)
              
                    """
                    print("\n The Solved Puzzle")
                    self.printTable(temp)
                    #time.sleep(2)
                    print("\n self.puzzle at this point")
                    self.printTable(self.puzzle)
                    #time.sleep(2)
                    print("\n Our Original Grid")
                    self.printTable(self.grid)
                    """

                    #time.sleep(3)

                    if puzzle != self.grid:
                        #print("\n Puzzle != Grid!")
                        #time.sleep(2)
                        break

                    #temp = [row[:] for row in self.puzzle]
                    #print("\n Returning to our original puzzle: ")
                    #self.printTable(temp)
                    #time.sleep(2)
                    counter += 1

                if counter == 20:
                    #print("\n Successful Puzzle Gen")
                    #time.sleep(2)
                    break
                #time.sleep(2)
                #print("Trying again?")
                puzzle_log.append(self.puzzle)
        except KeyboardInterrupt:
            print("\n Our Grid")
            self.printTable(self.grid)
            print("\n At this point, number of puzzles generated from our grid: ",len(puzzle_log))
            print("\n Check results file for the puzzles generated")
            f = open("./results","w")
            for puzzle in puzzle_log:
                for i in range(self.n):
                    for j in range(self.n):
                        if puzzle[i][j] == 0:
                            f.write("   ")
                        else:
                            f.write(" " + str(puzzle[i][j]) + " ")
                        if (j+1) % 3 == 0 and j != self.n - 1:
                            f.write("| ")
                    f.write("\n")
                    if (i+1) % 3 == 0 and i != self.n - 1:
                        f.write("- - - - - - - - - - - - - - - - -")
                        f.write("\n")
                f.write("\n")
            f.close()
   
        print("\n Number of puzzles generated that were not unique: ",len(puzzle_log))
        return self.puzzle

    def sudokuGen(self):
        return self.grid,self.puzzle

if __name__ == "__main__":
    #For testing purposes
    start = time.time()
    diff = int(input("\n Difficulity Choices \n\n 1.EASY \t 2.Medium \t 3.Hard \t 4.Impossible (Untested) \n Enter your choice: ")) 
    obj = sudoku(9,diff)
    end = time.time()

    print("\n Time of Execution: ",end-start)

    grid,puzzle = obj.sudokuGen()

    obj.printTable(grid)
    obj.printTable(puzzle)
