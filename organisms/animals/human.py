from organisms.animals.animal import Animal

class Human(Animal):
    def __init__(self, x, y, world):
        super().__init__(5, 4, x, y, world, "Human")
        self.__ability_active = False
        self.__remaining_ability_turns = 0
        self.__turns_to_ability_ready = 0
        self.__last_decrement_turn = -1

    def action(self):
        input_char = self._world.get_input()
        if not input_char:
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
            self._world.add_log(f"{self.draw()} at ({self.get_x()}, {self.get_y()}) stays")
            return
        if not self._world.is_position_valid(new_x, new_y):
            return
        opponent = self._world.find_organism(new_x, new_y)
        if self.__ability_active and opponent and opponent.get_strength() > self.get_strength():
            free_x, free_y = self.get_x(), self.get_y()
            for _ in range(10):
                rx, ry = self._world.random_field(self.get_x(), self.get_y())
                if self._world.is_position_valid(rx, ry) and not self._world.find_organism(rx, ry):
                    free_x, free_y = rx, ry
                    break
            self._world.add_log(f"{self.draw()} uses ability to run from {opponent.draw()} to ({free_x}, {free_y})")
            self.set_position(free_x, free_y)
        elif opponent:
            self._world.add_log(
                f"{self.draw()} (str {self.get_strength()}) attacks "
                f"{opponent.draw()} (str {opponent.get_strength()}) at ({new_x}, {new_y})"
            )
            opponent.collision(self)
            if not self.is_dead() and opponent.is_dead():
                self.set_position(new_x, new_y)
                self._world.add_log(f"{self.draw()} moves to ({new_x}, {new_y})")
        else:
            self.set_position(new_x, new_y)
            self._world.add_log(f"{self.draw()} moves to ({new_x}, {new_y})")

    def collision(self, opponent):
        if self.__ability_active and opponent.get_strength() > self.get_strength():
            self._world.add_log(
                f"{opponent.draw()} at ({opponent.get_x()}, {opponent.get_y()}) "
                f"tried to attack {self.draw()} at ({self.get_x()}, {self.get_y()}) but has immortality"
            )
            free_x, free_y = self.get_x(), self.get_y()
            for _ in range(10):
                rx, ry = self._world.random_field(self.get_x(), self.get_y())
                if self._world.is_position_valid(rx, ry) and not self._world.find_organism(rx, ry):
                    free_x, free_y = rx, ry
                    break
            self._world.add_log(f"{self.draw()} runs away to ({free_x}, {free_y})")
            self.set_position(free_x, free_y)
            return
        super().collision(opponent)

    def create_child(self, x, y):
        return None

    def activate_ability(self):
        if not self.__ability_active and self.__turns_to_ability_ready == 0:
            self.__ability_active = True
            self.__remaining_ability_turns = 5
            self.__last_decrement_turn = -1

    def is_ability_active(self):
        return self.__ability_active

    def get_remaining_ability_turns(self):
        return self.__remaining_ability_turns

    def get_turns_to_ability_ready(self):
        return self.__turns_to_ability_ready

    def decrement_ability_turns(self):
        current = self._world.get_turn_number()
        if current == self.__last_decrement_turn:
            return
        if self.__remaining_ability_turns > 0:
            self.__remaining_ability_turns -= 1
            if self.__remaining_ability_turns == 0:
                self.__ability_active = False
                self.__turns_to_ability_ready = 5
        self.__last_decrement_turn = current

    def decrement_turns_to_activation(self):
        current = self._world.get_turn_number()
        if current == self.__last_decrement_turn:
            return
        if self.__turns_to_ability_ready > 0:
            self.__turns_to_ability_ready -= 1
        self.__last_decrement_turn = current

    def set_ability_active(self, active):
        self.__ability_active = active

    def set_remaining_ability_turns(self, remaining):
        self.__remaining_ability_turns = remaining

    def set_turns_to_ability_ready(self, turns):
        self.__turns_to_ability_ready = turns
