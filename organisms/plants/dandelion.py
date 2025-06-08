from organisms.plants.plant import Plant

class Dandelion(Plant):
    def __init__(self, x, y, world):
        super().__init__(0, x, y, world, "🌼")

    def action(self):
        for _ in range(3):
            super().action()

    def create_plant(self, x, y):
        return Dandelion(x, y, self._world)
