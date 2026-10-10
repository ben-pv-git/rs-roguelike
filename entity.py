from collections import deque
from constants import Y, X, GRID_STATES

class Entity:
    def __init__(self, position):
        self.position = position

class Player(Entity):
    def __init__(self, position):
        super().__init__(position)
        self.dest_pos = [None, None]
        self.is_attacking = False
        self.is_moving = self.position != self.dest_pos
        self.action_queue = deque()
        self.path = None
        self.is_running = True
        self.attack_counter = 0

    def move(self, grid):
        if not self.path:
            return
        if self.is_running and len(self.path) >= 2:
            self.path.popleft()
        grid[self.position[Y]][self.position[X]] = GRID_STATES["empty"]
        next = self.path.popleft()
        grid[next[Y]][next[X]] = GRID_STATES["player"]
        self.position = [next[Y], next[X]]

    def attack(self):
        self.is_attacking = True
        self.is_moving = False
        print(f"attack{self.attack_counter}")
        self.attack_counter += 1

class MeleeEnemy(Entity):
    def move(self, grid, player_pos):
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
