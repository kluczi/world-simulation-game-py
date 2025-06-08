from organisms.animals.animal import Animal

class Human(Animal):
    def __init__(self, x, y, world):
        super().__init__(5, 4, x, y, world, "🧍")
        self.__ability_active = False
        self.__remaining_ability_turns = 0
        self.__turns_to_ability_ready = 0

    def action(self):
        input_char = self._world.get_input()
        if input_char == 0:
            return
        new_x, new_y = self.get_x(), self.get_y()
        if input_char == 'U':
            new_y -= 1
        elif input_char == 'D':
            new_y += 1
        elif input_char == 'L':
            new_x -= 1
        elif input_char == 'R':
            new_x += 1
        else:
            self._world.add_log(
                f"{self.draw()} at ({self.get_x()}, {self.get_y()}) stays"
            )
            return
        if not self._world.is_position_valid(new_x, new_y):
            return
        opponent = self._world.find_organism(new_x, new_y)
        if (self.__ability_active and opponent is not None and
            opponent.get_strength() > self.get_strength()):
            free_x, free_y = self.get_x(), self.get_y()
            for _ in range(10):
                rx, ry = self._world.random_field(self.get_x(), self.get_y())
                if (self._world.is_position_valid(rx, ry) and
                    self._world.find_organism(rx, ry) is None):
                    free_x, free_y = rx, ry
                    break
            self._world.add_log(
                f"{self.draw()} uses ability to run from {opponent.draw()} "
                f"to ({free_x}, {free_y})"
            )
            self.set_position(free_x, free_y)
        elif opponent is not None:
            self._world.add_log(
                f"{self.draw()} (str {self.get_strength()}) attacks "
                f"{opponent.draw()} (str {opponent.get_strength()}) at ({new_x}, {new_y})"
            )
            opponent.collision(self)
            if not self.is_dead() and opponent.is_dead():
                self.set_position(new_x, new_y)
                self._world.add_log(
                    f"{self.draw()} moves to ({new_x}, {new_y})"
                )
        else:
            self.set_position(new_x, new_y)
            self._world.add_log(
                f"{self.draw()} moves to ({new_x}, {new_y})"
            )

    def collision(self, opponent):
        if (self.__ability_active and
            opponent.get_strength() > self.get_strength()):
            self._world.add_log(
                f"{opponent.draw()} at ({opponent.get_x()}, {opponent.get_y()}) "
                f"tried to attack {self.draw()} at ({self.get_x()}, {self.get_y()}) "
                "but has immortality"
            )
            free_x, free_y = self.get_x(), self.get_y()
            for _ in range(10):
                rx, ry = self._world.random_field(self.get_x(), self.get_y())
                if (self._world.is_position_valid(rx, ry) and
                    self._world.find_organism(rx, ry) is None):
                    free_x, free_y = rx, ry
                    break
            self._world.add_log(
                f"{self.draw()} runs away to ({free_x}, {free_y})"
            )
            self.set_position(free_x, free_y)
            return
        super().collision(opponent)

    def create_child(self, x, y):
        return None

    def activate_ability(self):
        if self.__turns_to_ability_ready == 0 and not self.__ability_active:
            self.__ability_active = True
            self.__remaining_ability_turns = 5

    def is_ability_active(self):
        return self.__ability_active

    def get_remaining_ability_turns(self):
        return self.__remaining_ability_turns

    def get_turns_to_ability_ready(self):
        return self.__turns_to_ability_ready

    def set_turns_to_ability_ready(self, turns):
        self.__turns_to_ability_ready = turns

    def set_ability_active(self, active):
        self.__ability_active = active

    def set_remaining_ability_turns(self, remaining):
        self.__remaining_ability_turns = remaining

    def decrement_ability_turns(self):
        if self.__remaining_ability_turns > 0:
            self.__remaining_ability_turns -= 1
            if self.__remaining_ability_turns == 0:
                self.__ability_active = False
                self.__turns_to_ability_ready = 5

    def decrement_turns_to_activation(self):
        if self.__turns_to_ability_ready > 0:
            self.__turns_to_ability_ready -= 1
