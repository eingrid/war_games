import random
import sys
import os
from tqdm import tqdm

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(os.path.dirname(__file__))
from actor_critic_simulation.real_environment import Environment
import tensorflow as tf
import numpy as np
from collections import deque
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam

EPISODES = 1_000_00


class DQNAgent:
    def __init__(self, state_size, action_size):
        self.state_size = state_size
        self.action_size = action_size
        self.memory = deque(maxlen=40000)
        self.gamma = 1  # discount rate
        self.epsilon = 1  # exploration rate
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.7
        self.learning_rate = 0.01
        with tf.device("/GPU:0"):
            self.model = self._build_model()

    def _build_model(self):
        # Neural Net for Deep-Q learning Model
        model = Sequential()
        model.add(Dense(512, input_dim=self.state_size, activation="relu"))
        model.add(Dense(256, activation="relu"))
        model.add(Dense(128, activation="relu"))
        model.add(Dense(128, activation="relu"))
        model.add(Dense(self.action_size, activation="linear"))
        model.compile(loss="mse", optimizer=Adam(lr=self.learning_rate))
        return model

    def memorize(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def act(self, state):
        if np.random.rand() <= self.epsilon:
            return random.randrange(self.action_size)
        act_values = self.model.predict(state, verbose=None)
        return np.argmax(act_values[0])  # returns action

    def replay(self, batch_size):
        minibatch = random.sample(self.memory, batch_size)
        print("replay")
        # Initialize lists to store batch data
        states = []
        targets = []

        for state, action, reward, next_state, done in minibatch:
            target = reward
            if not done:
                target = reward + self.gamma * np.amax(
                    self.model.predict(next_state, verbose=None)[0]
                )

            # Get current target predictions
            target_f = self.model.predict(state, verbose=None)

            # Update the target for the chosen action
            target_f[0][action] = target

            # Append current state and updated target to the lists
            states.append(state)
            targets.append(target_f)

        # Convert lists to numpy arrays for batch training
        states = np.vstack(states)
        targets = np.vstack(targets)
        print(states.shape)
        # Train the model using batch data
        self.model.fit(states, targets, epochs=100, verbose=1)

        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

    def load(self, name):
        self.model.load_weights(name)

    def save(self, name):
        self.model.save_weights(name)


if __name__ == "__main__":
    env = Environment()
    state_size = 16
    n_actions = 5
    n_units = 2
    action_size = n_actions**n_units
    agent = DQNAgent(state_size, action_size)
    # agent.load("./save/cartpole-dqn.h5")
    done = False
    batch_size = 2048
    rewards = []
    endings = []

    for e in tqdm(range(EPISODES)):
        state = env.reset()
        state = np.reshape(state, [1, state_size])
        reward_episode = []
        if agent.epsilon > agent.epsilon_min and e % 100 == 1 and e > 10_000:
            agent.epsilon *= agent.epsilon_decay

        while True:
            # env.render()
            action = agent.act(state)
            next_state, reward, done, ending = env.step(
                action, number_of_units=n_units, number_of_actions_per_unit=n_actions
            )
            # reward = reward if not done else -10
            next_state = np.reshape(next_state, [1, state_size])
            agent.memorize(state, action, reward, next_state, done)
            state = next_state
            reward_episode.append(reward)
            # print(reward)
            if done:
                endings.append(ending)
                rewards.append(np.mean(reward_episode))
                # print("episode: {}/{}, score: {}, e: {:.2}"
                #   .format(e, EPISODES, time, agent.epsilon))
                break

        if len(agent.memory) > batch_size:
            agent.replay(batch_size)
        if e % 100 == 0:
            print(
                "Win rate",
                (np.array(endings)[-100:] == 1).sum(),
                f"Reward : {np.mean(rewards[-100:])}",
            )

        # if e % 10 == 0:
        #     agent.save("./save/cartpole-dqn.h5")
