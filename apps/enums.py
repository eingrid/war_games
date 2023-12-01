from enum import Enum
import pygame

from utils import get_absolute_path

class Cell(Enum):
    EMPTY = {"name": "Empty Cell", "image": pygame.image.load(get_absolute_path("/textures/EMPTY_TEX.png")), "value": 0}
    TREE = {"name": "Cell With Trees", "image": pygame.image.load(get_absolute_path("/textures/TEX_TREE.png")), "value": 1}
    HILL = {"name": "Cell With Hill", "image": pygame.image.load(get_absolute_path("/textures/HILL_TEX.png")), "value": 2}
    MOUNTAIN = {
        "name": "Cell With Mountain",
        "image": pygame.image.load(get_absolute_path("/textures/TEX_MOUNTAIN.png")),
        "value": 3,
    }

class TroopImage(Enum):
    TROOP = {"name": "troop", "image": pygame.image.load(get_absolute_path("/textures/troop_tex.png"))}
    TANK = {"name": "tank", "image": pygame.image.load(get_absolute_path("/textures/tank_modified.png"))}
    ARTILLERY = {"name": "artillery", "image": pygame.image.load(get_absolute_path("/textures/artillery_tex.png"))}
    