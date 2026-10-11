import pygame as pg
from constants import X, Y, GRID_STATES, GRID_SIZE, CELL_SIZE, MARGIN, COLOR_MAP, SCREEN, BLACK, WHITE
from entity import Player

def get_rect(r, c):
    return [
        (MARGIN + CELL_SIZE) * c + MARGIN,
        (MARGIN + CELL_SIZE) * r + MARGIN,
        CELL_SIZE,
        CELL_SIZE
    ]

def get_click_pos():
    mouse_pos = pg.mouse.get_pos()
    col_coord = mouse_pos[X] // (CELL_SIZE + MARGIN)
    row_coord = mouse_pos[Y] // (CELL_SIZE + MARGIN)
    is_out_of_bounds = (
        col_coord < 0 or col_coord >= GRID_SIZE[Y] or 
        row_coord < 0 or row_coord >= GRID_SIZE[X]
    )
    return [col_coord, row_coord], is_out_of_bounds

def handle_left_click(player: Player, grid, click_pos):
    if player.is_moving and player.dest_pos != click_pos:
        grid[player.dest_pos[Y]][player.dest_pos[X]] = GRID_STATES["empty"]
    player.dest_pos = click_pos
    grid[player.dest_pos[Y]][player.dest_pos[X]] = GRID_STATES["player_dest"]
    player.find_path(grid)
    player.action_queue.extend(["move_player"] * len(player.path))

def draw_grid(grid):
    SCREEN.fill(BLACK)
    # SCREEN.fill(WHITE)
    for r in range(GRID_SIZE[Y]):
        for c in range(GRID_SIZE[X]):
            color = COLOR_MAP.get(grid[r][c], WHITE)
            pg.draw.rect(SCREEN, color, get_rect(r, c))
            # pg.draw.rect(SCREEN, color, get_rect(r, c), MARGIN+2)

def draw_wall(grid):
    for x in range(0, 8):
        grid[x][16] = GRID_STATES["wall"]
    grid[8][15] = GRID_STATES["wall"]