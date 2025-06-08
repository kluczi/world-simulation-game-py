from src.Organisms.Animals.Animal import Animal
import random

class Turtle(Animal):
    __random = random.Random()

    def __init__(self, x, y, world):
        super().__init__(2, 1, x, y, world, "🐢")

    def action(self):
        if Turtle.__random.randint(0, 3) != 0:
            self._world.addLog(f"{self.draw()} at ({self.getX()}, {self.getY()}) is lazy and stays on his position")
            return
        super().action()

    def collision(self, opponent):
        if isinstance(opponent, Turtle):
            super().collision(opponent)
            return
        if opponent.getStrength() < 5:
            self._world.addLog(f"{self.draw()} at ({self.getX()}, {self.getY()}) defends attack of {opponent.draw()} with strength {opponent.getStrength()}")
            return
        super().collision(opponent)

    def createChild(self, x, y):
        return Turtle(x, y, self._world)
