from organisms.animals.animal import Animal

class Sheep(Animal):
    def __init__(self, x, y, world):
        super().__init__(4, 4, x, y, world, "Sheep")

    def create_child(self, x, y):
        return Sheep(x, y, self._world)
