from enum import Enum
import pygame



class Cell(Enum):
    EMPTY = {"name": "Empty Cell", "image": pygame.image.load("textures/EMPTY_TEX.png"), "value": 0}
    TREE = {"name": "Cell With Trees", "image": pygame.image.load("textures/TEX_TREE.png"), "value": 1}
    HILL = {"name": "Cell With Hill", "image": pygame.image.load("textures/HILL_TEX.png"), "value": 2}
    MOUNTAIN = {
        "name": "Cell With Mountain",
        "image": pygame.image.load("textures/TEX_MOUNTAIN.png"),
        "value": 3,
    }

class TroopImage(Enum):
    TROOP = {"name": "troop", "image": pygame.image.load("textures/tank_modified.png")}
    TANK = {"name": "tank", "image": pygame.image.load("textures/troop_tex.png")}
    