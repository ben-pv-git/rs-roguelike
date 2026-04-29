import pygame as pg
import time
from collections import deque

pg.init()

FPS = 60
TICK_RATE = 600
GRID_SIZE = (32, 18)
X = 0
Y = 1
CELL_SIZE = 40
MARGIN = 1
WINDOW_SIZE = (GRID_SIZE[X] * (CELL_SIZE + MARGIN) + MARGIN, GRID_SIZE[Y] * (CELL_SIZE + MARGIN) + MARGIN)
BLACK = (0, 0, 0)
WHITE = (200, 200, 200)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
COLOR_MAP = {0: WHITE, 1: BLUE, 2: GREEN, 3: RED}

SCREEN = pg.display.set_mode(WINDOW_SIZE)
CLOCK = pg.time.Clock()
NEXT_TICK_TIME = pg.time.get_ticks() + TICK_RATE
RUNNING = True

grid = [[0 for _ in range(GRID_SIZE[X])] for _ in range(GRID_SIZE[Y])]

player_pos = [GRID_SIZE[X]//2, GRID_SIZE[Y]//2]
grid[player_pos[X]][player_pos[Y]] = 1
dest_pos = player_pos
player_is_attacking = False
player_is_moving = player_pos != dest_pos
action_queue = deque()

enemy_pos = [10, 10]
grid[enemy_pos[X]][enemy_pos[Y]] = 3

def get_rect(r, c):
    return [
        (MARGIN + CELL_SIZE) * c + MARGIN,
        (MARGIN + CELL_SIZE) * r + MARGIN,
        CELL_SIZE,
        CELL_SIZE
    ]

def move_player():

    grid[player_pos[X]][player_pos[Y]] = 0 # tile is no longer occupied by the player

    move_speed = 2
    if abs(player_pos[Y] - dest_pos[Y]) == 1: move_speed = 1

    if player_pos[Y] < dest_pos[Y]: player_pos[Y] += move_speed
    elif player_pos[Y] > dest_pos[Y]: player_pos[Y] -= move_speed

    move_speed = 2
    if abs(player_pos[X] - dest_pos[X]) == 1: move_speed = 1

    if player_pos[X] < dest_pos[X]: player_pos[X] += move_speed
    elif player_pos[X] > dest_pos[X]: player_pos[X] -= move_speed
    
    grid[player_pos[X]][player_pos[Y]] = 1

def attack():
    print("attack")

while RUNNING:

    for event in pg.event.get():

        if event.type == pg.QUIT:
            RUNNING = False

        elif event.type == pg.MOUSEBUTTONDOWN:
            mouse_pos = pg.mouse.get_pos()
            col_coord = mouse_pos[X] // (CELL_SIZE + MARGIN)
            row_coord = mouse_pos[Y] // (CELL_SIZE + MARGIN)

            if not 0 <= row_coord < GRID_SIZE[Y] and 0 <= col_coord < GRID_SIZE[X]:
                continue

            if player_pos == [row_coord, col_coord]:
                continue

            if [col_coord, row_coord] == enemy_pos:
                if player_pos != dest_pos:
                    grid[dest_pos[X]][dest_pos[Y]] = 0
                action_queue.append("attack")
                player_is_attacking = True
                player_is_moving = False
                continue

            if dest_pos != [row_coord, col_coord] and dest_pos != player_pos:
                grid[dest_pos[X]][dest_pos[Y]] = 0

            dest_pos = [row_coord, col_coord]
            grid[dest_pos[X]][dest_pos[Y]] = 2
            action_queue.append("move_player")
    

    current_time = pg.time.get_ticks()
    if current_time > NEXT_TICK_TIME:
        time.sleep((current_time - NEXT_TICK_TIME) / 1000) # buffer until next tick

        if action_queue:
            action = action_queue.popleft()

            if action == "move_player":
                player_is_moving = True

            if action == "attack" and player_is_attacking:

                player_is_moving = False
                attack()
                player_is_attacking = False
        
        if player_is_moving:
            move_player()
                

        NEXT_TICK_TIME = current_time + TICK_RATE


    SCREEN.fill(BLACK)
    for r in range(GRID_SIZE[Y]):
        for c in range(GRID_SIZE[X]):
            cell_type = grid[r][c]
            color = COLOR_MAP.get(cell_type, WHITE)
            pg.draw.rect(SCREEN, color, get_rect(r, c))
    
    pg.display.flip()
    CLOCK.tick(FPS)

pg.quit()
