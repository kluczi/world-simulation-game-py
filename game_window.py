import sys
import pygame
from virtual_world.world import World
from virtual_world.organisms.animals.human import Human

CELL_SIZE = 32
INFO_PANEL_WIDTH = 200
FPS = 30

class GameWindow:
    def __init__(self, world: World):
        pygame.init()
        self.world = world
        self.width = world.get_width()
        self.height = world.get_height()
        self.screen = pygame.display.set_mode(
            (self.width * CELL_SIZE + INFO_PANEL_WIDTH,
             self.height * CELL_SIZE)
        )
        pygame.display.set_caption("Wirtualny Świat")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 24)
        self.next_turn_button = pygame.Rect(
            self.width * CELL_SIZE + 20, 20, INFO_PANEL_WIDTH - 40, 40
        )

    def draw_grid(self):
        for x in range(self.width):
            for y in range(self.height):
                rect = pygame.Rect(
                    x * CELL_SIZE, y * CELL_SIZE,
                    CELL_SIZE, CELL_SIZE
                )
                pygame.draw.rect(self.screen, (200, 200, 200), rect, 1)

    def draw_organisms(self):
        for org in self.world.get_organisms():
            text = self.font.render(org.draw(), True, (0, 0, 0))
            px = org.get_x() * CELL_SIZE + (CELL_SIZE - text.get_width()) // 2
            py = org.get_y() * CELL_SIZE + (CELL_SIZE - text.get_height()) // 2
            self.screen.blit(text, (px, py))

    def draw_button(self):
        pygame.draw.rect(self.screen, (100, 200, 100), self.next_turn_button)
        txt = self.font.render("Następna tura", True, (0, 0, 0))
        tx = self.next_turn_button.x + (self.next_turn_button.width - txt.get_width()) // 2
        ty = self.next_turn_button.y + (self.next_turn_button.height - txt.get_height()) // 2
        self.screen.blit(txt, (tx, ty))

    def draw_logs(self):
        logs = self.world.get_logs()[-10:]
        for i, line in enumerate(logs):
            txt = self.font.render(line, True, (0, 0, 0))
            self.screen.blit(
                txt,
                (self.width * CELL_SIZE + 10, 80 + i * 20)
            )

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                human = next(
                    (o for o in self.world.get_organisms()
                     if isinstance(o, Human) and not o.is_dead()),
                    None
                )
                if human:
                    if event.key == pygame.K_UP:
                        self.world.set_input('U')
                    elif event.key == pygame.K_DOWN:
                        self.world.set_input('D')
                    elif event.key == pygame.K_LEFT:
                        self.world.set_input('L')
                    elif event.key == pygame.K_RIGHT:
                        self.world.set_input('R')
                    elif event.key == pygame.K_SPACE:
                        human.activate_ability()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.next_turn_button.collidepoint(event.pos):
                    self.world.clear_logs()
                    self.world.execute_turn()

    def run(self):
        while True:
            self.handle_input()
            self.screen.fill((255, 255, 255))
            self.draw_grid()
            self.draw_organisms()
            self.draw_button()
            self.draw_logs()
            pygame.display.flip()
            self.clock.tick(FPS)

if __name__ == "__main__":
    world = World(20, 20)
    gui = GameWindow(world)
    gui.run()
