from abc import ABC, abstractmethod
from Organism import Organism
from Plant import Plant

class Animal(Organism, ABC):
    def __init__(self, strength, initiative, x, y, world, icon):
        super().__init__(strength, initiative, x, y, world, icon)

    def action(self):
        if self.getLastReproductionTurn() == self._world.getTurnNumber():
            return
        newX, newY = self._world.randomField(self.getX(), self.getY())
        opponent = self._world.findOrganism(newX, newY)
        if opponent is not None:
            opponent.collision(self)
            if opponent.isDead():
                self._world.addLog(
                    f"{self.draw()} moves from ({self.getX()}, {self.getY()}) to ({newX}, {newY})"
                )
                self.setPosition(newX, newY)
        else:
            self._world.addLog(
                f"{self.draw()} moves from ({self.getX()}, {self.getY()}) to ({newX}, {newY})"
            )
            self.setPosition(newX, newY)

    def collision(self, opponent):
        if isinstance(opponent, Plant):
            opponent.collision(self)
        elif type(self) is type(opponent):
            if (self.getLastReproductionTurn() == self._world.getTurnNumber() or
                opponent.getLastReproductionTurn() == self._world.getTurnNumber()):
                return
            newX, newY = self._world.randomField(self.getX(), self.getY())
            if (not self._world.isPositionValid(newX, newY) or
                self._world.findOrganism(newX, newY) is not None):
                return
            child = self.createChild(newX, newY)
            if child is not None:
                self._world.addLog(
                    f"{self.draw()} at ({self.getX()}, {self.getY()}) reproduces with "
                    f"{opponent.draw()} at ({opponent.getX()}, {opponent.getY()}), "
                    f"child at ({newX}, {newY})"
                )
                self.setLastReproductionTurn(self._world.getTurnNumber())
                opponent.setLastReproductionTurn(self._world.getTurnNumber())
        else:
            if self.getStrength() > opponent.getStrength():
                self._world.addLog(
                    f"{self.draw()} (str {self.getStrength()}) at ({self.getX()}, {self.getY()}) "
                    f"killed {opponent.draw()} (str {opponent.getStrength()}) "
                    f"at ({opponent.getX()}, {opponent.getY()})"
                )
                opponent.kill()
            elif self.getStrength() < opponent.getStrength():
                self._world.addLog(
                    f"{opponent.draw()} (str {opponent.getStrength()}) at ({opponent.getX()}, {opponent.getY()}) "
                    f"killed {self.draw()} (str {self.getStrength()}) "
                    f"at ({self.getX()}, {self.getY()})"
                )
                self.kill()
            else:
                self._world.addLog(
                    f"{self.draw()} (str {self.getStrength()}) at ({self.getX()}, {self.getY()}) "
                    f"killed {opponent.draw()} (str {opponent.getStrength()}) "
                    f"at ({opponent.getX()}, {opponent.getY()}) because attacked first"
                )
                opponent.kill()
                self.setPosition(opponent.getX(), opponent.getY())

    @abstractmethod
    def createChild(self, x, y):
        pass
