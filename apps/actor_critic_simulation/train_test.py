import sys
import os
sys.path.append("..")
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from model import Agent
from utils import plotLearning
import numpy as np
from environment import Environment
from tqdm import tqdm



if __name__ == '__main__':
    agent = Agent(alpha=0.00001, beta=0.00001)

    env = Environment(10)
    score_history = []
    num_episodes = 16_000
    wins = []

    for i in tqdm(range(num_episodes)):
        done = False
        score = 0
        observation = env.reset()
        if i > 400:
            agent.epsilon =0.25
        if i > 800:
            agent.epsilon = 0
        while not done:
            action = agent.choose_action(observation)
            observation_, reward, done, win = env.step(action)
            agent.learn(observation, action, reward, observation_, done)
            observation = observation_
            score += reward
        wins.append(win)
        score_history.append(score)
        avg_score = np.mean(score_history[-100:])

        if i % 100  == 0 :
            print(env.enemy_position, env.unit_position)
            print('episode: ', i,'score: %.2f' % score,
                  'avg score %.2f' % avg_score, f'winrate = {np.mean(wins[-100:])}')

    filename = 'LunarLander.png'
    plotLearning(score_history, filename=filename, window=100)