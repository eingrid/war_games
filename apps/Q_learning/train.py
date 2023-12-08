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
from utils import get_absolute_path
from actor_critic_simulation.real_environment import Environment

#
# from maze_env import Maze
from RL_brain import QLearningTable
import pandas as pd
import numpy as np


def main_loop(env, agent, epochs, number_of_units=1, number_of_actions=5):
    rewards = []
    endings = []
    steps_per_episode = []
    training_winrate_100 = []
    training_steps_100 = []
    training_reward_100 = []

    starting_lr = agent.lr
    for episode in tqdm(range(1, epochs)):
        steps = 1
        # initial observation
        observation = env.reset()
        reward_episode = []
        if episode % 1000:
            if agent.lr == 0.01:
                agent.lr == 0.1
            else:
                agent.lr = 0.01
        # if episode > 1250:
        #     env.epsilon = 0.6
        #     # agent.epsilon = 0.6
        # if episode > 10_000:
        #     env.epsilon = 0.8
        #     # agent.epsilon = 0.8
        # if episode > 20_000:
        #     env.epsilon = 0.9
        # agent.epsilon = 0.9
        while True:
            # fresh env
            # env.render()

            # RL choose action based on observation
            action = agent.choose_action(str(observation))

            # RL take action and get next observation and reward
            # action,number_of_units,number_of_actions_per_unit=5
            observation_, reward, done, ending = env.step(
                int(action),
                number_of_units=number_of_units,
                number_of_actions_per_unit=number_of_actions,
            )
            reward_episode.append(reward)
            # RL learn from this transition

            agent.learn(str(observation), action, reward, str(observation_), done)

            # swap observation
            observation = observation_

            # break while loop when end of this episode
            if done:
                steps_per_episode.append(steps)
                endings.append(ending)
                rewards.append(np.mean(reward_episode))
                break
            steps += 1

        if episode % 100 == 0:
            training_steps_100.append(np.array(steps_per_episode)[-100:].mean())
            training_winrate_100.append((np.array(endings)[-100:] == 1).sum())
            training_reward_100.append(np.mean(rewards[-100:]))
            pd.DataFrame(
                {
                    "episode": list(range(0, episode)),
                    "average_steps": steps_per_episode,
                    "average_reward": endings,
                    "average_winrate": rewards,
                }
            ).to_csv("train_metrics.csv")

            print(
                "Win rate",
                (np.array(endings)[-100:] == 1).sum(),
                f"Reward : {np.mean(rewards[-100:])}",
            )

        if episode % 500 == 0:
            agent.q_table.to_csv("trained_agent.csv")

    endings = np.array(endings)

    del env
    # env.destroy()
    return agent


if __name__ == "__main__":
    env = Environment()
    n_actions = 5
    n_units = 5
    RL = QLearningTable(
        actions=list(range(n_actions**n_units)),
        e_greedy=1,
        number_of_units=n_units,
        learning_rate=0.1,
        reward_decay=1,
    )
    agent = main_loop(env, RL, epochs=10000 * 10**3, number_of_units=n_units)
    agent.q_table.to_csv("trained_agent.csv")
