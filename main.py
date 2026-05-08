import pygame as pg
from collections import deque
from pathfinder import Pathfinder
from entity import *

pg.init()

Y = 0
X = 1
FPS = 60
TICK_RATE = 600
GRID_SIZE = (18, 32)
CELL_SIZE = 40
MARGIN = 1 
WINDOW_SIZE = (GRID_SIZE[X] * (CELL_SIZE + MARGIN) + MARGIN, GRID_SIZE[Y] * (CELL_SIZE + MARGIN) + MARGIN)
# WINDOW_SIZE =(GRID_SIZE[X] * CELL_SIZE, GRID_SIZE[Y] * CELL_SIZE)

SCREEN = pg.display.set_mode(WINDOW_SIZE)
CLOCK = pg.time.Clock()
NEXT_TICK_TIME = pg.time.get_ticks() + TICK_RATE
STOPPED = False

BLACK = (0, 0, 0)
WHITE = (200, 200, 200)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
COLOR_MAP = {0: WHITE, 1: BLUE, 2: GREEN, 3: RED, 4: BLACK}

grid = [[0 for _ in range(GRID_SIZE[X])] for _ in range(GRID_SIZE[Y])]
grid[0][16] = 4
grid[1][16] = 4
grid[2][16] = 4
grid[3][16] = 4
grid[4][16] = 4
grid[5][16] = 4
grid[6][16] = 4
grid[7][16] = 4
grid[8][15] = 4

Player = Player([GRID_SIZE[Y]//2, GRID_SIZE[X]//2])
grid[Player.position[Y]][Player.position[X]] = 1

Enemy = Enemy([10, 10])
grid[Enemy.position[Y]][Enemy.position[X]] = 3

Pathfinder = Pathfinder(grid)

def get_rect(r, c):
    return [(MARGIN + CELL_SIZE) * c + MARGIN, (MARGIN + CELL_SIZE) * r + MARGIN, CELL_SIZE, CELL_SIZE]
    # return [CELL_SIZE * c, CELL_SIZE * r, CELL_SIZE, CELL_SIZE]

while not STOPPED:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            STOPPED = True
        elif event.type == pg.MOUSEBUTTONDOWN:
            mouse_pos = pg.mouse.get_pos()
            col_coord = mouse_pos[X] // (CELL_SIZE + MARGIN)
            row_coord = mouse_pos[Y] // (CELL_SIZE + MARGIN)
            
            if not (0 <= col_coord < GRID_SIZE[Y] and 0 <= row_coord < GRID_SIZE[X]):
                continue

            click_pos = [col_coord, row_coord]

            if click_pos == Enemy.position:
                if Player.position != Player.dest_pos:
                    grid[Player.dest_pos[Y]][Player.dest_pos[X]] = 0
                Player.action_queue.append("attack")
                Player.is_attacking = True
                Player.is_moving = False
                continue

            if Player.dest_pos != click_pos and Player.dest_pos != Player.position:
                grid[Player.dest_pos[Y]][Player.dest_pos[X]] = 0
            
            Player.dest_pos = click_pos
            grid[Player.dest_pos[Y]][Player.dest_pos[X]] = 2
            Player.action_queue.append("move_player")
            Player.path = Pathfinder.find_path(tuple(Player.position), tuple(Player.dest_pos))
            if Player.path:
                Player.path = deque(Player.path)
                # Remove the first node since the player is already there
                Player.path.popleft() 
                grid[Player.dest_pos[Y]][Player.dest_pos[X]] = 2
                Player.is_moving = True
            else:
                Player.path = deque()
                Player.is_moving = False

    current_time = pg.time.get_ticks()
    if current_time > NEXT_TICK_TIME:
        if Player.action_queue:
            action = Player.action_queue.popleft()
            if action == "move_player":
                Player.is_moving = True
            if action == "attack":
                Player.is_moving = False
                Player.attack()
                Player.is_attacking = False
        
        if Player.is_moving: Player.move(grid)
        Enemy.move(grid, Player.position)

        NEXT_TICK_TIME = current_time + TICK_RATE

    SCREEN.fill(BLACK)
    # SCREEN.fill(WHITE)
    for r in range(GRID_SIZE[Y]):
        for c in range(GRID_SIZE[X]):
            color = COLOR_MAP.get(grid[r][c], WHITE)
            pg.draw.rect(SCREEN, color, get_rect(r, c))
            # pg.draw.rect(SCREEN, color, get_rect(r, c), MARGIN+2)

    pg.display.flip()
    CLOCK.tick(FPS)

pg.quit()
