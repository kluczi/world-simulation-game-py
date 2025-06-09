from organisms.animals.animal import Animal
from organisms.plants.sosnowsky_hogweed import SosnowskyHogweed

class CyberSheep(Animal):
    def __init__(self, x, y, world):
        super().__init__(11, 4, x, y, world, "CyberSheep")

    def action(self):
        hogweeds = [o for o in self._world.get_organisms() if isinstance(o, SosnowskyHogweed)]
        if not hogweeds:
            super().action()
            return

        sx, sy = self.get_x(), self.get_y()
        target = min(hogweeds, key=lambda o: abs(o.get_x()-sx) + abs(o.get_y()-sy))
        tx, ty = target.get_x(), target.get_y()
        dx = 1 if tx > sx else -1 if tx < sx else 0
        dy = 1 if ty > sy else -1 if ty < sy else 0
        if dx != 0:
            nx, ny = sx + dx, sy
        else:
            nx, ny = sx, sy + dy

        if not self._world.is_position_valid(nx, ny):
            return

        occupant = self._world.find_organism(nx, ny)
        if occupant is None:
            self._world.add_log(f"{self.draw()} moves from ({sx},{sy}) to ({nx},{ny})")
            self.set_position(nx, ny)
        else:
            self._world.add_log(f"{self.draw()} at ({sx},{sy}) attacks {occupant.draw()} at ({nx},{ny})")
            self.collision(occupant)

    def collision(self, opponent):
        if isinstance(opponent, SosnowskyHogweed):
            self._world.add_log(f"{self.draw()} eats {opponent.draw()} at ({opponent.get_x()},{opponent.get_y()})")
            opponent.kill()
            self.set_position(opponent.get_x(), opponent.get_y())
        else:
            super().collision(opponent)

    def create_child(self, x, y):
        return CyberSheep(x, y, self._world)