from Animal import Animal
import random

class Antelope(Animal):
    __random = random.Random()

    def __init__(self, x, y, world):
        super().__init__(4, 4, x, y, world, "🐐")

    def action(self):
        oldX, oldY = self.getX(), self.getY()
        newX, newY = oldX, oldY
        fieldFound = False
        for _ in range(10):
            newX, newY = oldX, oldY
            d = Antelope.__random.randint(0, 3)
            if d == 0:
                newY = oldY - 2
            elif d == 1:
                newY = oldY + 2
            elif d == 2:
                newX = oldX - 2
            else:
                newX = oldX + 2
            if self._world.isPositionValid(newX, newY):
                fieldFound = True
                break
        if not fieldFound:
            self._world.addLog(f"{self.draw()} at ({oldX}, {oldY}) found no free field and stays")
            return
        opponent = self._world.findOrganism(newX, newY)
        if opponent is not None:
            self._world.addLog(f"{self.draw()} at ({oldX}, {oldY}) atacks {opponent.draw()} at ({newX}, {newY})")
            opponent.collision(self)
            if not self.isDead() and self._world.findOrganism(newX, newY) is None:
                self.setPosition(newX, newY)
                self._world.addLog(f"{self.draw()} moves to ({newX}, {newY})")
        else:
            self._world.addLog(f"{self.draw()} moves from ({oldX}, {oldY}) to ({newX}, {newY})")
            self.setPosition(newX, newY)

    def collision(self, opponent):
        if Antelope.__random.randint(0, 1) == 0:
            oldX, oldY = self.getX(), self.getY()
            newX, newY = oldX, oldY
            fieldFound = False
            for _ in range(8):
                pos = self._world.randomField(newX, newY)
                newX, newY = pos[0], pos[1]
                if self._world.isPositionValid(newX, newY) and self._world.findOrganism(newX, newY) is None:
                    fieldFound = True
                    break
            if fieldFound:
                self.setPosition(newX, newY)
                self._world.addLog(f"{self.draw()} runs away from ({oldX}, {oldY}) from {opponent.draw()} at ({opponent.getX()}, {opponent.getY()}) to ({newX}, {newY})")
            else:
                self._world.addLog(f"{self.draw()} at ({oldX}, {oldY}) tries to run from {opponent.draw()} at ({opponent.getX()}, {opponent.getY()}) but found no free field and stays")
            return
        self._world.addLog(f"{self.draw()} at ({self.getX()}, {self.getY()}) fights with {opponent.draw()} at ({opponent.getX()}, {opponent.getY()})")
        super().collision(opponent)

    def createChild(self, x, y):
        return Antelope(x, y, self._world)
