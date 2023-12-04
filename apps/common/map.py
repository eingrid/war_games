import noise
import numpy as np
from enums import Cell


class Field:
    def __init__(self, vulnerability) -> None:
        self.vulnerability = vulnerability

    def get_vulnerability(self):
        return VULNERABILITY_MAPPER[self.vulnerability]


class Map:
    def __init__(self, terrain: np.array = None) -> None:
        """Map object that is created using perlin noise"""
        self.max_longtitude, self.max_latitude = terrain.shape
        # self.terrain = self.__convert_to_np_map(terrain)
        self.noise_cell_mapping = {
            (0.0, 0.05): Cell.TREE.value["value"],
            (0.0, 0.1): Cell.HILL.value["value"],
            (0.0, 0.1): Cell.MOUNTAIN.value["value"],
        }
        self.terrain = self._generate_map_using_perlin_noise()

    def _generate_map_using_perlin_noise(self) -> np.array:
        """Generate map using perlin noise

        returns 2d matrix with int numbers.
        """

        terrain = np.zeros((self.max_longtitude, self.max_latitude))

        # mapping between perlin noise and type of the cell

        for x in range(self.max_longtitude):
            for y in range(self.max_latitude):
                noise_value = noise.snoise2(x / 10, y / 10, octaves=6)
                terrain[x, y] = self._map_noise_to_cell(noise_value)

        return terrain

    def _map_noise_to_cell(self, noise_value):
        """Map noise to type of the cell"""

        for noise_range, cell_value in self.noise_cell_mapping.items():
            if noise_range[0] <= noise_value < noise_range[1]:
                return cell_value

        return Cell.EMPTY.value["value"]


VULNERABILITY_MAPPER = {1: 0.8, 2: 0.7, 3: 0.2}
