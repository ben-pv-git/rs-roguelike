from collections import deque

Y = 0
X = 1

class Entity:
    def __init__(self, position):
        self.position = position

    def attack(self):
        print("attack")

class Player(Entity):
    def __init__(self, position):
        super().__init__(position)
        self.dest_pos = self.position
        self.is_attacking = False
        self.is_moving = self.position != self.dest_pos
        self.action_queue = deque()
        self.path = None
        self.is_running = True

    def move(self, grid):
        if not self.path:
            return
        if self.is_running and len(self.path) >= 2:
            self.path.popleft()
        grid[self.position[Y]][self.position[X]] = 0
        next = self.path.popleft()
        grid[next[Y]][next[X]] = 1
        self.position = [next[Y], next[X]]

class Enemy(Entity):
    def move(self, grid, player_pos):
        dist_to_player = [self.position[Y] - player_pos[Y], self.position[X] - player_pos[X]]
        adjacent = (abs(dist_to_player[Y]) == 1 and dist_to_player[X] == 0) or \
                   (abs(dist_to_player[X]) == 1 and dist_to_player[Y] == 0)
        if adjacent:
            return
        grid[self.position[Y]][self.position[X]] = 0 
        move_speed = 1
        if dist_to_player[Y] != 0:
            next_y = self.position[Y] - move_speed if dist_to_player[Y] > 0 else self.position[Y] + move_speed
            if grid[next_y][self.position[X]] != 4:
                self.position[Y] = next_y
        if dist_to_player[X] != 0:
            next_x = self.position[X] - move_speed if dist_to_player[X] > 0 else self.position[X] + move_speed
            if grid[self.position[Y]][next_x] != 4:
                self.position[X] = next_x
        grid[self.position[Y]][self.position[X]] = 3