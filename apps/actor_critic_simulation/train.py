from real_model import Agent
from utils import plotLearning
import numpy as np
from real_environment import Environment




if __name__ == '__main__':
    agent = Agent(alpha=0.00001, beta=0.00005)

    env = Environment(10)
    score_history = []
    num_episodes = 2000

    for i in range(num_episodes):
        done = False
        score = 0 
        observation = env.reset()
        while not done:
            action = agent.choose_action(observation)
            observation_, reward, done = env.step(action,number_of_units=3,number_of_actions_per_unit=5)
            agent.learn(observation, action, reward, observation_, done)
            observation = observation_
            score += reward

        score_history.append(score)
        avg_score = np.mean(score_history[-100:])
        print('episode: ', i,'score: %.2f' % score,
              'avg score %.2f' % avg_score)

    filename = 'LunarLander.png'
    plotLearning(score_history, filename=filename, window=100)