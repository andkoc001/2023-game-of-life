# Game of life 
# Andrzej Kocielski, 2023
# Based on code and tutorial by NeuralNine at https://youtu.be/cRWg2SWuXtM

################################

# Importing libraries
import time
import pygame
import numpy as np

### Setting constants

# Colours
COLOUR_BG = (20, 20, 20)
COLOUR_GRID = (70, 70, 70)
COLOUR_DIE_NEXT = (170, 0, 170)
COLOUR_ALIVE_NEXT = (255, 255, 0)

# Game settings
window_resolution_x = 400
window_resolution_y = 200
cell_size = 10
board_size_x = window_resolution_x // cell_size
board_size_y = window_resolution_y // cell_size

speed = time.sleep(0.2)

### Game logic

# Defining the update for each generation
def update(screen, cells, size, with_progress=False):
    '''
    This function updates the state of game for new generation.
    '''    
    
    # Generate empty board 
    updated_cells = np.zeros((cells.shape[0], cells.shape[1]))
    
    #check the conditions for keeping the cells alive, i.e. surrounding cells
    for row, col in np.ndindex(cells.shape):
        # sum up alive neighbouring cells, excluding own cell
        alive_neighbours = np.sum(cells[row-1:row+2, col-1:col+2]) - cells[row, col]
        colour = COLOUR_BG if cells[row, col] == 0 else COLOUR_ALIVE_NEXT
            
            
        if cells[row, col] == 1:
            if alive_neighbours < 2 or alive_neighbours > 3:
                if with_progress:
                    colour = COLOUR_DIE_NEXT
            elif 2 <= alive_neighbours <= 3:
                updated_cells[row, col] = 1
                if with_progress:
                    colour = COLOUR_ALIVE_NEXT
        else:
            if alive_neighbours == 3:
                updated_cells[row, col] = 1
                if with_progress:
                    colour = COLOUR_ALIVE_NEXT
                    
        # # consider given cell is alive
        # if cells[row, col] == 1:
        #     if alive_neighbours == 2 or alive_neighbours == 3:
        #         updated_cells[row, col] = 1
        #         if with_progress:
        #             colour = COLOUR_ALIVE_NEXT
        #     else:
        #         if with_progress:
        #             colour == COLOUR_DIE_NEXT
        
        # else: # given cell is dead
        #     if alive_neighbours == 3:
        #         updated_cells[row, col] = 1
        #         if with_progress:
        #             colour = COLOUR_ALIVE_NEXT
        
        pygame.draw.rect(screen, colour, (col * size, row * size, size - 1, size - 1))
    
    return updated_cells

# Defining the main function of the program
def main():
    '''
    This is the main function of the program.
    '''
    
    pygame.init()
    pygame.display.set_caption("Conway's game of life")
    screen = pygame.display.set_mode((window_resolution_x, window_resolution_y))
        
    # genrate empty board - note the order!
    cells = np.zeros((board_size_y, board_size_x))
    screen.fill(COLOUR_GRID)
    update(screen, cells, cell_size)
    
    pygame.display.flip()
    pygame.display.update()
    
    running = False
    
    # Game loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            
            # pause the game with SPACE kay
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    running = not running
                    update(screen, cells, cell_size)
                    pygame.display.update()
                    
            # Set alive cell with mouse click
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                cells[pos[1] // cell_size, pos[0] // cell_size] = 1
                update(screen, cells, cell_size)
                pygame.display.update()
                
        screen.fill(COLOUR_GRID)
        
        if running:
            cells = update(screen, cells, cell_size, with_progress=True)
            pygame.display.update()
            
        # time.sleep(.01)
        speed

# Dependencies check
if __name__ == '__main__':
    main()