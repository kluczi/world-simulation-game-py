import sys
import pygame
import pygame_gui
from pygame_gui.elements import UIButton, UISelectionList, UILabel
from pygame_gui.windows import UIFileDialog

from organisms.animals.cyber_sheep import CyberSheep
from world.grid_world import GridWorld
from organisms.animals.antelope import Antelope
from organisms.animals.fox import Fox
from organisms.animals.sheep import Sheep
from organisms.animals.turtle import Turtle
from organisms.animals.wolf import Wolf
from organisms.animals.human import Human
from organisms.plants.dandelion import Dandelion
from organisms.plants.grass import Grass
from organisms.plants.guarana import Guarana
from organisms.plants.nightshade import Nightshade
from organisms.plants.sosnowsky_hogweed import SosnowskyHogweed
from organisms.plants.plant import Plant
from organisms.animals.animal import Animal

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768

class GameWindow:
    def __init__(self, world: GridWorld):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
        pygame.display.set_caption("ddd")
        self.world = world
        self.panel_width = 200
        self.log_height = 150
        self.font_ui = pygame.font.SysFont(None, 24)
        self.line_h = self.font_ui.get_height()
        self.max_visible = self.log_height // self.line_h
        self.gui_manager = pygame_gui.UIManager((SCREEN_WIDTH, SCREEN_HEIGHT))
        self._create_ui()
        self._layout()
        self._refresh()
        self.save_dialog = None
        self.load_dialog = None
        self.selection_list = None
        self.organism_options = [
            (f"{cls.__name__[0]} {cls.__name__}", cls)
            for cls in (Human, Antelope, Fox, Sheep, Turtle, Wolf,
                        Dandelion, Grass, Guarana, Nightshade, SosnowskyHogweed, CyberSheep)
        ]
        self.game_info = [
            "Bartosz Kluska, s203185",
            "Animals: H - Human, W - Wolf, S - Sheep, F - Fox, A - Antelope, T - Turtle, C - CyberSheep",
            "Plants: G - Grass, D - Dandelion, U - Guarana, N - Nightshade, S - Sosnowsky Hogweed",
            "Controls: U - human ability, Arrows: up - move up, down - move down, left - move left, right - move right"
        ]

    def _create_ui(self):
        x0 = SCREEN_WIDTH - self.panel_width
        bw, bh = self.panel_width - 20, 30
        self.btn_next = UIButton(pygame.Rect((x0+10,10),(bw,bh)), "Next Turn", manager=self.gui_manager)
        self.btn_save = UIButton(pygame.Rect((x0+10,50),(bw,bh)), "Save", manager=self.gui_manager)
        self.btn_load = UIButton(pygame.Rect((x0+10,90),(bw,bh)), "Load", manager=self.gui_manager)
        self.lbl_move = UILabel(pygame.Rect((x0+10,130),(bw,bh)), "Move: None", manager=self.gui_manager)
        self.lbl_turn = UILabel(pygame.Rect((x0+10,170),(bw,bh)), "", manager=self.gui_manager)
        self.lbl_ability = UILabel(pygame.Rect((x0+10,210),(bw,bh)), "", manager=self.gui_manager)

    def _layout(self):
        self.cols = self.world.get_width()
        self.rows = self.world.get_height()
        grid_w = SCREEN_WIDTH - self.panel_width
        grid_h = SCREEN_HEIGHT - self.log_height
        cw = grid_w // self.cols
        ch = grid_h // self.rows
        self.cell_size = max(5, min(32, cw, ch))
        self.grid_width = self.cols * self.cell_size
        self.grid_height = self.rows * self.cell_size
        self.offset_x = (grid_w - self.grid_width) // 2
        self.offset_y = (grid_h - self.grid_height) // 2
        self.font_cell = pygame.font.SysFont(None, int(self.cell_size * 0.75))

    def run(self):
        clock = pygame.time.Clock()
        while True:
            dt = clock.tick(30) / 1000.0
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if ev.type == pygame.VIDEORESIZE:
                    self.screen = pygame.display.set_mode((ev.w, ev.h), pygame.RESIZABLE)
                    self.gui_manager.set_window_resolution((ev.w, ev.h))
                if ev.type == pygame_gui.UI_BUTTON_PRESSED:
                    if ev.ui_element == self.btn_next:
                        self.world.clear_logs()
                        self.world.execute_turn()
                        self._refresh()
                    elif ev.ui_element == self.btn_save:
                        self.save_dialog = UIFileDialog(pygame.Rect((100,100),(600,400)), manager=self.gui_manager, window_title="Save World", initial_file_path="worlds")
                    elif ev.ui_element == self.btn_load:
                        self.load_dialog = UIFileDialog(pygame.Rect((100,100),(600,400)), manager=self.gui_manager, window_title="Load World", initial_file_path="worlds")
                if ev.type == pygame_gui.UI_FILE_DIALOG_PATH_PICKED:
                    if ev.ui_element == self.save_dialog:
                        self.world.save_to_file(ev.text)
                        self.save_dialog.kill()
                        self.save_dialog = None
                    elif ev.ui_element == self.load_dialog:
                        self.world = type(self.world).load_from_file(ev.text)
                        self.load_dialog.kill()
                        self.load_dialog = None
                        self._layout()
                        self._refresh()
                if ev.type == pygame_gui.UI_WINDOW_CLOSE and ev.ui_element in (self.save_dialog, self.load_dialog):
                    ev.ui_element.kill()
                    self.save_dialog = None
                    self.load_dialog = None
                if ev.type == pygame.MOUSEBUTTONDOWN:
                    if self.selection_list and not self.selection_list.relative_rect.collidepoint(ev.pos):
                        self.selection_list.kill()
                        self.selection_list = None
                    elif ev.button == 1 and not self.selection_list:
                        mx, my = ev.pos
                        gx0, gy0 = self.offset_x, self.offset_y
                        if gx0 <= mx < gx0 + self.grid_width and gy0 <= my < gy0 + self.grid_height:
                            col = (mx - gx0) // self.cell_size
                            row = (my - gy0) // self.cell_size
                            if not any(o.get_x() == col and o.get_y() == row for o in self.world.get_organisms()):
                                items = [d for d, _ in self.organism_options]
                                h_list = min(len(items) * 30, 200)
                                lx = min(mx, SCREEN_WIDTH - 150)
                                ly = min(my, SCREEN_HEIGHT - h_list)
                                self.selected_cell = (col, row)
                                self.selection_list = UISelectionList(pygame.Rect((lx, ly), (150, h_list)), item_list=items, manager=self.gui_manager)
                if ev.type == pygame_gui.UI_SELECTION_LIST_NEW_SELECTION and self.selection_list and ev.ui_element == self.selection_list:
                    for disp, cls in self.organism_options:
                        if disp == ev.text:
                            x, y = self.selected_cell
                            cls(x, y, self.world)
                            self.world.add_log(f"Added {disp} at ({x},{y})")
                            break
                    self.selection_list.kill()
                    self.selection_list = None
                if ev.type == pygame.KEYDOWN:
                    if ev.key == pygame.K_ESCAPE and self.selection_list:
                        self.selection_list.kill()
                        self.selection_list = None
                    human = next((o for o in self.world.get_organisms() if isinstance(o,Human) and not o.is_dead()), None)
                    if human:
                        if ev.key == pygame.K_u:
                            human.activate_ability()
                            self._refresh()
                        move = None
                        if ev.key == pygame.K_UP:
                            self.world.set_input('U')
                            move = "Up"
                        elif ev.key == pygame.K_DOWN:
                            self.world.set_input('D')
                            move = "Down"
                        elif ev.key == pygame.K_LEFT:
                            self.world.set_input('L')
                            move = "Left"
                        elif ev.key == pygame.K_RIGHT:
                            self.world.set_input('R')
                            move = "Right"
                        if move:
                            self.lbl_move.set_text(f"Move: {move}")
                self.gui_manager.process_events(ev)
            self.screen.fill((30,30,30))
            self._draw_grid()
            self._draw_organisms()
            self.gui_manager.update(dt)
            self.gui_manager.draw_ui(self.screen)
            self._draw_info()
            self._draw_logs()
            pygame.display.flip()

    def _draw_info(self):
        y0 = self.offset_y + self.grid_height + 5
        for i, line in enumerate(self.game_info):
            txt = self.font_ui.render(line, True, (255,255,255))
            self.screen.blit(txt, (5, y0 + i*self.line_h))

    def _refresh(self):
        self.lbl_turn.set_text(f"Turn: {self.world.get_turn_number()}")
        human = next((o for o in self.world.get_organisms() if isinstance(o,Human)), None)
        if human:
            if human.is_ability_active():
                self.lbl_ability.set_text(f"Ability: active ({human.get_remaining_ability_turns()} left)")
            else:
                t = human.get_turns_to_ability_ready()
                self.lbl_ability.set_text(f"Ability: ready in {t}" if t>0 else "Ability: ready")
        else:
            self.lbl_ability.set_text("Ability: none")

    def _draw_grid(self):
        for x in range(self.cols):
            for y in range(self.rows):
                r = pygame.Rect(self.offset_x + x*self.cell_size, self.offset_y + y*self.cell_size, self.cell_size, self.cell_size)
                pygame.draw.rect(self.screen, (200,200,200), r, 1)

    def _draw_organisms(self):
        for o in self.world.get_organisms():
            r = pygame.Rect(self.offset_x + o.get_x()*self.cell_size, self.offset_y + o.get_y()*self.cell_size, self.cell_size, self.cell_size)
            color = (0,150,0) if isinstance(o,Plant) else (255,165,0) if isinstance(o,Human) else (200,0,0) if isinstance(o,Animal) else (100,100,100)
            pygame.draw.rect(self.screen, color, r)
            txt = self.font_cell.render(o.__class__.__name__[0], True, (255,255,255))
            self.screen.blit(txt, (r.x + (r.width-txt.get_width())//2, r.y + (r.height-txt.get_height())//2))

    def _draw_logs(self):
        logs = self.world.get_logs()
        pygame.draw.rect(self.screen, (40,40,40), (0, SCREEN_HEIGHT-self.log_height, SCREEN_WIDTH, self.log_height))
        start = max(0, len(logs)-self.max_visible)
        for i, line in enumerate(logs[start:]):
            txt = self.font_ui.render(line, True, (255,255,255))
            self.screen.blit(txt, (5, SCREEN_HEIGHT-self.log_height + i*self.line_h))
        total = len(logs)
        if total > self.max_visible:
            bar_h = max(10, self.log_height*self.max_visible//total)
            off = (total-self.max_visible)*(self.log_height-bar_h)//(total-self.max_visible)
            bx, by = SCREEN_WIDTH-10, SCREEN_HEIGHT-self.log_height+off
            pygame.draw.rect(self.screen, (180,180,180), (bx,by,8,bar_h))
