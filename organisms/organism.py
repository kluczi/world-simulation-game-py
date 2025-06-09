from abc import ABC, abstractmethod

class Organism(ABC):
    def __init__(self, strength, initiative, x, y, world, name):
        self._strength = strength
        self._initiative = initiative
        self._x = x
        self._y = y
        self._world = world
        self._name = name
        self._age = 0
        self._dead = False
        self._last_reproduction_turn = -1
        self._world.add_organism(self)

    @abstractmethod
    def action(self):
        pass

    @abstractmethod
    def collision(self, opponent):
        pass

    def get_strength(self):
        return self._strength

    def set_strength(self, strength):
        self._strength = strength

    def get_initiative(self):
        return self._initiative

    def get_x(self):
        return self._x

    def get_y(self):
        return self._y

    def set_position(self, x, y):
        self._x = x
        self._y = y

    def draw(self):
        return self._name

    def get_age(self):
        return self._age

    def increment_age(self):
        self._age += 1

    def kill(self):
        self._dead = True

    def is_dead(self):
        return self._dead

    def get_last_reproduction_turn(self):
        return self._last_reproduction_turn

    def set_last_reproduction_turn(self, turn):
        self._last_reproduction_turn = turn