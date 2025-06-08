from organisms.plants.plant import Plant

class Nightshade(Plant):
    def __init__(self, x, y, world):
        super().__init__(99, x, y, world, "🍄")

    def collision(self, opponent):
        self._world.add_log(
            f"{opponent.draw()} at ({opponent.get_x()}, {opponent.get_y()}) ate "
            f"{self.draw()} at ({self.get_x()}, {self.get_y()}) and died from poisoning"
        )
        opponent.kill()
        self.kill()

    def create_plant(self, x, y):
        return Nightshade(x, y, self._world)
