import random
from world.world import World

class GridWorld(World):
    def __init__(self, width=20, height=20):
        super().__init__(width, height)

    def random_field(self, x, y):
        dirs = [(0,-1),(0,1),(-1,0),(1,0)]
        dx, dy = random.choice(dirs)
        return x+dx, y+dy