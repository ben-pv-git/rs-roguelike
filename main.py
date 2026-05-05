import pygame as pg
import time
from collections import deque
import heapq

pg.init()

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
NEXT_TICK_TIME = pg.time.get_ticks() + TICK_RATE
STOPPED = False

BLACK = (0, 0, 0)
WHITE = (200, 200, 200)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
COLOR_MAP = {0: WHITE, 1: BLUE, 2: GREEN, 3: RED, 4: BLACK}

grid = [[0 for _ in range(GRID_SIZE[X])] for _ in range(GRID_SIZE[Y])]

player_pos = [GRID_SIZE[Y]//2, GRID_SIZE[X]//2]
grid[player_pos[Y]][player_pos[X]] = 1
dest_pos = player_pos
player_is_attacking = False
player_is_moving = player_pos != dest_pos
action_queue = deque()
player_path = None
player_is_running = True

enemy_pos = [10, 10]
grid[enemy_pos[Y]][enemy_pos[X]] = 3
enemy_dest_pos = player_pos

class Pathfinder:
    def __init__(self, grid):
        self.grid = grid  
        self.height = len(grid)
        self.width = len(grid[0])

    def get_neighbors(self, y, x):
        cardinals = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        diagonals = [(-1, -1), (1, -1), (-1, 1), (1, 1)]
        neighbors = []

        def is_walkable(ty, tx):
            if 0 <= tx < self.width and 0 <= ty < self.height:
                return self.grid[ty][tx] != 4
            return False

        for dy, dx in cardinals:
            if is_walkable(y + dy, x + dx):
                neighbors.append((y + dy, x + dx))

        for dy, dx in diagonals:
            if is_walkable(y + dy, x + dx):
                if is_walkable(y + dy, x) and is_walkable(y, x + dx):
                    neighbors.append((y + dy, x + dx))
        return neighbors

    def find_path(self, start, target):
        queue = deque([start])
        visited = {start: None} 
        while queue:
            current = queue.popleft()
            if current == target:
                return self.reconstruct_path(visited, target)
            for neighbor in self.get_neighbors(current[0], current[1]):
                if neighbor not in visited:
                    visited[neighbor] = current
                    queue.append(neighbor)
        return []

    def reconstruct_path(self, visited, target):
        path = []
        curr = target
        while curr is not None:
            path.append(curr)
            curr = visited[curr]
        return path[::-1]

pf = Pathfinder(grid)

def get_rect(r, c):
    return [(MARGIN + CELL_SIZE) * c + MARGIN, (MARGIN + CELL_SIZE) * r + MARGIN, CELL_SIZE, CELL_SIZE]

def move_player():
    global player_pos
    global player_path
    global grid
    if player_path:
        if player_is_running and len(player_path) >= 2:
            player_path.popleft()
        grid[player_pos[Y]][player_pos[X]] = 0
        next = player_path.popleft()
        grid[next[Y]][next[X]] = 1
        player_pos = [next[Y], next[X]]

def attack():
    print("attack")

def move_enemy():
    global grid
    global enemy_pos
    global player_pos
    grid[enemy_pos[Y]][enemy_pos[X]] = 0 
    dist_to_player = [enemy_pos[Y] - player_pos[Y], enemy_pos[X] - player_pos[X]]
    adjacent = (abs(dist_to_player[Y]) == 1 and dist_to_player[X] == 0) or \
               (abs(dist_to_player[X]) == 1 and dist_to_player[Y] == 0)
    if not adjacent:
        move_speed = 1
        if dist_to_player[Y] != 0:
            enemy_pos[Y] -= move_speed if dist_to_player[Y] > 0 else -move_speed
        if dist_to_player[X] != 0:
            enemy_pos[X] -= move_speed if dist_to_player[X] > 0 else -move_speed
    grid[enemy_pos[Y]][enemy_pos[X]] = 3

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

            if click_pos == enemy_pos:
                if player_pos != dest_pos:
                    grid[dest_pos[Y]][dest_pos[X]] = 0
                action_queue.append("attack")
                player_is_attacking = True
                player_is_moving = False
                continue

            if dest_pos != click_pos and dest_pos != player_pos:
                grid[dest_pos[Y]][dest_pos[X]] = 0
            
            dest_pos = click_pos
            grid[dest_pos[Y]][dest_pos[X]] = 2
            action_queue.append("move_player")
            path = pf.find_path(tuple(player_pos), tuple(dest_pos))
            if path:
                player_path = deque(path)
                # Remove the first node since the player is already there
                player_path.popleft() 
                grid[dest_pos[Y]][dest_pos[X]] = 2
                player_is_moving = True
            else:
                player_path = deque()
                player_is_moving = False



    current_time = pg.time.get_ticks()
    if current_time > NEXT_TICK_TIME:
        if action_queue:
            action = action_queue.popleft()
            if action == "move_player": player_is_moving = True
            if action == "attack" and player_is_attacking:
                player_is_moving = False
                attack()
                player_is_attacking = False
        
        if player_is_moving: move_player()
        move_enemy()
        NEXT_TICK_TIME = current_time + TICK_RATE

    SCREEN.fill(BLACK)
    for r in range(GRID_SIZE[Y]):
        for c in range(GRID_SIZE[X]):
            color = COLOR_MAP.get(grid[r][c], WHITE)
            pg.draw.rect(SCREEN, color, get_rect(r, c))

    pg.display.flip()
    CLOCK.tick(FPS)

pg.quit()
