from abc import ABC, abstractmethod
import random

class World(ABC):
    def __init__(self, width, height):
        self.__width = width
        self.__height = height
        self._turn_number = 0
        self._organisms = []
        self._logs = []
        self._random = random.Random()

    def get_width(self):
        return self.__width

    def get_height(self):
        return self.__height

    def get_turn_number(self):
        return self._turn_number

    def add_organism(self, organism):
        self._organisms.append(organism)

    def find_organism(self, x, y):
        for o in self._organisms:
            if o.get_x() == x and o.get_y() == y and not o.is_dead():
                return o
        return None

    def add_log(self, message):
        self._logs.append(f"Turn {self._turn_number}: {message}")

    def get_logs(self):
        return self._logs

    def next_turn(self):
        self._turn_number += 1
        for o in list(self._organisms):
            if not o.is_dead():
                o.increment_age()
                o.action()
        self._organisms = [o for o in self._organisms if not o.is_dead()]

    def random_field(self, x, y):
        neighbors = self.get_neighbors(x, y)
        if not neighbors:
            return x, y
        return self._random.choice(neighbors)

    @abstractmethod
    def get_neighbors(self, x, y):
        pass

    def is_position_valid(self, x, y):
        return 0 <= x < self.__width and 0 <= y < self.__height