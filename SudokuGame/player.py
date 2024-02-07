#Main Player Code
#Note: Right now, it only shows up with 1 game. Should add a main menu, check button, reset button, mistake counter,
#timer, pause option, and some music maybe, along with a bit of art for the game
#Should add a loading screen

#!/usr/bin/python3

import pygame
import RSudoku
import sys
import numpy as np
from time import sleep # Using it for now, used only in testing
from copy import deepcopy

class Game:
    def __init__(self):
        pygame.init()
        self.width = 600 # Width of our screen
        self.background_fill = (242,242,242) # Background Fill
        self.background_fill_alt = (55, 59, 64) # Alternate Background Fill for Difficulity Menu
        self.screen = pygame.display.set_mode((self.width,self.width))
        pygame.display.set_caption("Pydoku")
        self.screen.fill(self.background_fill) 
        self.running = True 
        self.clock = pygame.time.Clock()
        self.start = False #At start, this will generate the main menu, after selecting option, we go to diff menu
        self.main_flag = 0 #For checking whether to not render main menu
        self.game = RSudoku.sudoku(0) #Initializing game variable
        self.diff_flag = 0 #For checking whether to render the difficulity menu
        self.sel_diff = 0 #For the difficulity choice option
        self.p = 493 / 9 #Obtained by Trial and Error
        self.i = self.j = 10 #Used for validating mouse pos and entering values
        self.value = "0" #Used for intialising entry value
        self.sel_flag = 0 # Used for checking selected cell coloring
        self.sel_i = self.sel_j = 10 # Used for storing previous selected cell
        self.solution = np.empty([9,9]) # Initializing an empty array that will be used for endgame

    def run(self):
        """Responsible for running the game"""
        while self.running == True:
            self.handle_event()
            self.draw()
            # Win Event
            if np.all(np.equal(self.solution,self.game.grid)):
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
                    if self.start == False and self.width // 2 - self.p < pos[0] < self.width // 2 + self.p:
                        # If Quit Button is pressed
                        if self.width // 2 + self.p < pos[1] < self.width // 2 + 2*self.p:
                            self.quit()
                        # If START Button is pressed
                        if self.width //2 - self.p < pos[1] < self.width // 2 :
                            self.start = True
                            self.main_flag = 1
                    if self.diff_flag == 1 and 2*self.p < pos[0] < 2*self.p + self.width - 4*self.p:
                        # When we enter the difficulity menu
                        # If Easy Button is pressed
                        if 2*self.p < pos[1] < 2*self.p + self.p:
                            self.sel_diff = 1
                            self.diff_flag = 0
                        elif 4*self.p < pos[1] < 4*self.p + self.p:
                            self.sel_diff = 2
                            self.diff_flag = 0
                        elif 6*self.p < pos[1] < 6*self.p + self.p:
                            self.sel_diff = 3
                            self.diff_flag = 0
                        elif 8*self.p < pos[1] < 8*self.p + self.p:
                            self.sel_diff = 4
                            self.diff_flag = 0

                    # Checks whether mouse click was within grid
                    if (self.p < pos[0] < self.width - self.p) and (self.p < pos[1] < self.width - self.p):
                        self.i,self.j = int(pos[1]//self.p), int(pos[0]//self.p)                      
                    try:
                        # Checks whether selected cell is a part of original puzzle or not
                        if self.game.puzzle[self.i-1][self.j-1] != 0:
                            self.sel_flag = 0
                            self.i,self.j = 10,10
                        else:
                            self.sel_flag = 1
                    except (IndexError, AttributeError):
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
            if self.main_flag == 1:
                # If Start Button is pressed, we remove the Main Screen Buttons
                # The flag is given so that this does not happen for every frame
                rmv_title = pygame.draw.rect(self.screen, self.background_fill,
                            (0,0,self.width,self.width//2))
                rmv_start = pygame.draw.rect(self.screen, self.background_fill, 
                            (self.width // 2 - self.p, self.width // 2 - self.p, 2*self.p, self.p))
                rmv_quit = pygame.draw.rect(self.screen, self.background_fill,
                            (self.width // 2 - self.p, self.width // 2 + self.p, 2*self.p, self.p))
                pygame.display.update([rmv_start,rmv_quit,rmv_title])
                self.main_flag = 0
                self.diff_flag = 1
            if self.diff_flag == 1:
                self.screen.fill(self.background_fill_alt)
                diff_font = pygame.font.Font(".\content\Fonts\Copperplate.ttf",40)
                diff_text_color = (168, 50, 78)

                # Diff Choice Container
                diff_main_rect = pygame.draw.rect(self.screen, self.background_fill,
                                (self.p-10,self.p-10,self.width - (2*(self.p - 10)),self.width - (2*(self.p - 10))))
                
                # Easy Diff Button
                easy_diff_button = pygame.draw.rect(self.screen, self.background_fill_alt,
                                (2*self.p,2*self.p,self.width - 4*self.p,self.p),width=2)
                easy_text = diff_font.render("EASY",True,diff_text_color)
                self.screen.blit(easy_text,(self.width//2 - self.p,2*self.p+10))

                # Medium Diff Button
                med_diff_button = pygame.draw.rect(self.screen, self.background_fill_alt,
                                (2*self.p,4*self.p,self.width - 4*self.p,self.p),width=2)
                med_text = diff_font.render("MEDIUM",True,diff_text_color)
                self.screen.blit(med_text,(self.width//2 - ((3*self.p)//2)-6,4*self.p+10))

                # Hard Diff Button
                hard_diff_button = pygame.draw.rect(self.screen, self.background_fill_alt,
                                (2*self.p,6*self.p,self.width - 4*self.p,self.p),width=2)
                hard_text = diff_font.render("HARD",True,diff_text_color)
                self.screen.blit(hard_text,(self.width//2 - self.p,6*self.p+10))

                # Impossible Diff Button
                imp_diff_button = pygame.draw.rect(self.screen, self.background_fill_alt,
                                (2*self.p,8*self.p,self.width - 4*self.p,self.p),width=2)
                imp_text = diff_font.render("IMPOSSIBLE",True,diff_text_color)
                self.screen.blit(imp_text,(self.width//2 - 2*self.p - 15,8*self.p+10))

                pygame.display.update()
            
            if self.sel_diff != 0:
                self.game = RSudoku.sudoku(self.sel_diff) # Intializing game variable, has the grid and puzzle as attributes
                self.solution = deepcopy(self.game.puzzle) #Used for end game check
            
            if self.diff_flag == 0:
                if self.sel_diff != 0:
                    self.screen.fill(self.background_fill)
                    pygame.display.update()
                    self.sel_diff = 0
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
                inst = num_font.render("Select Cell, Enter Number", True, (9,23,46))
                self.screen.blit(inst,(15,5))

                # Coloring Selected Cell
                if self.sel_flag == 1:
                    # Using the stored previous selection coordinates 
                    if self.sel_i != 10 and self.sel_j != 10: # This is needed for the first selection cell
                        rmv_sel_cell = pygame.draw.rect(self.screen, self.background_fill,
                                                        (self.sel_j*self.p,self.sel_i*self.p,self.p,self.p))
                        pygame.display.update(rmv_sel_cell)
                        if self.solution[self.sel_i-1][self.sel_j-1] != 0:
                            prev_sel_cell_val = num_font.render(str(self.solution[self.sel_i-1][self.sel_j-1]),
                                                                True,num_color)
                            self.screen.blit(prev_sel_cell_val,(self.sel_j*self.p+20,self.sel_i*self.p+5))
                    # Providing Selection Color to Selected Cell
                    selector = pygame.Surface((self.p,self.p))
                    selector.fill(sel_color)
                    self.screen.blit(selector, (self.j*self.p, self.i*self.p))
                    if self.solution[self.i-1][self.j-1] != 0:
                        selected_cell_val = num_font.render(str(self.solution[self.i-1][self.j-1]),True,num_color)
                        self.screen.blit(selected_cell_val,(self.j*self.p + 20, self.i*self.p + 5))
                    self.sel_i,self.sel_j = self.i, self.j
                    self.sel_flag = 0

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
    Game().run()
    