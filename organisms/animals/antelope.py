from organisms.animals.animal import Animal
import random

class Antelope(Animal):
    __random = random.Random()

    def __init__(self, x, y, world):
        super().__init__(4, 4, x, y, world, "Antelope")

    def action(self):
        old_x, old_y = self.get_x(), self.get_y()
        directions = [(0, -2), (0, 2), (-2, 0), (2, 0)]
        __random = Antelope.__random
        for _ in range(10):
            dx, dy = __random.choice(directions)
            new_x = old_x + dx
            new_y = old_y + dy
            if self._world.is_position_valid(new_x, new_y):
                break
        else:
            self._world.add_log(f"{self.draw()} at ({old_x}, {old_y}) found no free field and stays")
            return
        opponent = self._world.find_organism(new_x, new_y)
        if opponent:
            self._world.add_log(f"{self.draw()} at ({old_x}, {old_y}) attacks {opponent.draw()} at ({new_x}, {new_y})")
            opponent.collision(self)
            if not self.is_dead() and self._world.find_organism(new_x, new_y) is None:
                self.set_position(new_x, new_y)
                self._world.add_log(f"{self.draw()} moves to ({new_x}, {new_y})")
        else:
            self._world.add_log(f"{self.draw()} moves from ({old_x}, {old_y}) to ({new_x}, {new_y})")
            self.set_position(new_x, new_y)

    def collision(self, opponent):
        __random = Antelope.__random
        if __random.randint(0, 1) == 0:
            old_x, old_y = self.get_x(), self.get_y()
            directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
            for _ in range(8):
                dx, dy = __random.choice(directions)
                nx, ny = old_x + dx, old_y + dy
                if self._world.is_position_valid(nx, ny) and self._world.find_organism(nx, ny) is None:
                    self.set_position(nx, ny)
                    self._world.add_log(
                        f"{self.draw()} runs away from ({old_x}, {old_y}) from "
                        f"{opponent.draw()} at ({opponent.get_x()}, {opponent.get_y()}) "
                        f"to ({nx}, {ny})"
                    )
                    return
            self._world.add_log(
                f"{self.draw()} at ({old_x}, {old_y}) tries to run from "
                f"{opponent.draw()} at ({opponent.get_x()}, {opponent.get_y()}) "
                "but found no free field and stays"
            )
            return
        self._world.add_log(
            f"{self.draw()} at ({self.get_x()}, {self.get_y()}) fights with "
            f"{opponent.draw()} at ({opponent.get_x()}, {opponent.get_y()})"
        )
        super().collision(opponent)

    def create_child(self, x, y):
        return Antelope(x, y, self._world)
