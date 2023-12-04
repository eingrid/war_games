import sys
import os
# sys.path.append("..")
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(os.path.dirname(__file__))


from real_model import Agent
from utils import plotLearning
import numpy as np
from real_environment import Environment

from tqdm import tqdm


if __name__ == '__main__':
    agent = Agent(alpha=0.0001, beta=0.0001)
    endings = []
    env = Environment()
    score_history = []
    num_episodes = 100_000

    for i in tqdm(range(num_episodes)):
        agent.epsilon = 0.1
        if i > 30_000:
            agent.epsilon = -1
        done = False
        score = 0 
        observation = env.reset()
        while not done:
            action = agent.choose_action(observation)
            observation_, reward, done, ending = env.step(action,number_of_units=1,number_of_actions_per_unit=5)
            reward = reward
            # print(observation[-10:-1] == observation_[-10:-1])
            agent.learn(observation, action, reward, observation_, done)
            observation = observation_
            score += reward

        endings.append(ending)
        score_history.append(score)
        avg_score = np.mean(score_history[-100:])
        if i%100 == 0:
            print(np.array(endings)[-100:].shape)
            print('episode: ', i,'score: %.2f' % score,
              'avg score %.2f' % avg_score, f'win/lose {(np.array(endings)[-100:]==1).sum()}/{(np.array(endings)[-100:]==-1).sum()}')
    
    agent.save_models()
    
    filename = 'LunarLander.png'
    plotLearning(score_history, filename=filename, window=100)