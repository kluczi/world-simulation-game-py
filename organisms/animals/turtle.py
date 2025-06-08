from organisms.animals.animal import Animal
import random

class Turtle(Animal):
    __random = random.Random()

    def __init__(self, x, y, world):
        super().__init__(2, 1, x, y, world, "🐢")

    def action(self):
        if Turtle.__random.randint(0, 3) != 0:
            self._world.add_log(
                f"{self.draw()} at ({self.get_x()}, {self.get_y()}) is lazy and stays"
            )
            return
        super().action()

    def collision(self, opponent):
        if isinstance(opponent, Turtle):
            super().collision(opponent)
            return
        if opponent.get_strength() < 5:
            self._world.add_log(
                f"{self.draw()} at ({self.get_x()}, {self.get_y()}) defends attack of "
                f"{opponent.draw()} (str {opponent.get_strength()})"
            )
            return
        super().collision(opponent)

    def create_child(self, x, y):
        return Turtle(x, y, self._world)
