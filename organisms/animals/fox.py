from organisms.animals.animal import Animal

class Fox(Animal):
    def __init__(self, x, y, world):
        super().__init__(3, 7, x, y, world, "Fox")

    def action(self):
        moved = False
        for _ in range(4):
            new_x, new_y = self._world.random_field(self.get_x(), self.get_y())
            if not self._world.is_position_valid(new_x, new_y):
                continue
            opponent = self._world.find_organism(new_x, new_y)
            if opponent is None:
                self._world.add_log(
                    f"{self.draw()} moves from ({self.get_x()}, {self.get_y()}) "
                    f"to ({new_x}, {new_y})"
                )
                self.set_position(new_x, new_y)
                moved = True
                break
            if isinstance(opponent, Fox):
                self.collision(opponent)
                moved = True
                break
            if opponent.get_strength() > self.get_strength():
                run_away = None
                for _ in range(6):
                    rx, ry = self._world.random_field(self.get_x(), self.get_y())
                    if (self._world.is_position_valid(rx, ry) and
                        self._world.find_organism(rx, ry) is None):
                        run_away = (rx, ry)
                        break
                if run_away:
                    self._world.add_log(
                        f"{self.draw()} from ({self.get_x()}, {self.get_y()}) feels that "
                        f"{opponent.draw()} (str {opponent.get_strength()}) is stronger "
                        f"and runs away to ({run_away[0]}, {run_away[1]})"
                    )
                    self.set_position(run_away[0], run_away[1])
                else:
                    self._world.add_log(
                        f"{self.draw()} at ({self.get_x()}, {self.get_y()}) feels that "
                        f"{opponent.draw()} is stronger but found no free field and stays"
                    )
                moved = True
                break
            self._world.add_log(
                f"{self.draw()} moves from ({self.get_x()}, {self.get_y()}) "
                f"to ({new_x}, {new_y})"
            )
            self.set_position(new_x, new_y)
            moved = True
            break
        if not moved:
            self._world.add_log(
                f"{self.draw()} at ({self.get_x()}, {self.get_y()}) found no free field and stays"
            )

    def create_child(self, x, y):
        return Fox(x, y, self._world)
