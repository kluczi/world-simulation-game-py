from organisms.plants.plant import Plant

class Grass(Plant):
    def __init__(self, x, y, world):
        super().__init__(0, x, y, world, "Grass")

    def create_plant(self, x, y):
        return Grass(x, y, self._world)
