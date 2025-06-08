from abc import ABC, abstractmethod
from collections import deque
from world.grid_world import GridWorld
from world.hex_world import HexWorld

from organisms.animals.antelope import Antelope
from organisms.animals.fox import Fox
from organisms.animals.sheep import Sheep
from organisms.animals.turtle import Turtle
from organisms.animals.wolf import Wolf
from organisms.animals.human import Human

from organisms.plants.sosnowsky_hogweed import SosnowskyHogweed
from organisms.plants.guarana import Guarana
from organisms.plants.grass import Grass
from organisms.plants.nightshade import Nightshade

class World(ABC):
    def __init__(self, width=20, height=20):
        self._width = width
        self._height = height
        self._turn_number = 0
        self.__organisms = []
        self.__logs = []
        self.__input = deque()

    def set_input(self, c):
        self.__input.clear()
        self.__input.append(c)

    def get_input(self):
        return self.__input.popleft() if self.__input else 0

    def save_to_file(self, filename):
        with open(filename, 'w') as f:
            world_type = "HEX" if isinstance(self, HexWorld) else "GRID"
            f.write(f"{world_type} {self._width} {self._height} {self._turn_number}\n")
            human = next((o for o in self.__organisms if isinstance(o, Human)), None)
            if human:
                status = "ACTIVE" if human.is_ability_active() else "INACTIVE"
                f.write(f"{status} {human.get_remaining_ability_turns()} {human.get_turns_to_ability_ready()}\n")
            else:
                f.write("INACTIVE 0 0\n")
            for o in self.__organisms:
                f.write(f"{o.__class__.__name__} {o.get_x()} {o.get_y()} {o.get_strength()} {o.get_age()}\n")

    @staticmethod
    def load_from_file(filename):
        with open(filename, 'r') as f:
            header = f.readline().split()
            world = HexWorld(int(header[1]), int(header[2])) if header[0] == "HEX" else GridWorld(int(header[1]), int(header[2]))
            world._turn_number = int(header[3])

            ability_info = f.readline().split()
            active = (ability_info[0] == "ACTIVE")
            rem, cd = int(ability_info[1]), int(ability_info[2])

            for line in f:
                parts = line.split()
                typ, x, y, str_, age = parts[0], int(parts[1]), int(parts[2]), int(parts[3]), int(parts[4])
                cls = {
                    "Fox": Fox, "Wolf": Wolf, "Sheep": Sheep, "Turtle": Turtle,
                    "Antelope": Antelope, "Human": Human,
                    "SosnowskyHogweed": SosnowskyHogweed, "Guarana": Guarana,
                    "Grass": Grass, "Nightshade": Nightshade
                }.get(typ, None)
                if cls:
                    org = cls(x, y, world)
                    org.set_strength(str_)
                    for _ in range(age):
                        org.increment_age()
                    if isinstance(org, Human):
                        org.set_ability_active(active)
                        org.set_remaining_ability_turns(rem)
                        org.set_turns_to_ability_ready(cd)
        return world

    def execute_turn(self):
        self.__sort_organisms()
        for o in list(self.__organisms):
            if isinstance(o, Human):
                if o.is_ability_active():
                    o.decrement_ability_turns()
                elif o.get_turns_to_ability_ready() > 0:
                    o.decrement_turns_to_activation()
        for o in list(self.__organisms):
            if not o.is_dead():
                o.action()
                if not o.is_dead():
                    other = self.find_organism(o.get_x(), o.get_y())
                    if other and other is not o and not other.is_dead():
                        o.collision(other)
                o.increment_age()
        self.__remove_dead_organisms()
        self._turn_number += 1

    def __sort_organisms(self):
        self.__organisms.sort(key=lambda o: (-o.get_initiative(), -o.get_age()))

    def __remove_dead_organisms(self):
        self.__organisms = [o for o in self.__organisms if not o.is_dead()]

    def add_organism(self, organism):
        self.__organisms.append(organism)

    def find_organism(self, x, y):
        for o in self.__organisms:
            if o.get_x() == x and o.get_y() == y:
                return o
        return None

    def is_position_valid(self, x, y):
        return 0 <= x < self._width and 0 <= y < self._height

    def add_log(self, log):
        self.__logs.append(log)

    def get_logs(self):
        return list(self.__logs)

    def clear_logs(self):
        self.__logs.clear()

    def get_organisms(self):
        return list(self.__organisms)

    def get_turn_number(self):
        return self._turn_number

    def get_width(self):
        return self._width

    def get_height(self):
        return self._height

    @abstractmethod
    def random_field(self, x, y):
        pass
