"""
Reinforcement learning maze example.

Red rectangle:          explorer.
Black rectangles:       hells       [reward = -1].
Yellow bin circle:      paradise    [reward = +1].
All other states:       ground      [reward = 0].

This script is the main part which controls the update method of this example.
The RL is in RL_brain.py.

View more on my tutorial page: https://morvanzhou.github.io/tutorials/
"""
import sys
import os
from tqdm import tqdm
# sys.path.append("..")
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(os.path.dirname(__file__))

from apps.actor_critic_simulation.real_environment import Environment
#
# from maze_env import Maze
from RL_brain import QLearningTable

import numpy as np


def main_loop(env, agent, epochs):
    rewards = []
    endings = []

    for episode in tqdm(range(epochs)):
        # initial observation
        observation = env.reset()
        if episode > 1250:
            agent.epsilon = 0.6
        if episode > 3000:
            agent.epsilon = 0.8
        if episode > 4000:
            agent.epsilon = 0.9
        while True:
            # fresh env
            # env.render()

            # RL choose action based on observation
            action = RL.choose_action(str(observation))

            # RL take action and get next observation and reward
            # action,number_of_units,number_of_actions_per_unit=5
            observation_, reward, done, ending = env.step(int(action),  number_of_units=1, number_of_actions_per_unit=5)

            # RL learn from this transition
            RL.learn(str(observation), action, reward, str(observation_))

            # swap observation
            observation = observation_

            # break while loop when end of this episode
            if done:
                break

        endings.append(ending)
    if episode % 100 :
        print((np.array(endings)[-100:]==1).sum())

    endings = np.array(endings)
    print(endings)
    print((endings[-100:]==1).sum())

    # end of game
    print('game over')
    del env
    # env.destroy()
    return agent


if __name__ == "__main__":
    env = Environment()
    RL = QLearningTable(actions=list(range(5)), e_greedy=0)

    agent = main_loop(env, RL, epochs=5*10**3)
    agent.q_table.to_csv("trained_agent.csv")

    # env.after(100, update)
    # env.mainloop()