import sys
import os
from tqdm import tqdm

# sys.path.append("..")
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(os.path.dirname(__file__))

from actor_critic_simulation.real_environment import Environment

#
# from maze_env import Maze
import numpy as np
from RL_brain import DeepQNetwork


def train(env, agent, epochs, number_of_units=3, number_of_actions=5):
    step = 0
    rewards = []
    endings = []
    for episode in tqdm(range(epochs)):
        # initial observation
        observation = env.reset()
        reward_episode = []
        if episode > 4000:
            agent.epsilon = 0.8
        if episode > 8000:
            agent.epsilon = 0.95

        if episode > 20000:
            agent.epsilon = 0.99

        while True:
            # fresh env
            # env.render()

            # RL choose action based on observation
            action = agent.choose_action(observation)

            # RL take action and get next observation and reward
            observation_, reward, done, ending = env.step(
                int(action),
                number_of_units=number_of_units,
                number_of_actions_per_unit=number_of_actions,
            )
            reward_episode.append(reward)

            agent.store_transition(observation, action, reward, observation_)

            if (step > 200) and (step % 5 == 0):
                agent.learn()

            # swap observation
            observation = observation_

            # break while loop when end o
            # f this episode
            if done:
                endings.append(ending)
                rewards.append(np.mean(reward_episode))
                break
            step += 1
        if episode % 100 == 0:
            print(
                "Win rate",
                (np.array(endings)[-100:] == 1).sum(),
                f"Reward : {np.mean(rewards[-100:])}",
            )

    # end of game
    print("game over")


if __name__ == "__main__":
    # maze game
    env = Environment()
    n_actions = 5
    n_units = 2
    n_features = 16
    total_actions = n_actions**n_units
    RL = DeepQNetwork(
        total_actions,
        n_features,
        learning_rate=0.01,
        reward_decay=1,
        e_greedy=0.5,
        replace_target_iter=200,
        memory_size=40000,
        batch_size=1024
        # output_graph=True
    )
    train(env, RL, 30000, n_units, n_actions)
