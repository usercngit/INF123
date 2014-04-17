'''
Edits on Apr 13, 2014

@editor: Chris
'''

"""
Style: main and subroutines
Components: main program and subroutines
Connectors: procedure calls
Constraints: components can't communicate using shared memory (e.g. global 
variables) 
Gains: change the implementation of a subroutine without affecting the main 
program.  
"""

from random import randint

import pygame
from pygame.locals import KEYDOWN, QUIT, K_ESCAPE, K_w, K_a, K_s, K_d, K_SPACE


############################################################

def process_input(prev_direction, paused_status):
    game_status, direction, paused = 1, prev_direction, paused_status
    for event in pygame.event.get():
        if event.type == QUIT:
            game_status = 0 # 0 for game over, 1 for play
        if event.type == KEYDOWN:
            key = event.key
            if key == K_ESCAPE:
                game_status = 0
            if paused_status != 1:
                if key == K_w:
                    direction = (0, -1)
                elif key == K_s:
                    direction = (0, 1)
                elif key == K_a:
                    direction = (-1, 0)
                elif key == K_d:
                    direction = (1, 0)
            if key == K_SPACE: # 0 for not paused, 1 for paused
                if paused_status == 1:
                    paused = 0
                elif paused_status != 1:
                    paused = 1
                
    return paused, game_status, direction

############################################################

def draw_everything(screen, mybox, pellets, borders):
    screen.fill((0, 59, 103))  # Ocean blue
    [pygame.draw.rect(screen, (255, 150, 100), b) for b in borders]  # Bright Orange
    [pygame.draw.rect(screen, (50, 150, 50), p) for p in pellets]  # Forest Green
    pygame.draw.rect(screen, (200, 100, 50), mybox)  # Dark orange
    pygame.display.update()

############################################################

def create_box(dims):
    w, h = dims
    box = pygame.Rect(w / 2, h / 2, 10, 10)  # start in middle of the screen
    direction = 0, 1  # start direction: down
    return box, direction

############################################################

def collide(box, boxes):
    # return True if box collides with any entity in boxes
    return box.collidelist(boxes) != -1
    
############################################################

def move(box, direction): 
    return box.move(direction[0]*2, direction[1]*2) 

############################################################

def create_borders(dims, thickness=2):
    w, h = dims
    return [pygame.Rect(0, 0, thickness, h),
            pygame.Rect(0, 0, w, thickness),
            pygame.Rect(w - thickness, 0, thickness, h),
            pygame.Rect(0, h - thickness, w, thickness),
            pygame.Rect(w/3, h/2, thickness, h/3),
            pygame.Rect(h/4, h/4, h/3, thickness)]
    
############################################################

def create_pellet(dims, offset):
    w, h = dims
    return pygame.Rect(randint(offset, w - offset),
                       randint(offset, h - offset), 5, 5)

def create_pellets(dims, qty, offset=10): 
    # this is the only subroutine independent of Pygame
    return [create_pellet(dims, offset) for _ in range(qty)]
    
def eat_and_replace_colliding_pellet(box, pellets, dims, offset=10):
    p_index = box.collidelist(pellets)
    if p_index != -1:  # ate a pellet: grow, and replace a pellet
        pellets[p_index] = create_pellet(dims, offset)
        box.size = box.width * 1.2, box.height * 1.2
    return box, pellets
    
############################################################

pygame.init()
clock = pygame.time.Clock()

# display
dims = 400, 300
screen = pygame.display.set_mode(dims)

# game objects
borders = create_borders(dims)
pellets = create_pellets(dims, 4)
mybox, direction = create_box(dims)

# game loop
game_status = 1  # 0 for game over, 1 for play
paused = 0 # 0 for not paused, 1 for paused
while game_status:

    paused, game_status, direction = process_input(direction, paused)
    
    if paused != 1:
        mybox = move(mybox, direction)
        if collide(mybox, borders):
            mybox, direction = create_box(dims)
        mybox, pellets = eat_and_replace_colliding_pellet(mybox, pellets, dims)
    
        draw_everything(screen, mybox, pellets, borders)
    
    clock.tick(50)  # or sleep(.02) to have the loop Pygame-independent