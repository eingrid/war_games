import noise
import numpy as np
from enums import Cell


class Field:
    def __init__(self, vulnerability) -> None:
        self.vulnerability = vulnerability

    def get_vulnerability(self):
        return VULNERABILITY_MAPPER[self.vulnerability]

class Map:
    def __init__(self, frontline_longtitude = None, terrain: np.array = None) -> None:
        """Map object that is created using perlin noise"""
        self.max_longtitude, self.max_latitude = terrain.shape
        # self.terrain = self.__convert_to_np_map(terrain)
        self.noise_cell_mapping = {
            (0.0, 0.2): Cell.TREE.value["value"],
            (0.2, 0.4): Cell.HILL.value["value"],
            (0.4, 0.6): Cell.MOUNTAIN.value["value"],
        }
        self.terrain = self._generate_map_using_perlin_noise()
        self.action_map = np.zeros(terrain.shape)
        self.frontline_longtitude = frontline_longtitude if frontline_longtitude is not None else self.max_longtitude

    def _generate_map_using_perlin_noise(self) -> np.array:
        """Generate map using perlin noise

        returns 2d matrix with int numbers.
        """

        terrain = np.zeros((self.max_longtitude, self.max_latitude))

        # mapping between perlin noise and type of the cell

        for x in range(self.max_longtitude):
            for y in range(self.max_latitude):
                noise_value = noise.snoise2(x / 30, y / 30, octaves=6)
                terrain[x, y] = self._map_noise_to_cell(noise_value)

        return terrain

    def _map_noise_to_cell(self, noise_value):
        """Map noise to type of the cell"""

        for noise_range, cell_value in self.noise_cell_mapping.items():
            if noise_range[0] <= noise_value < noise_range[1]:
                return cell_value

        return Cell.EMPTY.value["value"]
    
    def update_action_map(self,latitude, longitutte, value):
        if (self._is_in_range(latitude,longitutte)):
            self.action_map[latitude][longitutte] = value
    
    def can_move_to_point(self,latitude, longitutte, passability):
        return self._is_point_available(latitude,longitutte) and (self.terrain[longitutte][latitude] <= passability)

    def _is_point_available(self,latitude, longitutte):
        return self.action_map[latitude][longitutte] == 0
    
    def clear_unit(self,latitude, longitutte):
        self.action_map[latitude][longitutte] = 0

    def _is_in_range(self,latitude, longitutte):
        return (latitude < (self.max_latitude)) & (longitutte < (self.max_longtitude))


VULNERABILITY_MAPPER = {1: 0.8, 2: 0.7, 3: 0.2}
