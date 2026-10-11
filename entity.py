from collections import deque
from constants import Y, X, GRID_STATES
from pathfinder import Pathfinder

class Entity:
    def __init__(self, position):
        self.position = position

class Player(Entity):
    def __init__(self, position):
        super().__init__(position)
        self.dest_pos = self.position
        self.is_attacking = False
        self.action_queue = deque()
        self.path = None
        self.is_running = True
        self.attack_counter = 0

    @property
    def is_moving(self):
        return self.position != self.dest_pos
    
    def find_path(self, grid):
        pf = Pathfinder(grid)
        self.path = pf.find_path(tuple(self.position), tuple(self.dest_pos))
        if not self.path:
            self.path = deque()
            return
        self.path = deque(self.path)
        # remove the first node since the player is already there
        self.path.popleft()
        grid[self.dest_pos[Y]][self.dest_pos[X]] = GRID_STATES["player_dest"]

    def move(self, grid):
        if not self.path:
            return
        if self.is_running and len(self.path) >= 2:
            self.path.popleft()
        grid[self.position[Y]][self.position[X]] = GRID_STATES["empty"]
        next = self.path.popleft()
        grid[next[Y]][next[X]] = GRID_STATES["player"]
        self.position = next

    def attack(self):
        self.is_attacking = True
        self.dest_pos = self.position
        print(f"attack{self.attack_counter}")
        self.attack_counter += 1

class MeleeEnemy(Entity):
    def __init__(self, position):
        super().__init__(position)
        self.move_speed = 1

    def move(self, player_pos: list[int], grid):
        dist_to_player = [self.position[Y] - player_pos[Y], self.position[X] - player_pos[X]]
        adjacent = (abs(dist_to_player[Y]) == 1 and dist_to_player[X] == 0) or \
                   (abs(dist_to_player[X]) == 1 and dist_to_player[Y] == 0)
        if adjacent:
            return
        grid[self.position[Y]][self.position[X]] = GRID_STATES["empty"]
        move_speed = 1
        if dist_to_player[Y] != 0:
            next_y = self.position[Y] - move_speed if dist_to_player[Y] > 0 else self.position[Y] + move_speed
            if grid[next_y][self.position[X]] != GRID_STATES["wall"]:
                self.position[Y] = next_y
        if dist_to_player[X] != 0:
            next_x = self.position[X] - move_speed if dist_to_player[X] > 0 else self.position[X] + move_speed
            if grid[self.position[Y]][next_x] != GRID_STATES["wall"]:
                self.position[X] = next_x
        grid[self.position[Y]][self.position[X]] = GRID_STATES["enemy"]
