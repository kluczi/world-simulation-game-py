from organisms.plants.plant import Plant

class Guarana(Plant):
    def __init__(self, x, y, world):
        super().__init__(0, x, y, world, "Guarana")

    def collision(self, opponent):
        opponent.set_strength(opponent.get_strength() + 3)
        self._world.add_log(
            f"{opponent.draw()} at ({opponent.get_x()}, {opponent.get_y()}) ate "
            f"{self.draw()} at ({self.get_x()}, {self.get_y()}) and gained 3 strength. "
            f"New strength: {opponent.get_strength()}"
        )
        self.kill()

    def create_plant(self, x, y):
        return Guarana(x, y, self._world)
