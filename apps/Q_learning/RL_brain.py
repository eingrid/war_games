import numpy as np
import pandas as pd

from actor_critic_simulation.real_environment import Environment


class QLearningTable:
    def __init__(
        self,
        actions,
        learning_rate=0.01,
        reward_decay=0.9,
        e_greedy=0.8,
        number_of_units=1,
        number_of_actions=5,
    ):
        self.number_of_units = number_of_units
        self.number_of_actions = number_of_actions
        self.actions = actions  # a list
        self.lr = learning_rate
        self.gamma = reward_decay
        self.epsilon = e_greedy
        self.q_table = pd.DataFrame(columns=self.actions, dtype=np.float64)

    def choose_action(self, observation):
        self.check_state_exist(observation)
        # action selection
        if np.random.uniform() < self.epsilon:
            # choose best action
            state_action = self.q_table.loc[observation, :]
            # some actions may have the same value, randomly choose on in these actions
            action = np.random.choice(
                state_action[state_action == np.max(state_action)].index
            )
        else:
            # choose random action
            action = np.random.choice(self.actions)
        return action

    def learn(self, s, a, r, s_, done):
        self.check_state_exist(s_)
        q_predict = self.q_table.loc[s, a]
        if not done:
            q_target = (
                r + self.gamma * self.q_table.loc[s_, :].max()
            )  # next state is not terminal
        else:
            q_target = r  # next state is terminal
        self.q_table.loc[s, a] += self.lr * (q_target - q_predict)  # update

    def check_state_exist(self, state):
        if state not in self.q_table.index:
            # append new state to q table
            self.q_table = self.q_table.append(
                pd.Series(
                    [0] * len(self.actions),
                    index=self.q_table.columns,
                    name=state,
                )
            )

    def perform_step(self, ss):
        """Performs step for simulation"""
        env = Environment.from_simulation_session(ss)
        env.time = ss.step
        observation = env.get_state()
        action = self.choose_action(str(observation))
        action = int(action)
        for ally in env.ss.allies:
            print(ally.latitude, ally.longtitude)
        print("perform_step", self.number_of_units)
        state, reward, done, status_of_game = env.step(
            action,
            number_of_units=self.number_of_units,
            number_of_actions_per_unit=self.number_of_actions,
        )

        print("AFTER STEP")
        for ally in env.ss.allies:
            print(ally.latitude, ally.longtitude)

        alive_allies, alive_enemies = env.ss._get_alive_units()
        print(alive_allies, alive_enemies)

        print("Status ", status_of_game)
        status = "Proceeding"
        if status_of_game == 1:
            status = "Victory"
        elif status_of_game == -1:
            status = "Defeat"
        return env.ss, status
