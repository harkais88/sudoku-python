#!/usr/bin/python3

import random

def initCellGen(table):
    #print("\n Making our Diagonal Cells")
    for cell in range(0,9,3): #Cell here should represent the cell number we are working with
        #print("\n Working with the {},{} index".format(cell,cell))
        initFillCell(table,cell,cell)
    return table

#Would generate the diagonal cells
def initFillCell(table,row,col): 
    nolist = [1,2,3,4,5,6,7,8,9]
    nolist_cp = nolist
    for i in range(3):
        for j in range(3):
            while True:
                if len(nolist_cp) < 2:
                    num = nolist_cp[0]
                else: 
                    num = random.choice(nolist_cp)
                #print("\n Seeing if num = {} can be placed in {},{}".format(num,row+i,col+j))
                if unUsedNum(table,row,col,num):
                    break
                else:
                    nolist_cp.remove(num)

            table[row+i][col+j] = num
            #print("\n {} placed in {},{}".format(num,row+i,col+j))
            nolist.remove(num)
            nolist_cp = nolist


#Should check for all numbers in particular cell
def unUsedNum(table,row,col,num):
    for i in range(3):
        for j in range(3):
            if table[row+i][col+j] == num:
                #print("\n num = {} found in {},{}, hence can't be placed in this cell".format(num,row+i,col+j))
                return False
    #print("\n num = {} can be safely placed".format(num))
    return True

#For filling up the remaining cells
def remainCellGen(table,i,j):
    #Check if we reached end of table
    if i == 8 and j == 9:
        return True

    #Check if row is filled
    if j == 9:
        i += 1
        j = 0

    #Check if cell is filled, this should happen at 4th row 4th column
    #If not, moves to next cell on right
    if table[i][j] != 0:
        return remainCellGen(table,i,j+1)

    #Now the magic, let's try putting some value in there
    #Iterating through all numbers and checking if they can get placed there
    for num in range(1,10): 
        if checkSafe(table,i,j,num):
            table[i][j] = num
            
            #The backtracking takes place here in mode of recursion, if this function returns false, which means a certain cell was not able to accept any value, it would return here, otherwise this function returns true
            if remainCellGen(table,i,j+1):                
                return True
            
            #If the above function returns false, that means the num should not be placed in that cell, so we try with another number
            table[i][j] = 0

    #In case we reach here, it means no num worked in the cell i,j, so we return false
    return False


#Checks if num is safe to place in cell
def checkSafe(table,i,j,num):
    #Perform row check
    for k in range(0,9):
        if table[i][k] == num:
            return False
        
    #Perform column check
    for k in range(0,9):
        if table[k][j] == num:
            return False

    #Perform cell check, and if all passed, the cell check function itself passes True
    return unUsedNum(table,i - i%3,j - j%3,num) #A nifty trick to avoid index error here, ex - for 0,7, parameter passed to unUsedNum is 0 - 0%3 = 0, 7 - 7%3 = 6 => 0,6, which is the uppermost left side cell we are currently working with

#if __name__ == "__main__": #Only if this script needs to run
def sudokuGridGen():
    table = [[0 for i in range(9)] for i in range(9)] #Should initialize a list of lists with all elements as 0

    table = initCellGen(table)

    remainCellGen(table,0,3) #Should then start filling from the 1strow 4column element

    return table #Comment this line when running this script only


