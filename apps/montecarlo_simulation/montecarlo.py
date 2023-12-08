import numpy as np
from common.units import UNIT_FIGHTING_IMPACT
from common.simulation import Simulation


class MonteCarlo(Simulation):

    def __init__(self, move_east_probability_threshold=0.5):
        self.move_east_probability_threshold = move_east_probability_threshold
        pass

    def select_move(self, avaliable_actions):
        if ("move_east",) in avaliable_actions and len(avaliable_actions) != 1:
            move_probability = np.random.rand()
            if move_probability > self.move_east_probability_threshold:

                return ("move_east",)
            else:
                avaliable_actions.remove(("move_east",))
        generated_index = np.random.randint(0, len(avaliable_actions))
        return avaliable_actions[generated_index]
