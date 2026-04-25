import pygame as pg
import time

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

SCREEN = pg.display.set_mode(WINDOW_SIZE)
CLOCK = pg.time.Clock()
NEXT_TICK_TIME = pg.time.get_ticks() + TICK_RATE
running = True

grid = [[0 for _ in range(GRID_SIZE[X])] for _ in range(GRID_SIZE[Y])]
player_pos = [GRID_SIZE[X]//2, GRID_SIZE[Y]//2]
dest_pos = player_pos
grid[player_pos[X]][player_pos[Y]] = 1

# Color mapping to remove nested IFs
color_map = {0: WHITE, 1: BLUE, 2: GREEN}

def get_rect(r, c):
    return [
        (MARGIN + CELL_SIZE) * c + MARGIN,
        (MARGIN + CELL_SIZE) * r + MARGIN,
        CELL_SIZE,
        CELL_SIZE
    ]

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        elif event.type == pg.MOUSEBUTTONDOWN:
            mouse_pos = pg.mouse.get_pos()

            col_coord = mouse_pos[X] // (CELL_SIZE + MARGIN)
            row_coord = mouse_pos[Y] // (CELL_SIZE + MARGIN)

            if not 0 <= row_coord < GRID_SIZE[Y] and 0 <= col_coord < GRID_SIZE[X]:
                continue

            if dest_pos == player_pos:
                grid[dest_pos[X]][dest_pos[Y]] = 1
            elif dest_pos:
                grid[dest_pos[X]][dest_pos[Y]] = 0
            dest_pos = [row_coord, col_coord]
            grid[row_coord][col_coord] = 2
    
    current_time = pg.time.get_ticks()
    if current_time > NEXT_TICK_TIME:
        time.sleep((current_time - NEXT_TICK_TIME) / 1000) # buffer until next tick
        if player_pos != dest_pos:

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

        NEXT_TICK_TIME = current_time + TICK_RATE


    SCREEN.fill(BLACK)
    for r in range(GRID_SIZE[Y]):
        for c in range(GRID_SIZE[X]):
            cell_type = grid[r][c]
            color = color_map.get(cell_type, WHITE)
            pg.draw.rect(SCREEN, color, get_rect(r, c))
    
    pg.display.flip()
    CLOCK.tick(FPS)

pg.quit()
