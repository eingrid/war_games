import numpy as np

class Map():
    def __init__(self, frontline_longtitude,terrain=None) -> None:
        self.max_longtitude, self.max_latitude = terrain.shape
        self.terrain = terrain
        self.action_map = np.zeros(terrain.shape)
        self.frontline_longtitude = frontline_longtitude

    def update_action_map(self,latitude, longitutte, value):
        if (self._is_in_range(latitude,longitutte)):
            self.action_map[latitude][longitutte] = value

    def is_point_available(self,latitude, longitutte):
        return self.action_map[latitude][longitutte] == 0
    
    def clear_unit(self,latitude, longitutte):
        self.action_map[latitude][longitutte] = 0

    def _is_in_range(self,latitude, longitutte):
        return (latitude < (self.max_latitude)) & (longitutte < (self.max_longtitude))

    # map converter from C# engine to np.ndarray
    def __convert_to_np_map(self):      
        pass

class Field:
    def __init__(self, vulnerability) -> None:
        self.vulnerability = vulnerability

    def get_vulnerability(self):
        return VULNERABILITY_MAPPER[self.vulnerability]


    
VULNERABILITY_MAPPER = {
    1: 0.8,
    2: 0.7,
    3: 0.2
}   