from src.Organisms.Animals.Animal import Animal

class Human(Animal):
    def __init__(self, x, y, world):
        super().__init__(5, 4, x, y, world, "🧍")
        self.__abilityActive = False
        self.__remainingAbilityTurns = 0
        self.__turnsToAbilityReady = 0

    def action(self):
        input_char = self._world.getInput()
        if input_char == 0:
            return
        newX, newY = self.getX(), self.getY()
        if input_char == 'U':
            newY -= 1
        elif input_char == 'D':
            newY += 1
        elif input_char == 'L':
            newX -= 1
        elif input_char == 'R':
            newX += 1
        else:
            self._world.addLog(f"{self.draw()} at ({self.getX()}, {self.getY()}) stays")
            return
        if not self._world.isPositionValid(newX, newY):
            return
        opponent = self._world.findOrganism(newX, newY)
        if self.__abilityActive and opponent is not None and opponent.getStrength() > self.getStrength():
            freeX, freeY = self.getX(), self.getY()
            for _ in range(10):
                pos = self._world.randomField(self.getX(), self.getY())
                if self._world.isPositionValid(pos[0], pos[1]) and self._world.findOrganism(pos[0], pos[1]) is None:
                    freeX, freeY = pos[0], pos[1]
                    break
            self._world.addLog(f"{self.draw()} uses ability to run from {opponent.draw()} to ({freeX}, {freeY})")
            self.setPosition(freeX, freeY)
        elif opponent is not None:
            self._world.addLog(f"{self.draw()} with strength {self.getStrength()} attack {opponent.draw()} with strength {opponent.getStrength()} at ({newX}, {newY})")
            opponent.collision(self)
            if not self.isDead() and opponent.isDead():
                self.setPosition(newX, newY)
                self._world.addLog(f"{self.draw()} moves to ({newX}, {newY})")
        else:
            self.setPosition(newX, newY)
            self._world.addLog(f"{self.draw()} moves to ({newX}, {newY})")

    def collision(self, opponent):
        if self.__abilityActive and opponent.getStrength() > self.getStrength():
            self._world.addLog(f"{opponent.draw()} at ({opponent.getX()}, {opponent.getY()}) tried to attack {self.draw()} at ({self.getX()}, {self.getY()}) but has immortality")
            freeX, freeY = self.getX(), self.getY()
            for _ in range(10):
                pos = self._world.randomField(self.getX(), self.getY())
                if self._world.isPositionValid(pos[0], pos[1]) and self._world.findOrganism(pos[0], pos[1]) is None:
                    freeX, freeY = pos[0], pos[1]
                    break
            self._world.addLog(f"{self.draw()} runs away to ({freeX}, {freeY})")
            self.setPosition(freeX, freeY)
            return
        super().collision(opponent)

    def createChild(self, x, y):
        return None

    def activateAbility(self):
        if self.__turnsToAbilityReady == 0 and not self.__abilityActive:
            self.__abilityActive = True
            self.__remainingAbilityTurns = 5

    def isAbilityActive(self):
        return self.__abilityActive

    def getRemainingAbilityTurns(self):
        return self.__remainingAbilityTurns

    def getTurnsToAbilityReady(self):
        return self.__turnsToAbilityReady

    def setTurnsToAbilityReady(self, turns):
        self.__turnsToAbilityReady = turns

    def setAbilityActive(self, active):
        self.__abilityActive = active

    def setRemainingAbilityTurns(self, remaining):
        self.__remainingAbilityTurns = remaining

    def decrementAbilityTurns(self):
        if self.__remainingAbilityTurns > 0:
            self.__remainingAbilityTurns -= 1
            if self.__remainingAbilityTurns == 0:
                self.__abilityActive = False
                self.__turnsToAbilityReady = 5

    def decrementTurnsToActivation(self):
        if self.__turnsToAbilityReady > 0:
            self.__turnsToAbilityReady -= 1
