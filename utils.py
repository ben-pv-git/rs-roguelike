from pathfinder import Pathfinder
from collections import deque
from constants import X, Y, GRID_STATES
from entity import Player

def handle_left_click(player: Player, grid, click_pos):
    pf = Pathfinder(grid)
    if player.dest_pos != [None, None] and player.dest_pos != click_pos and player.dest_pos != player.position:
        grid[player.dest_pos[Y]][player.dest_pos[X]] = GRID_STATES["empty"]
    player.dest_pos = click_pos
    grid[player.dest_pos[Y]][player.dest_pos[X]] = GRID_STATES["player_dest"]
    player.action_queue.append("move_player")
    player.path = pf.find_path(tuple(player.position), tuple(player.dest_pos))
    if player.path:
        player.path = deque(player.path)
        # remove the first node since the player is already there
        player.path.popleft()
        grid[player.dest_pos[Y]][player.dest_pos[X]] = GRID_STATES["player_dest"]
        player.is_moving = True
    else:
        player.path = deque()
        player.is_moving = False

def draw_wall(grid):
    grid[0][16] = 4
    grid[1][16] = 4
    grid[2][16] = 4
    grid[3][16] = 4
    grid[4][16] = 4
    grid[5][16] = 4
    grid[6][16] = 4
    grid[7][16] = 4
    grid[8][15] = 4