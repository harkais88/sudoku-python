#!/usr/bin/python3

import random

def initCellGen(table):
    for cell in range(0,9,3): #Cell here should represent the cell number we are working with
        fillCell(table,cell)
    return table

def fillCell(table,cell): #Plan here is we would essentially be accessing the diagonal elements. 
    nolist = [1,2,3,4,5,6,7,8,9]
    for i in range(3):
        for j in range(3):
            while True:
                num = random.choice(nolist)
                if unUsedNum(table,cell,num):
                    break        
            table[cell+i][cell+j] = num
            nolist.remove(num)


#Should check for all numbers in particular cell
def unUsedNum(table,cell,num):
    for i in range(3):
        for j in range(3):
            if table[cell+i][cell+j] == num:
                return False
    return True


if __name__ == "__main__":
    table = [[0 for _ in range(9)] for _ in range(9)] #Should initialize a list of lists with all elements as 0

    table = initCellGen(table)

    for row in table:
        print(row,"\n")


