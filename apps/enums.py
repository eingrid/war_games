from enum import Enum
import pygame

from pathlib import Path

folder = Path("/run/media/eingrid/ec26c78b-20bc-47f1-b2d5-33a92d92c9b6/UCU/Intro to ds/apps/textures")

class Cell(Enum):

    EMPTY = {"name": "Empty Cell", "image": pygame.image.load(folder/"EMPTY_TEX.png"), "value": 0}
    TREE = {"name": "Cell With Trees", "image": pygame.image.load(folder/"TEX_TREE.png"), "value": 1}
    HILL = {"name": "Cell With Hill", "image": pygame.image.load(folder/"HILL_TEX.png"), "value": 2}
    MOUNTAIN = {
        "name": "Cell With Mountain",
        "image": pygame.image.load(folder/"TEX_MOUNTAIN.png"),
        "value": 3,
    }

class TroopImage(Enum):
    TROOP = {"name": "troop", "image": pygame.image.load(folder/"troop_tex.png")}
    TANK = {"name": "tank", "image": pygame.image.load(folder/"tank_modified.png")}
    