#!/usr/bin/python3

#DEV NOTES: Attempted to introduce a thread that relies on a keyboard press, however keyboard library has a lot of hassle
#Could try with pynput, if successful, will be v1.1
#As of now, successful puzzle generation, successful playing in terminal, however hint giving and exit functions not provided 

#IMP NOTE: THIS SERVES AS THE PROTOTYPE TO THE MAIN SUDOKU GAME THAT IS TO BE CREATED IN PYGAME. THAT BEING SAID, HAVE FUN WITH THIS ONE. 
#THIS WILL BE CONSIDERED THE BASIS OF v1.0

from sudokuGameGen import sudokuGameGen,diffInput,printGrid,sgg,Fore,Style,deepcopy
from colorama import Back
import os
import keyboard
#from sys import exit
import threading 
import art
import playsound as pls

hint_chck = False

def filledGrid(puzzle):
    for row in range(9):
        for col in range(9):
            if puzzle[row][col] == 0: #Meaning that the grid is not completely filled
                return False
    return True


"""def menuSys(puzzle,sol):
    global hint_chck
    while True:
        if keyboard.is_pressed("m"):
            os.system('clear')
                    
            while True:
                print("\n Menu System Activated, Select an option: \n 1) Give a hint 2) Exit \n System will continue running until right key is pressed")

                if keyboard.is_pressed("1"):
                    if hint_chck == False:
                        os.system('clear')
                        printGrid(puzzle)
                        print("\n Enter the row and column number of the cell you want revealed: ")
                        row = int(input("\n Enter the row number: ")) - 1
                        col = int(input("\n Enter the column number: ")) - 1
                        puzzle[row][col] = sol[row][col]
                        print("\n Cell Revealed")
                        hint_chck = True
                    else:
                        print("\n Sorry, no more hints allowed")
                    break
                    
                elif keyboard.is_pressed("2"):
                    os.system('clear')
                    print("\n Oh man, nice try!! Try again, we believe in you!")
                    print("\n The solution to this puzzle")
                    printGrid(sol)
                    exit()
                else:
                    os.system('clear')
                    continue"""

def numbers_left(num,puzzle):
    counter = 0
    for i in range(9):
        for j in range(9):
            if puzzle[i][j] == num:
                counter += 1
    if counter == 9: #Meaning there are 9 nums in the grid, which is true for a sudoku grid, check it out yourself
        return True
    return False


def bgm(): 
    music = ['content/music/bgm.mp3', 'content/music/bgm2.mp3', 'content/music/bgm3.mp3', 'content/music/bgm4.mp3']
    while True:
        pls.playsound(sgg.random.choice(music))    
    

if __name__ == "__main__":
    #Generate puzzle and solution to puzzle
    os.system('clear')
    
    threading.Thread(target=bgm, daemon=True).start() #For playing the background music

    print(Fore.CYAN + art.text2art("SUDOKU!!",font="epic") + Style.RESET_ALL)
    diff = diffInput()
    puzzle,sol,noOfClues = sudokuGameGen(diff)
    nolist = [i for i in range(0,9)]
    original = deepcopy(puzzle)

    error_counter = 0
    
    remarks = ["Nice!","Awesome!!","Not bad bro!","Cool!","Heck yeah!","Toastie!","High Five!","Sodutastic!!","Tasty!","Mmm, nice ;)"]
    streak = 0
    score = 0

    os.system('clear')
    try:
        while filledGrid(puzzle) == False:

            #pls.playsound('content/bgm.mp3')
            
            if error_counter >= 3:
                break

            if streak != 0:
                print("\n On a roll man, current streak: {} \n".format(streak))

            #os.system('clear')
            print(Fore.CYAN + art.text2art("SUDOKU!!",font="epic") + Style.RESET_ALL)
            printGrid(puzzle,original)
            print("\n Numbers Left! : ",end="")
            for i in [1,2,3,4,5,6,7,8,9]:
                if numbers_left(i,puzzle) == False:
                    print(" {}".format(i),end="")

            print("\n\n Choose a grid to fill in! \n To Exit, Press Ctrl-C")

            row = -1
            col = -1

            print("\n Current Score: {:.2f}%".format((score/(81 - noOfClues))*100))

            while row not in nolist or col not in nolist:
                try:
                    row = int(input("\n Enter the row number: ")) - 1
                    col = int(input("\n Enter the column number: ")) - 1
                    if row not in nolist or col not in nolist:
                        print("\n Enter valid row or column number")
                except ValueError:
                    row = -1
                    col = -1
                    continue

            if puzzle[row][col] != 0:
                os.system("clear")
                print("\n This one's already filled, try another one")
            else:
                while puzzle[row][col] < 1 or puzzle[row][col] > 9:
                    puzzle[row][col] = int(input("\n Enter the number into the grid: "))
                    if puzzle[row][col] < 1 or puzzle[row][col] > 9:
                        #os.system("clear")
                        print("\n Please enter a valid number")
                if puzzle[row][col] != sol[row][col]:
                    os.system('clear')
                    if streak != 0:
                        streak = 0
                    score -= 3
                    puzzle[row][col] = 0
                    pls.playsound('content/music/miss.mp3',block=False)
                    print("\n Not correct, try another one \n")
                    error_counter += 1
                    print("\n Mistakes: {}/3 \n".format(error_counter))
                else:
                    streak += 1
                    score += 1
                    os.system('clear')
                    pls.playsound('content/music/ding.mp3',block=False)
                    print("\n {} \n".format(sgg.random.choice(remarks)))

        printGrid(puzzle,original)
        if filledGrid(puzzle) == True:
            pls.playsound('content/music/success.mp3')
            print("\n Congratulations!! Puzzle solved!")
            print("\n Final Score: {:.2f}%".format((score/(81 - noOfClues))*100))
        else: #Meaning we failed the game
            pls.playsound('content/music/fail.mp3')
            print("\n Oh man, nice try!! Try again, we believe in you!")
            print("\n The solution to this puzzle")
            printGrid(sol)
    except KeyboardInterrupt:
        pls.playsound('content/music/fail.mp3')
        print("\n\n Oh, no problem bro, try again someday! \n")
        print("\n The solution to this puzzle \n")
        printGrid(sol)
            


