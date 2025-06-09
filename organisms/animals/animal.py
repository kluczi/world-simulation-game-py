import random
from organisms.organism import Organism
from organisms.plants.plant import Plant

class Animal(Organism):
    _random = random.Random()

    def action(self):
        old_x, old_y = self.get_x(), self.get_y()
        directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        self._random.shuffle(directions)
        for dx, dy in directions:
            new_x, new_y = old_x + dx, old_y + dy
            if not self._world.is_position_valid(new_x, new_y):
                continue
            occupant = self._world.find_organism(new_x, new_y)
            if occupant:
                if type(occupant) is type(self):
                    self.collision(occupant)
                    return
                self._world.add_log(f"{self.draw()} at ({old_x},{old_y}) attacks {occupant.draw()} at ({new_x},{new_y})")
                occupant.collision(self)
                if not self.is_dead() and self._world.find_organism(new_x, new_y) is None:
                    self.set_position(new_x, new_y)
                    self._world.add_log(f"{self.draw()} moves to ({new_x},{new_y})")
            else:
                self._world.add_log(f"{self.draw()} moves from ({old_x},{old_y}) to ({new_x},{new_y})")
                self.set_position(new_x, new_y)
            return
        self._world.add_log(f"{self.draw()} at ({old_x},{old_y}) found no free field and stays")

    def collision(self, opponent):
        if isinstance(opponent, Plant):
            opponent.collision(self)
        elif type(self) is type(opponent):
            if (self.get_last_reproduction_turn() == self._world.get_turn_number()
                or opponent.get_last_reproduction_turn() == self._world.get_turn_number()):
                return
            nx, ny = self._world.random_field(self.get_x(), self.get_y())
            if (not self._world.is_position_valid(nx, ny)
                or self._world.find_organism(nx, ny) is not None):
                return
            child = self.create_child(nx, ny)
            if child:
                self._world.add_organism(child)
                self._world.add_log(
                    f"{self.draw()} at ({self.get_x()},{self.get_y()}) reproduces with "
                    f"{opponent.draw()} at ({opponent.get_x()},{opponent.get_y()}), child at ({nx},{ny})"
                )
                self.set_last_reproduction_turn(self._world.get_turn_number())
                opponent.set_last_reproduction_turn(self._world.get_turn_number())
        else:
            sx, sy = self.get_x(), self.get_y()
            ox, oy = opponent.get_x(), opponent.get_y()
            if self.get_strength() > opponent.get_strength():
                self._world.add_log(
                    f"{self.draw()} with strength {self.get_strength()} at ({sx},{sy}) killed "
                    f"{opponent.draw()} with strength {opponent.get_strength()} at ({ox},{oy})"
                )
                opponent.kill()
                self.set_position(ox, oy)
            elif self.get_strength() < opponent.get_strength():
                self._world.add_log(
                    f"{opponent.draw()} with strength {opponent.get_strength()} at ({ox},{oy}) killed "
                    f"{self.draw()} with strength {self.get_strength()} at ({sx},{sy})"
                )
                self.kill()
                opponent.set_position(sx, sy)
            else:
                self._world.add_log(
                    f"{self.draw()} with strength {self.get_strength()} at ({sx},{sy}) killed "
                    f"{opponent.draw()} with strength {opponent.get_strength()} at ({ox},{oy}) because he attacked first"
                )
                opponent.kill()
                self.set_position(ox, oy)

    def create_child(self, x, y):
        pass
