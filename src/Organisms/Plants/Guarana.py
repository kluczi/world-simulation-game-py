from Plant import Plant

class Guarana(Plant):
    def __init__(self, x, y, world):
        super().__init__(0, x, y, world, "🌺")

    def collision(self, opponent):
        opponent.setStrength(opponent.getStrength() + 3)
        self._world.addLog(
            opponent.draw() + " at (" + str(opponent.getX()) + ", " + str(opponent.getY()) +
            ") ate " + self.draw() + " at (" + str(self.getX()) + ", " + str(self.getY()) +
            ") and gained additional 3 strength. New strength: " + str(opponent.getStrength())
        )
        self.kill()

    def createPlant(self, x, y):
        return Guarana(x, y, self._world)
