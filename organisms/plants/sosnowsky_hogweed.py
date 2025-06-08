from organisms.plants.plant import Plant
from organisms.animals.animal import Animal
from organisms.animals.human import Human

class SosnowskyHogweed(Plant):
    def __init__(self, x, y, world):
        super().__init__(10, x, y, world, "🌿")

    def action(self):
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                if dx == 0 and dy == 0:
                    continue
                nx, ny = self.get_x() + dx, self.get_y() + dy
                if self._world.is_position_valid(nx, ny):
                    opponent = self._world.find_organism(nx, ny)
                    if isinstance(opponent, Animal):
                        if isinstance(opponent, Human) and opponent.is_ability_active():
                            self._world.add_log(
                                f"{opponent.draw()} at ({nx}, {ny}) is immune to "
                                f"{self.draw()} at ({self.get_x()}, {self.get_y()})"
                            )
                        else:
                            self._world.add_log(
                                f"{self.draw()} at ({self.get_x()}, {self.get_y()}) kills "
                                f"{opponent.draw()} at ({nx}, {ny})"
                            )
                            opponent.kill()
        super().action()

    def collision(self, opponent):
        self._world.add_log(
            f"{opponent.draw()} at ({opponent.get_x()}, {opponent.get_y()}) ate "
            f"{self.draw()} at ({self.get_x()}, {self.get_y()}) and died from poisoning"
        )
        opponent.kill()
        self.kill()

    def create_plant(self, x, y):
        return SosnowskyHogweed(x, y, self._world)
