import numpy as np


class Field:
    def __init__(self, vulnerability) -> None:
        self.vulnerability = vulnerability

    def get_vulnerability(self):
        return VULNERABILITY_MAPPER[self.vulnerability]


class Map():
    def __init__(self, terrain=None) -> None:
        self.max_longtitude, self.max_latitude = terrain.shape
        self.terrain = terrain
        # self.terrain = self.__convert_to_np_map(terrain) 

    def __convert_to_np_map(self):      # map converter from C# engine to np.ndarray
        pass

    
VULNERABILITY_MAPPER = {
    1: 0.8,
    2: 0.7,
    3: 0.2
}

    