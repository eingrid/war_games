import sys
import os
from tqdm import tqdm
# sys.path.append("..")
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(os.path.dirname(__file__))
from train import main_loop
import multiprocessing

from actor_critic_simulation.real_environment import Environment
#
# from maze_env import Maze
from RL_brain import QLearningTable
import pandas as pd
import numpy as np

n_epochs = 5
n_actions = 5
n_units = 3
q_table = None

def train_job(idx):
    np.random.seed(idx)
    env = Environment()
    RL = QLearningTable(actions=list(range(n_actions**n_units)), e_greedy=1,number_of_units=n_units,learning_rate=0.3)
    if q_table is not None:
        RL.q_table = q_table
    agent = main_loop(env, RL, epochs=n_epochs,number_of_units=n_units)
    agent.q_table.to_csv(f'/run/media/eingrid/ec26c78b-20bc-47f1-b2d5-33a92d92c9b6/UCU/Intro to ds/apps/train_job_results/q_table{idx}.csv')
    return agent.q_table


if __name__ == '__main__':
    for i in tqdm(range(100)):
        num_processes = multiprocessing.cpu_count() - 3 # Get the number of CPU cores
        # Sample data
        ids = list(range(num_processes))
        # Create a pool of processes
        pool = multiprocessing.Pool(processes=num_processes)

        # Execute the function in parallel on the data
        results = pool.map(train_job, ids)

        # Close the pool of processes
        pool.close()
        pool.join()

        resulting_df = pd.concat(results)
        resulting_q_table = resulting_df.groupby(level=0).mean()
        resulting_q_table.to_csv(f'/run/media/eingrid/ec26c78b-20bc-47f1-b2d5-33a92d92c9b6/UCU/Intro to ds/apps/train_job_results/q_table_merged/q_table{n_epochs}.csv')
        q_table = resulting_q_table