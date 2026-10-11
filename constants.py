import pygame as pg

Y = 0
X = 1
FPS = 60
TICK_RATE = 600
GRID_SIZE = (18, 32)
CELL_SIZE = 40
MARGIN = 1 
WINDOW_SIZE = (GRID_SIZE[X] * (CELL_SIZE + MARGIN) + MARGIN, GRID_SIZE[Y] * (CELL_SIZE + MARGIN) + MARGIN)

SCREEN = pg.display.set_mode(WINDOW_SIZE)
CLOCK = pg.time.Clock()
STOPPED = False

GRID_STATES = {
    "empty": 0,
    "player": 1,
    "player_dest": 2,
    "enemy": 3,
    "wall": 4,
}

BLACK = (0, 0, 0)
WHITE = (200, 200, 200)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
COLOR_MAP = {
    GRID_STATES["empty"]: WHITE,
    GRID_STATES["player"]: BLUE,
    GRID_STATES["player_dest"]: GREEN,
    GRID_STATES["enemy"]: RED,
    GRID_STATES["wall"]: BLACK
}

PLAYER_STARTING_POS = [GRID_SIZE[Y]//2, GRID_SIZE[X]//2]
ENEMY_STARTING_POS = [10, 10]