from Plant import Plant
from src.Organisms.Animals.Animal import Animal
from src.Organisms.Animals.Human import Human

class SosnowskyHogweed(Plant):
    def __init__(self, x, y, world):
        super().__init__(10, x, y, world, "🌿")

    def action(self):
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                if dx == 0 and dy == 0:
                    continue
                newX = self.getX() + dx
                newY = self.getY() + dy
                if self._world.isPositionValid(newX, newY):
                    opponent = self._world.findOrganism(newX, newY)
                    if isinstance(opponent, Animal):
                        if isinstance(opponent, Human) and opponent.isAbilityActive():
                            self._world.addLog(
                                opponent.draw() + " at (" + str(newX) + ", " + str(newY) +
                                ") has immortality to " + self.draw() +
                                " at (" + str(self.getX()) + ", " + str(self.getY()) + ")"
                            )
                        else:
                            self._world.addLog(
                                self.draw() + " at (" + str(self.getX()) + ", " + str(self.getY()) +
                                ") kills " + opponent.draw() + " at (" + str(newX) + ", " + str(newY) + ")"
                            )
                            opponent.kill()
        super().action()

    def collision(self, opponent):
        self._world.addLog(
            opponent.draw() + " at (" + str(opponent.getX()) + ", " + str(opponent.getY()) +
            ") ate " + self.draw() + " at (" + str(self.getX()) + ", " + str(self.getY()) +
            ") and dies from poisoning"
        )
        opponent.kill()
        self.kill()

    def createPlant(self, x, y):
        return SosnowskyHogweed(x, y, self._world)
