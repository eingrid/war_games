from common.simulation import Simulation
import numpy as np


class Uniform(Simulation):
    def select_move(self, unit, allies, enemies, map):
        """Select move for unit by random"""
        avaliable_actions = unit.get_available_actions(allies, enemies, map)
        generated_index = np.random.randint(0, len(avaliable_actions))
        # select move
        action = avaliable_actions[generated_index]

        return action
