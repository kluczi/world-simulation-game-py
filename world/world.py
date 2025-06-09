import os
from abc import ABC, abstractmethod
from collections import deque
from organisms.animals.human import Human
from organisms.animals.antelope import Antelope
from organisms.animals.fox import Fox
from organisms.animals.sheep import Sheep
from organisms.animals.turtle import Turtle
from organisms.animals.wolf import Wolf
from organisms.plants.dandelion import Dandelion
from organisms.plants.sosnowsky_hogweed import SosnowskyHogweed
from organisms.plants.guarana import Guarana
from organisms.plants.grass import Grass
from organisms.plants.nightshade import Nightshade
from organisms.animals.cyber_sheep import CyberSheep

class World(ABC):
    def __init__(self, width=20, height=20):
        self._width = width
        self._height = height
        self._turn_number = 0
        self.__organisms = []
        self.__logs = []
        self.__input = deque()

    def add_organism(self, org):
        self.__organisms.append(org)

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

    def set_input(self, direction):
        self.__input.clear()
        self.__input.append(direction)

    def get_input(self):
        return self.__input.popleft() if self.__input else None

    def execute_turn(self):
        self.__organisms.sort(key=lambda o: (-o.get_initiative(), -o.get_age()))
        for o in list(self.__organisms):
            if not o.is_dead():
                o.action()
                other = self.find_organism(o.get_x(), o.get_y())
                if other and other is not o and not other.is_dead():
                    o.collision(other)
                o.increment_age()
        self.__organisms = [o for o in self.__organisms if not o.is_dead()]
        self._turn_number += 1
        for o in self.__organisms:
            if isinstance(o, Human):
                if o.is_ability_active():
                    o.decrement_ability_turns()
                elif o.get_turns_to_ability_ready() > 0:
                    o.decrement_turns_to_activation()

    @abstractmethod
    def random_field(self, x, y):
        pass

    def save_to_file(self, filename: str):
        os.makedirs('worlds', exist_ok=True)
        path = filename if os.path.dirname(filename) else os.path.join('worlds', filename)
        with open(path, 'w') as f:
            wt = 'HEX' if type(self).__name__ == 'HexWorld' else 'GRID'
            f.write(f"{wt} {self._width} {self._height} {self._turn_number}\n")
            human = next((o for o in self.__organisms if isinstance(o, Human)), None)
            if human:
                status = 'ACTIVE' if human.is_ability_active() else 'INACTIVE'
                rem = human.get_remaining_ability_turns()
                cd = human.get_turns_to_ability_ready()
            else:
                status, rem, cd = 'INACTIVE', 0, 0
            f.write(f"{status} {rem} {cd}\n")
            for o in self.__organisms:
                f.write(f"{o.__class__.__name__} {o.get_x()} {o.get_y()} {o.get_strength()} {o.get_age()}\n")

    @staticmethod
    def load_from_file(filename: str):
        import os
        from world.grid_world import GridWorld
        from world.hex_world import HexWorld
        path = filename if os.path.dirname(filename) else os.path.join('worlds', filename)
        with open(path, 'r') as f:
            typ, w, h, turn = f.readline().split()
            w, h, turn = int(w), int(h), int(turn)
            world = HexWorld(w, h) if typ == 'HEX' else GridWorld(w, h)
            world._turn_number = turn
            status, rem, cd = f.readline().split()
            rem, cd = int(rem), int(cd)
            for line in f:
                data = line.split()
                cls = {
                    'Antelope': Antelope,
                    'Fox': Fox,
                    'Sheep': Sheep,
                    'Turtle': Turtle,
                    'Wolf': Wolf,
                    'Human': Human,
                    'CyberSheep': CyberSheep,
                    'Dandelion': Dandelion,
                    'SosnowskyHogweed': SosnowskyHogweed,
                    'Guarana': Guarana,
                    'Grass': Grass,
                    'Nightshade': Nightshade
                }.get(data[0])
                if not cls:
                    continue
                x, y, strength, age = map(int, data[1:5])
                org = cls(x, y, world)
                org.set_strength(strength)
                for _ in range(age):
                    org.increment_age()
                if isinstance(org, Human):
                    org.set_ability_active(status == 'ACTIVE')
                    org.set_remaining_ability_turns(rem)
                    org.set_turns_to_ability_ready(cd)
                world.add_organism(org)
        return world
