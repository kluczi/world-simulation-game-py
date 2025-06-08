import random
from world.world import World

class GridWorld(World):
    def __init__(self, width, height):
        super().__init__(width, height)
        self.__random = random.Random()

    def random_field(self, x, y):
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        neighbors = [(x + dx, y + dy) for dx, dy in directions]
        self.__random.shuffle(neighbors)
        for nx, ny in neighbors:
            if self.is_position_valid(nx, ny):
                return nx, ny
        return x, y
