from abc import ABC, abstractmethod
from organisms.organism import Organism
from organisms.plants.plant import Plant

class Animal(Organism, ABC):
    def __init__(self, strength, initiative, x, y, world, icon):
        super().__init__(strength, initiative, x, y, world, icon)

    def action(self):
        if self.get_last_reproduction_turn() == self._world.get_turn_number():
            return
        new_x, new_y = self._world.random_field(self.get_x(), self.get_y())
        opponent = self._world.find_organism(new_x, new_y)
        if opponent is not None:
            opponent.collision(self)
            if opponent.is_dead():
                self._world.add_log(
                    f"{self.draw()} moves from ({self.get_x()}, {self.get_y()}) to ({new_x}, {new_y})"
                )
                self.set_position(new_x, new_y)
        else:
            self._world.add_log(
                f"{self.draw()} moves from ({self.get_x()}, {self.get_y()}) to ({new_x}, {new_y})"
            )
            self.set_position(new_x, new_y)

    def collision(self, opponent):
        if isinstance(opponent, Plant):
            opponent.collision(self)
        elif type(self) is type(opponent):
            if (self.get_last_reproduction_turn() == self._world.get_turn_number() or
                opponent.get_last_reproduction_turn() == self._world.get_turn_number()):
                return
            new_x, new_y = self._world.random_field(self.get_x(), self.get_y())
            if (not self._world.is_position_valid(new_x, new_y) or
                self._world.find_organism(new_x, new_y) is not None):
                return
            child = self.create_child(new_x, new_y)
            if child is not None:
                self._world.add_log(
                    f"{self.draw()} at ({self.get_x()}, {self.get_y()}) reproduces with "
                    f"{opponent.draw()} at ({opponent.get_x()}, {opponent.get_y()}), "
                    f"child at ({new_x}, {new_y})"
                )
                self.set_last_reproduction_turn(self._world.get_turn_number())
                opponent.set_last_reproduction_turn(self._world.get_turn_number())
        else:
            if self.get_strength() > opponent.get_strength():
                self._world.add_log(
                    f"{self.draw()} (str {self.get_strength()}) at ({self.get_x()}, {self.get_y()}) "
                    f"killed {opponent.draw()} (str {opponent.get_strength()}) "
                    f"at ({opponent.get_x()}, {opponent.get_y()})"
                )
                opponent.kill()
            elif self.get_strength() < opponent.get_strength():
                self._world.add_log(
                    f"{opponent.draw()} (str {opponent.get_strength()}) at ({opponent.get_x()}, {opponent.get_y()}) "
                    f"killed {self.draw()} (str {self.get_strength()}) "
                    f"at ({self.get_x()}, {self.get_y()})"
                )
                self.kill()
            else:
                self._world.add_log(
                    f"{self.draw()} (str {self.get_strength()}) at ({self.get_x()}, {self.get_y()}) "
                    f"killed {opponent.draw()} (str {opponent.get_strength()}) "
                    f"at ({opponent.get_x()}, {opponent.get_y()}) because attacked first"
                )
                opponent.kill()
                self.set_position(opponent.get_x(), opponent.get_y())

    @abstractmethod
    def create_child(self, x, y):
        pass
