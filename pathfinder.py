from collections import deque

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