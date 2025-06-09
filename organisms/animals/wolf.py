from organisms.animals.animal import Animal

class Wolf(Animal):
    def __init__(self, x, y, world):
        super().__init__(9, 5, x, y, world, "Wolf")

    def create_child(self, x, y):
        return Wolf(x, y, self._world)
