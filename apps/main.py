from visualization import Visualization
from common.map import Map
from session import SimulationSession
from uniform_simulation.uniform import Uniform
import json
import numpy as np

ALLIES = json.load(open("input/allies.json", "r")).get("forces")
ENEMIES = json.load(open("input/enemies.json", "r")).get("forces")
WIDTH_CELLS = 50
HEIGHT_CELLS = 50 


if __name__ == "__main__":
    ss = SimulationSession(
    Map(terrain=np.ones(shape=(WIDTH_CELLS, HEIGHT_CELLS))), allies=ALLIES, enemies=ENEMIES, simulation= Uniform())
    visualization = Visualization(WIDTH_CELLS*18, HEIGHT_CELLS*18, session=ss )  # Set your desired window size
    visualization.run_simulation()