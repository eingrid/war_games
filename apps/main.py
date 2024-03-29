import os
import sys

folder_name = os.path.dirname(__file__)
sys.path.append(os.path.join(folder_name, "actor_critic_simulation"))
print(sys.path)

from montecarlo_simulation.montecarlo import MonteCarlo
from utils import get_absolute_path
from visualization import Visualization
from common.map import Map
from session import SimulationSession
from actor_critic_simulation.actor_critic import ActorCritic
import json
import numpy as np
import pandas as pd

from Q_learning.RL_brain import QLearningTable
from delta_api import delta

WIDTH_CELLS = 20
HEIGHT_CELLS = 20 
MAP = Map(terrain=np.zeros(shape=(WIDTH_CELLS, HEIGHT_CELLS)))

if __name__ == "__main__":

    ss = SimulationSession(
        MAP, 
        allies=delta.allies(), 
        enemies=delta.enemy(), 
        simulation= MonteCarlo())
    visualization = Visualization(WIDTH_CELLS*18, HEIGHT_CELLS*18, session=ss )  # Set your desired window size
    # visualization.run_with_visualization()
    visualization.run_simulation(n=1, mode='q_2')




# ALLIES = json.load(open(get_absolute_path("/input/allies_q.json"), "r")).get("forces")
# ENEMIES = json.load(open(get_absolute_path("/input/enemies_q.json"), "r")).get("forces")
# WIDTH_CELLS = 20
# HEIGHT_CELLS = 20


# if __name__ == "__main__":
#     n_units = 5
#     agent = QLearningTable(
#         actions=list(range(5**n_units)), e_greedy=1, number_of_units=n_units
#     )
#     agent.q_table = pd.read_csv(get_absolute_path("/trained_agent.csv"))
#     agent.q_table = agent.q_table.set_index(agent.q_table["Unnamed: 0"])
#     agent.q_table.drop(columns=["Unnamed: 0"], inplace=True)
#     # print(agent.q_table)
#     #
#     #
#     ss = SimulationSession(
#         Map(terrain=np.zeros(shape=(WIDTH_CELLS, HEIGHT_CELLS))),
#         allies=ALLIES,
#         enemies=ENEMIES,
#         simulation=agent,
#     )
#     visualization = Visualization(
#         WIDTH_CELLS * 18, HEIGHT_CELLS * 18, session=ss
#     )  # Set your desired window size
#     visualization.run_with_visualization(type="q_learning")
