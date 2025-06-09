from organisms.plants.plant import Plant
from organisms.animals.animal import Animal
from organisms.animals.human import Human

class SosnowskyHogweed(Plant):
    def __init__(self, x, y, world):
        super().__init__(10, x, y, world, "SosnowskyHogweed")

    def action(self):
        from organisms.animals.cyber_sheep import CyberSheep
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                if dx == 0 and dy == 0:
                    continue
                nx, ny = self.get_x() + dx, self.get_y() + dy
                if not self._world.is_position_valid(nx, ny):
                    continue
                opponent = self._world.find_organism(nx, ny)
                if isinstance(opponent, Animal) and not isinstance(opponent, CyberSheep):
                    if isinstance(opponent, Human) and opponent.is_ability_active():
                        self._world.add_log(
                            f"{opponent.draw()} at ({nx},{ny}) is immune to {self.draw()} at ({self.get_x()},{self.get_y()})"
                        )
                    else:
                        self._world.add_log(
                            f"{self.draw()} at ({self.get_x()},{self.get_y()}) kills {opponent.draw()} at ({nx},{ny})"
                        )
                        opponent.kill()
        super().action()

    def collision(self, opponent):
        self._world.add_log(
            f"{opponent.draw()} at ({opponent.get_x()},{opponent.get_y()}) ate {self.draw()} at ({self.get_x()},{self.get_y()}) and died from poisoning"
        )
        opponent.kill()
        self.kill()

    def create_plant(self, x, y):
        return SosnowskyHogweed(x, y, self._world)
