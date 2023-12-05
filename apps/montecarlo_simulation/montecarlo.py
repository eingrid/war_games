import numpy as np
from common.simulation import Simulation

class MonteCarlo(Simulation):
    def __init__(self,move_vest_probability_threshold=0.5):
        """init montecarlo with probabilities"""
        pass

    def select_move(self,avaliable_actions):
        if ("move_east",) in avaliable_actions:
            move_probability = np.random.rand()
            if(move_probability > 0.5):
                return ("move_east",)
            else:
                avaliable_actions.remove(("move_east",))
        generated_index = np.random.randint(0, len(avaliable_actions))
        return avaliable_actions[generated_index]
