# from common.simulation import Simulation
import numpy as np
import sys
from real_model import Agent
from real_environment import Environment


class ActorCritic:
    def __init__(self):
        self.agent = Agent(0.1, 0.1)
        self.agent.load_models(
            "actor_critic_simulation/model_weights/actor.h5",
            "actor_critic_simulation/model_weights/critic.h5",
        )

    def perform_step(self, ss):
        """Performs step for simulation"""
        env = Environment.from_simulation_session(ss)
        observation = env.get_state()
        action = self.agent.choose_action(observation)
        for ally in env.ss.allies:
            print(ally.latitude, ally.longtitude)
        state, reward, done, status_of_game = env.step(
            action, number_of_units=1, number_of_actions_per_unit=5
        )

        print("AFTER STEP")
        for ally in env.ss.allies:
            print(ally.latitude, ally.longtitude)

        status = "Proceeding"
        if status_of_game == 1:
            status = "Victory"
        elif status_of_game == -1:
            status = "Defeat"
        return env.ss, status
