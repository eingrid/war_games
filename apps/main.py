from montecarlo_simulation.montecarlo import MonteCarlo
from utils import get_absolute_path
from visualization import Visualization
from common.map import Map
from session import SimulationSession
import json
import numpy as np

ALLIES = json.load(open(get_absolute_path("/input/allies_q2.json"), "r")).get("forces")
ENEMIES = json.load(open(get_absolute_path("/input/enemies_q2.json"), "r")).get("forces")
WIDTH_CELLS = 20
HEIGHT_CELLS = 20 
MAP = Map(terrain=np.zeros(shape=(WIDTH_CELLS, HEIGHT_CELLS)))


if __name__ == "__main__":
    ss = SimulationSession(
        MAP, 
        allies=ALLIES, 
        enemies=ENEMIES, 
        simulation= MonteCarlo())
    visualization = Visualization(WIDTH_CELLS*18, HEIGHT_CELLS*18, session=ss )  # Set your desired window size
    # visualization.run_with_visualization()
    visualization.run_simulation(n=100, mode='q_2')