from abc import ABC, abstractmethod
from organisms.organism import Organism
import random

class Plant(Organism, ABC):
    __random = random.Random()

    def __init__(self, strength, x, y, world, name):
        super().__init__(strength, 0, x, y, world, name)

    def action(self):
        if Plant.__random.randint(0, 9) == 0:
            self.spread()

    def collision(self, opponent):
        self.kill()

    def spread(self):
        free_fields = 0
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                if dx == 0 and dy == 0:
                    continue
                nx, ny = self.get_x() + dx, self.get_y() + dy
                if (self._world.is_position_valid(nx, ny) and
                    self._world.find_organism(nx, ny) is None):
                    free_fields += 1
        if free_fields == 0:
            return
        choice = Plant.__random.randint(0, free_fields - 1)
        count = 0
        new_x = new_y = -1
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                if dx == 0 and dy == 0:
                    continue
                nx, ny = self.get_x() + dx, self.get_y() + dy
                if (self._world.is_position_valid(nx, ny) and
                    self._world.find_organism(nx, ny) is None):
                    if count == choice:
                        new_x, new_y = nx, ny
                        break
                    count += 1
            if new_x != -1:
                break
        if new_x != -1 and self._world.find_organism(new_x, new_y) is None:
            new_plant = self.create_plant(new_x, new_y)
            if new_plant is not None:
                self._world.add_log(
                    f"{self.draw()} spreads to ({new_x}, {new_y})"
                )

    @abstractmethod
    def create_plant(self, x, y):
        pass
