from src.Organisms.Animals.Animal import Animal

class Fox(Animal):
    def __init__(self, x, y, world):
        super().__init__(3, 7, x, y, world, "🦊")

    def action(self):
        moved = False
        for _ in range(4):
            newX, newY = self._world.randomField(self.getX(), self.getY())
            if not self._world.isPositionValid(newX, newY):
                continue
            opponent = self._world.findOrganism(newX, newY)
            if opponent is None:
                self._world.addLog(f"{self.draw()} moves from ({self.getX()}, {self.getY()}) to ({newX}, {newY})")
                self.setPosition(newX, newY)
                moved = True
                break
            if isinstance(opponent, Fox):
                self.collision(opponent)
                moved = True
                break
            if opponent.getStrength() > self.getStrength():
                run_away = None
                for _ in range(6):
                    pos2 = self._world.randomField(self.getX(), self.getY())
                    if self._world.isPositionValid(pos2[0], pos2[1]) and self._world.findOrganism(pos2[0], pos2[1]) is None:
                        run_away = pos2
                        break
                if run_away:
                    self._world.addLog(f"{self.draw()} from ({self.getX()}, {self.getY()}) feels that {opponent.draw()} with strength {opponent.getStrength()} is stronger and runs away to ({run_away[0]}, {run_away[1]})")
                    self.setPosition(run_away[0], run_away[1])
                else:
                    self._world.addLog(f"{self.draw()} at ({self.getX()}, {self.getY()}) feels that {opponent.draw()} is stronger but found no free field and stays")
                moved = True
                break
            self._world.addLog(f"{self.draw()} moves from ({self.getX()}, {self.getY()}) to ({newX}, {newY})")
            self.setPosition(newX, newY)
            moved = True
            break
        if not moved:
            self._world.addLog(f"{self.draw()} at ({self.getX()}, {self.getY()}) found no free field and stays")

    def createChild(self, x, y):
        return Fox(x, y, self._world)
