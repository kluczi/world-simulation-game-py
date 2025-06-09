from organisms.animals.cyber_sheep import CyberSheep
from world.grid_world import GridWorld
from game_window import GameWindow
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



def main():
    world = GridWorld(15, 15)
    # Antelope(5, 5, world)
    # Fox(1, 1, world)
    # Fox(2, 1, world)
    # Fox(3, 1, world)
    # Sheep(7, 7, world)
    Human(1, 1, world)
    # Wolf(15, 15, world)
    SosnowskyHogweed(14, 14, world)
    CyberSheep(3, 3, world)
    # Grass(4, 4, world)
    # Guarana(6, 6, world)
    # Nightshade(8, 8, world)
    # SosnowskyHogweed(9, 9, world)
    window = GameWindow(world)
    window.run()

if __name__ == '__main__':
    main()
