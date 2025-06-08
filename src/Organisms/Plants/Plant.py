from abc import ABC, abstractmethod
from Organism import Organism
import random

class Plant(Organism, ABC):
    __random = random.Random()

    def __init__(self, strength, x, y, world, icon):
        super().__init__(strength, 0, x, y, world, icon)

    def action(self):
        if Plant.__random.randint(0, 9) == 0:
            self.spread()

    def collision(self, opponent):
        self.kill()

    def spread(self):
        freeFields = 0
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                if dx == 0 and dy == 0:
                    continue
                nx, ny = self.getX() + dx, self.getY() + dy
                if (self._world.isPositionValid(nx, ny) and
                    self._world.findOrganism(nx, ny) is None):
                    freeFields += 1
        if freeFields == 0:
            return
        choice = Plant.__random.randint(0, freeFields - 1)
        count = 0
        newX = newY = -1
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                if dx == 0 and dy == 0:
                    continue
                nx, ny = self.getX() + dx, self.getY() + dy
                if (self._world.isPositionValid(nx, ny) and
                    self._world.findOrganism(nx, ny) is None):
                    if count == choice:
                        newX, newY = nx, ny
                        break
                    count += 1
            if newX != -1:
                break
        if newX != -1 and self._world.findOrganism(newX, newY) is None:
            spreadPlant = self.createPlant(newX, newY)
            if spreadPlant is not None:
                self._world.addLog(
                    f"{self.draw()} spreads to ({newX}, {newY})"
                )

    @abstractmethod
    def createPlant(self, x, y):
        pass
