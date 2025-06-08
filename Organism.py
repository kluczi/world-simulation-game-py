from abc import ABC, abstractmethod

class Organism(ABC):
    def __init__(self, strength, initiative, x, y, world, icon):
        self._strength = strength
        self._initiative = initiative
        self._x = x
        self._y = y
        self._world = world
        self._icon = icon
        self._age = 0
        self._dead = False
        self._lastReproductionTurn = -1

    @abstractmethod
    def action(self):
        pass

    @abstractmethod
    def collision(self, other):
        pass

    def getStrength(self):
        return self._strength

    def setStrength(self, strength):
        self._strength = strength

    def getInitiative(self):
        return self._initiative

    def getX(self):
        return self._x

    def getY(self):
        return self._y

    def setPosition(self, x, y):
        self._x = x
        self._y = y

    def getWorld(self):
        return self._world

    def draw(self):
        return self._icon

    def getAge(self):
        return self._age

    def incrementAge(self):
        self._age += 1

    def kill(self):
        self._dead = True

    def isDead(self):
        return self._dead

    def getLastReproductionTurn(self):
        return self._lastReproductionTurn

    def setLastReproductionTurn(self, turn):
        self._lastReproductionTurn = turn
