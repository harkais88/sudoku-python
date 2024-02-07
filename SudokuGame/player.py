#Main Player Code
#Note: Right now, it only shows up with 1 game. Should add a main menu, check button, reset button, mistake counter,
#timer, pause option, and some music maybe, along with a bit of art for the game

#!/usr/bin/python3

import pygame
import RSudoku
import sys
import numpy as np
from time import sleep # Using it for now, used only in testing
from copy import deepcopy

class Game:
    def __init__(self,diff):
        pygame.init()
        self.width = 600 # Width of our screen
        self.background_fill = (242,242,242) # Background Fill
        self.screen = pygame.display.set_mode((self.width,self.width))
        pygame.display.set_caption("Pydoku")
        self.screen.fill(self.background_fill) 
        self.running = True 
        self.clock = pygame.time.Clock()
        self.start = False
        self.start_flag = 0
        self.game = RSudoku.sudoku(diff) # Intializing game variable, has the grid and puzzle as attributes
        self.p = 493 / 9 #Obtained by Trial and Error
        self.i = self.j = 10 #Used for validating mouse pos and entering values
        self.value = "0" #Used for intialising entry value
        self.flag = 0 # Used for checking selected cell coloring
        self.solution = deepcopy(self.game.puzzle) #Used for end game check

    def run(self):
        """Responsible for running the game"""
        while self.running == True:
            self.handle_event()
            self.draw()
            # Win Event
            if np.all(np.equal(self.solution,self.game.grid)):
                print("Game Solved!!!")
                win = self.screen.blit(pygame.font.SysFont("Comic Sans MS", 30).render("YOU WON THE GAME!!!", 
                                        True, (0, 255, 0)), (15,self.width - self.p + 10))
                pygame.display.update(win) 
                # For Testing purpose, remove later
                sleep(2)
                self.running = False
            self.clock.tick(60)
        self.quit()

    def handle_event(self):
        """Responsible for handling all valid events"""
        for event in pygame.event.get():
                # Quit Event
                if event.type == pygame.QUIT:
                    self.running = False
                # Getting Mouse Position Data
                if event.type == pygame.MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()
                    # Following occurs only in main_menu
                    if self.start == False:
                        # If Quit Button is pressed
                        if self.width // 2 - self.p < pos[0] < self.width // 2 + self.p and \
                            self.width // 2 + self.p < pos[1] < self.width // 2 + 2*self.p:
                            self.quit()
                        # If START Button is pressed
                        if self.width // 2 - self.p < pos[0] < self.width // 2 + self.p and \
                                self.width //2 - self.p < pos[1] < self.width // 2 :
                            self.start = True
                            self.start_flag = 1
                    # Checks whether mouse click was within grid
                    if (self.p < pos[0] < self.width - self.p) and (self.p < pos[1] < self.width - self.p):
                        self.i,self.j = int(pos[1]//self.p), int(pos[0]//self.p)                      
                    try:
                        # Checks whether selected cell is a part of original puzzle or not
                        if self.game.puzzle[self.i-1][self.j-1] != 0:
                            self.flag = 0
                            self.i,self.j = 10,10
                        else:
                            self.flag = 1
                    except IndexError:
                        pass
                # Taking Input From Keyboard
                if event.type == pygame.KEYDOWN and (self.i != 10 and self.j != 10):
                    self.value = "0"
                    if event.key == pygame.K_1:
                        self.value = "1"
                    if event.key == pygame.K_2:
                        self.value = "2"
                    if event.key == pygame.K_3:
                        self.value = "3"
                    if event.key == pygame.K_4:
                        self.value = "4"
                    if event.key == pygame.K_5:
                        self.value = "5"
                    if event.key == pygame.K_6:
                        self.value = "6"
                    if event.key == pygame.K_7:
                        self.value = "7"
                    if event.key == pygame.K_8:
                        self.value = "8"
                    if event.key == pygame.K_9:
                        self.value = "9"                

    def draw(self):
        """Responsible for drawing at every frame"""
        if self.start == False:
            # Main Menu
            main_font = pygame.font.SysFont("Comic Sans MS",30)
            main_title_font = pygame.font.Font(".\content\Fonts\Copperplate.ttf", 100)

            # Main Title
            main_title = main_title_font.render("PYDOKU",True,(52, 235, 177))
            self.screen.blit(main_title, (self.p+(0.5*self.p),self.p))

            # Start Button Operations
            start_text = main_font.render("START",True,(255,0,0))
            pygame.draw.rect(self.screen, (0,0,0), 
                             (self.width // 2 - self.p, self.width // 2 - self.p, 2*self.p, self.p),2)
            self.screen.blit(start_text, (self.width // 2 - self.p + 2, self.width // 2 - self.p + 2))

            # Quit Button Operations
            quit_text = main_font.render("QUIT",True,(255,0,0))
            pygame.draw.rect(self.screen, (0,0,0), 
                             (self.width // 2 - self.p, self.width // 2 + self.p, 2*self.p, self.p),2)
            self.screen.blit(quit_text, (self.width // 2 - self.p + 10, self.width // 2 + self.p + 2))
            pygame.display.update()
        else:
            if self.start_flag == 1:
                # If Start Button is pressed, we remove the Main Screen Buttons
                # The flag is given so that this does not happen for every frame
                rmv_title = pygame.draw.rect(self.screen, self.background_fill,
                            (0,0,self.width,self.width//2))
                rmv_start = pygame.draw.rect(self.screen, self.background_fill, 
                            (self.width // 2 - self.p, self.width // 2 - self.p, 2*self.p, self.p))
                rmv_quit = pygame.draw.rect(self.screen, self.background_fill,
                            (self.width // 2 - self.p, self.width // 2 + self.p, 2*self.p, self.p))
                pygame.display.update([rmv_start,rmv_quit,rmv_title])
                self.start_flag = 0
            # Drawing the lines
            for i in range(10):
                if i % 3 == 0: line_width = 4;
                else: line_width = 2;
                # Vertical Line
                pygame.draw.line(self.screen, (0,0,0), 
                                (self.p + (self.p*i), self.p), (self.p + (self.p * i),self.width - self.p), 
                                width = line_width)
                # Horizontal Line
                pygame.draw.line(self.screen, (0,0,0), 
                                (self.p, self.p + (self.p * i)), (self.width - self.p,self.p + (self.p * i)), 
                                width = line_width)

            # Updating Screen
            pygame.display.update()

            # Setting Font Style And Colors
            num_font = pygame.font.SysFont("Comic Sans MS",30) # Setting Font of the Numbers
            sel_color = (177,232,237)
            num_color = (56,123,232)
            sol_color = (19,214,120)
            err_color = (247,27,20)

            # Instruction
            inst = num_font.render("Select, Then Enter Number", True, (9,23,46))
            self.screen.blit(inst,(15,5))

            # Coloring Selected Cell
            if self.flag == 1:
                # The worst way to clear a already selected cell :(
                # Could probably fix this if the previous selected cell coords are recorded, will do this later
                for i in range(int(self.p), int(self.width - self.p)):
                    for j in range(int(self.p), int(self.width - self.p)):
                        if self.screen.get_at((i,j)) == sel_color:
                            self.screen.set_at((i,j),self.background_fill)
                # Providing Selection Color to Selected Cell
                selector = pygame.Surface((self.p,self.p))
                selector.fill(sel_color)
                self.screen.blit(selector, (self.j*self.p, self.i*self.p))
                if self.solution[self.i-1][self.j-1] != 0:
                    selected_cell_val = num_font.render(str(self.solution[self.i-1][self.j-1]),True,num_color)
                    self.screen.blit(selected_cell_val,((self.j)*self.p + 20, (self.i)*self.p + 5))
                self.flag = 0

            # Rendering the puzzle
            for i in range(9):
                for j in range(9):
                    if self.game.puzzle[i][j] != 0:
                        puzzle_num = num_font.render(str(self.game.puzzle[i][j]), True, num_color)
                        self.screen.blit(puzzle_num, ((j+1)*self.p + 20, (i+1)*self.p + 5)) #Values found from T&E

            if self.value != "0":
                # Inputting the value into our solution for checking with our grid 
                self.solution[self.i-1][self.j-1] = int(self.value)
                
                # Any value in the selected cell will be removed
                whitener = pygame.Surface((self.p, self.p))
                whitener.fill(self.background_fill)
                whitener_rect = self.screen.blit(whitener, (self.j * self.p, self.i * self.p))
                pygame.display.update(whitener_rect)

                # Checking our input ... I should probably change this to where I cant do this,
                # then give a check button, which would then show which ones are wrong
                if self.game.grid[self.i-1][self.j-1] != int(self.value):
                    value = num_font.render(self.value, True, err_color)
                else:
                    value = num_font.render(self.value, True, sol_color)
                self.screen.blit(value, (self.j * self.p + 20, self.i * self.p + 5))
                self.value = "0"
    
    def quit(self):
        """Quits the Game"""
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    # For now, it only works with a sudoku grid with 35-46 clues present
    # After Main Menu Implementation, should give the player the option to choose other difficulities
    game = Game(1)
    game.run()
    