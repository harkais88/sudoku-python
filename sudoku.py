#!/usr/bin/python3

import random

def initCellGen(table):
    for cell in range(0,9,3): #Cell here should represent the cell number we are working with
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
                if unUsedNum(table,row,col,num):
                    break
                else:
                    nolist_cp.remove(num)
            table[row+i][col+j] = num
            nolist.remove(num)
            nolist_cp = nolist


#Should check for all numbers in particular cell
def unUsedNum(table,row,col,num):
    for i in range(3):
        for j in range(3):
            if table[row+i][col+j] == num:
                return False
    return True


if __name__ == "__main__":
    table = [[0 for _ in range(9)] for _ in range(9)] #Should initialize a list of lists with all elements as 0

    table = initCellGen(table)

    for row in table:
        print(row,"\n")


