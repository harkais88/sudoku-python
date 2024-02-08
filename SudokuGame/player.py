#Main Player Code
#Note: Right now, it only shows up with 1 game. Should add a check button, mistake counter,
#timer, pause option, and some music maybe, along with a bit of art for the game
#Should add a loading screen, and animation for a lose or win event to get rid of missing value bug

#!/usr/bin/python3

import pygame
import RSudoku
import sys
import numpy as np
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
        # To avoid the chance that empty solution is equal to empty grid
        while np.all(np.equal(self.solution,self.game.grid)): self.solution = np.empty([9,9]);
        self.error_count = 0 #Used for recording number of errors, after 5 times game will end
        self.frame_count = 0 #Used for timer

    def run(self):
        """Responsible for running the game"""
        while self.running == True:
            self.handle_event()
            self.draw()  
            self.clock.tick(60)
        self.quit()

    def handle_event(self):
        """Responsible for handling all valid events"""
            
        # After Lose or Win Event, I should give option to quit or new game or reset the game if lost
        # Lose Event
        if self.error_count == 5:
            lose_txt = "YOU LOST THE GAME\nPress R to Reset\nPress N for a New Game\nPress Q to Quit".split("\n")
            # Lose Screen Made from T&E
            self.screen.fill(self.background_fill)
            self.screen.blit(pygame.font.Font(".\content\Fonts\Copperplate.ttf", 40).render(lose_txt[0],
                        True, (232, 50, 50)), (self.width//2-self.p-170,self.width//2-self.p))
            self.screen.blit(pygame.font.Font(".\content\Fonts\Copperplate.ttf",30).render(lose_txt[1],
                        True, (232, 50, 50)), (self.width//2 - self.p-80,self.width//2))
            self.screen.blit(pygame.font.Font(".\content\Fonts\Copperplate.ttf",30).render(lose_txt[2],
                        True, (232, 50, 50)), (self.width//2 - self.p-127,self.width//2 + self.p))
            self.screen.blit(pygame.font.Font(".\content\Fonts\Copperplate.ttf",30).render(lose_txt[3],
                        True, (232, 50, 50)), (self.width//2 - self.p-80,self.width//2 + (2*self.p)))                                           
            pygame.display.update()

        # Win Event
        if np.all(np.equal(self.solution,self.game.grid)):
            win_txt = "YOU WON THE GAME!!!\nPress R to Restart\nPress N for a New Game\nPress Q to Quit".split("\n")
            self.screen.fill(self.background_fill)
            self.screen.blit(pygame.font.SysFont("Comic Sans MS", 30).render(win_txt[0], 
                        True, (0, 255, 0)), (self.width//4,self.width//2-self.p))
            self.screen.blit(pygame.font.Font(".\content\Fonts\Copperplate.ttf",30).render(win_txt[1],
                        True, (232, 50, 50)), (self.width//2 - self.p-80,self.width//2))
            self.screen.blit(pygame.font.Font(".\content\Fonts\Copperplate.ttf",30).render(win_txt[2],
                        True, (232, 50, 50)), (self.width//2 - self.p-127,self.width//2 + self.p))
            self.screen.blit(pygame.font.Font(".\content\Fonts\Copperplate.ttf",30).render(win_txt[3],
                        True, (232, 50, 50)), (self.width//2 - self.p-80,self.width//2 + (2*self.p))) 
            pygame.display.update()       
            
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
                        # If Medium Button is pressed
                        elif 4*self.p < pos[1] < 4*self.p + self.p:
                            self.sel_diff = 2
                            self.diff_flag = 0
                        # If Hard Button is pressed
                        elif 6*self.p < pos[1] < 6*self.p + self.p:
                            self.sel_diff = 3
                            self.diff_flag = 0
                        # If Impossible Button is pressed
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
                if event.type == pygame.KEYDOWN and (self.i != 10 and self.j != 10) \
                    and self.diff_flag == 0 and self.main_flag == 0:
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
                    if event.key == pygame.K_r: #Reset Event
                        self.solution = deepcopy(self.game.puzzle)
                        if self.error_count == 5: self.error_count = 0;
                        self.screen.fill(self.background_fill)
                        self.frame_count = 0
                        pygame.display.update()
                    if event.key == pygame.K_n: #New Game Event
                        if self.error_count == 5: self.error_count = 0;
                        self.game = RSudoku.sudoku(0)
                        self.diff_flag = 1
                        self.screen.fill(self.background_fill)
                        self.frame_count = 0
                        pygame.display.update()
                    if event.key == pygame.K_q: #Quit Event
                        self.quit()

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
                pygame.draw.rect(self.screen, self.background_fill,
                                (self.p-10,self.p-10,self.width - (2*(self.p - 10)),self.width - (2*(self.p - 10))))
                
                # Easy Diff Button
                pygame.draw.rect(self.screen, self.background_fill_alt,
                                (2*self.p,2*self.p,self.width - 4*self.p,self.p),width=2)
                easy_text = diff_font.render("EASY",True,diff_text_color)
                self.screen.blit(easy_text,(self.width//2 - self.p,2*self.p+10))

                # Medium Diff Button
                pygame.draw.rect(self.screen, self.background_fill_alt,
                                (2*self.p,4*self.p,self.width - 4*self.p,self.p),width=2)
                med_text = diff_font.render("MEDIUM",True,diff_text_color)
                self.screen.blit(med_text,(self.width//2 - ((3*self.p)//2)-6,4*self.p+10))

                # Hard Diff Button
                pygame.draw.rect(self.screen, self.background_fill_alt,
                                (2*self.p,6*self.p,self.width - 4*self.p,self.p),width=2)
                hard_text = diff_font.render("HARD",True,diff_text_color)
                self.screen.blit(hard_text,(self.width//2 - self.p,6*self.p+10))

                # Impossible Diff Button
                pygame.draw.rect(self.screen, self.background_fill_alt,
                                (2*self.p,8*self.p,self.width - 4*self.p,self.p),width=2)
                imp_text = diff_font.render("IMPOSSIBLE",True,diff_text_color)
                self.screen.blit(imp_text,(self.width//2 - 2*self.p - 15,8*self.p+10))

                pygame.display.update()
            
            if self.sel_diff != 0:
                # Intializing game variable, has the grid and puzzle as attributes
                pygame.draw.rect(self.screen, self.background_fill,
                                (self.p-10,self.p-10,self.width - (2*(self.p - 10)),self.width - (2*(self.p - 10))))
                self.screen.blit(pygame.font.SysFont("Comic Sans Ms",25).render("LOADING GAME",True,(0,0,0)),
                                 (self.width//2 - self.p - 30,self.width//2 - (self.p//2)))
                pygame.display.update()
                self.game = RSudoku.sudoku(self.sel_diff)
                self.solution = deepcopy(self.game.puzzle) #Used for end game check

            if self.diff_flag == 0 and self.error_count != 5 and not np.all(np.equal(self.solution,self.game.grid)):
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
                sel_num_color = (56,123,232)
                ori_num_color = (9,23,46)
                # Following colors will be used when check button is given
                sol_num_color = (19,214,120)
                err_color = (247,27,20)

                # Instruction
                inst = num_font.render("Select Cell, Enter Number", True, ori_num_color)
                self.screen.blit(inst,(15,5))

                # Timer
                time = num_font.render(f"Time: {(self.frame_count//60)//60}:{(self.frame_count//60)%60}",
                                       True, ori_num_color)
                self.frame_count += 1
                time_blank = pygame.draw.rect(self.screen,self.background_fill,(self.width-(3*self.p),0,3*self.p,self.p-3))
                pygame.display.update(time_blank)
                time_display = self.screen.blit(time,(self.width-(3*self.p),5))
                pygame.display.update(time_display)

                # Coloring Selected Cell
                if self.sel_flag == 1:
                    # Using the stored previous selection coordinates 
                    if self.sel_i != 10 and self.sel_j != 10: # This is needed for the first selection cell
                        rmv_sel_cell = pygame.draw.rect(self.screen, self.background_fill,
                                                        (self.sel_j*self.p,self.sel_i*self.p,self.p,self.p))
                        pygame.display.update(rmv_sel_cell)
                        if self.solution[self.sel_i-1][self.sel_j-1] != 0:
                            if self.solution[self.sel_i-1][self.sel_j-1] != self.game.grid[self.sel_i-1][self.sel_j-1]:
                                prev_sel_cell_val = num_font.render(str(self.solution[self.sel_i-1][self.sel_j-1]),
                                                                    True,err_color)
                            else:
                                prev_sel_cell_val = num_font.render(str(self.solution[self.sel_i-1][self.sel_j-1]),
                                                                    True,sol_num_color)
                            self.screen.blit(prev_sel_cell_val,(self.sel_j*self.p+20,self.sel_i*self.p+5))
                    # Providing Selection Color to Selected Cell
                    selector = pygame.Surface((self.p,self.p))
                    selector.fill(sel_color)
                    self.screen.blit(selector, (self.j*self.p, self.i*self.p))
                    if self.solution[self.i-1][self.j-1] != 0:
                        selected_cell_val = num_font.render(str(self.solution[self.i-1][self.j-1]),
                                                            True,sel_num_color)
                        self.screen.blit(selected_cell_val,(self.j*self.p + 20, self.i*self.p + 5))
                    self.sel_i,self.sel_j = self.i, self.j
                    self.sel_flag = 0

                # Rendering the puzzle
                for i in range(9):
                    for j in range(9):
                        if self.game.puzzle[i][j] != 0:
                            puzzle_num = num_font.render(str(self.game.puzzle[i][j]), True, ori_num_color)
                            #Values 20 and 5 found from T&E
                            self.screen.blit(puzzle_num, ((j+1)*self.p + 20, (i+1)*self.p + 5)) 

                if self.value != "0":                    
                    # Any value in the selected cell will be removed
                    whitener = pygame.Surface((self.p, self.p))
                    whitener.fill(self.background_fill)
                    whitener_rect = self.screen.blit(whitener, (self.j * self.p, self.i * self.p))
                    pygame.display.update(whitener_rect)

                    if self.game.grid[self.i-1][self.j-1] != int(self.value):
                        value = num_font.render(self.value,True,err_color)
                        self.error_count += 1
                    else:
                        value = num_font.render(self.value, True, sol_num_color)
                    self.screen.blit(value, (self.j * self.p + 20, self.i * self.p + 5))
                    # Inputting the value into our solution for checking with our grid 
                    self.solution[self.i-1][self.j-1] = int(self.value)
                    self.value = "0"

    def quit(self):
        """Quits the Game"""
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    Game().run()
    