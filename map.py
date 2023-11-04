import numpy as np


class Field:
    def __init__(self, vulnerability) -> None:
        self.vulnerability = vulnerability


class Map():
    def __init__(self, terrain=None) -> None:
        self.terrain = None # 2x2 matrix with class for each cell