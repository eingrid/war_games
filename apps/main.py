from utils import get_absolute_path
from visualization import Visualization
from common.map import Map
from session import SimulationSession
from uniform_simulation.uniform import Uniform
import json
import numpy as np

ALLIES = json.load(open(get_absolute_path("/input/allies.json"), "r")).get("forces")
ENEMIES = json.load(open(get_absolute_path("/input/enemies.json"), "r")).get("forces")
WIDTH_CELLS = 20
HEIGHT_CELLS = 20 


if __name__ == "__main__":
    ss = SimulationSession(
        Map(terrain=np.zeros(shape=(WIDTH_CELLS, HEIGHT_CELLS)),frontline_longtitude=18), 
        allies=ALLIES, 
        enemies=ENEMIES, 
        simulation= Uniform())
    visualization = Visualization(WIDTH_CELLS*18, HEIGHT_CELLS*18, session=ss )  # Set your desired window size
    visualization.run_simulation()