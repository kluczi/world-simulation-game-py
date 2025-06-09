import random
from world.world import World

class HexWorld(World):
    def __init__(self, width, height):
        super().__init__(width, height)
        self.__random = random.Random()

    def random_field(self, x, y):
        even_dirs = [(1, 0), (0, -1), (-1, 0), (0, 1), (-1, 1), (1, 1)]
        odd_dirs  = [(1, 0), (1, -1), (0, -1), (-1, 0), (0, 1), (1, 1)]
        directions = even_dirs if (x % 2 == 0) else odd_dirs
        neighbors = [(x + dx, y + dy) for dx, dy in directions]
        self.__random.shuffle(neighbors)
        for nx, ny in neighbors:
            if self.is_position_valid(nx, ny):
                return nx, ny
        return x, y
