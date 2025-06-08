from Plant import Plant

class Nightshade(Plant):
    def __init__(self, x, y, world):
        super().__init__(99, x, y, world, "🍄")

    def collision(self, opponent):
        self._world.addLog(
            opponent.draw() + " at (" + str(opponent.getX()) + ", " + str(opponent.getY()) +
            ") ate " + self.draw() + " at (" + str(self.getX()) + ", " + str(self.getY()) + ") and dies from poisoning"
        )
        opponent.kill()
        self.kill()

    def createPlant(self, x, y):
        return Nightshade(x, y, self._world)
