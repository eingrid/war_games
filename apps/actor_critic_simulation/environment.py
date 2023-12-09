# Environment simulation
import numpy as np


class Environment:
    def __init__(self, grid_size):
        self.grid_size = grid_size
        self.time = 0
        self.unit_position = np.array([1, 1])  # Starting position of the unit
        self.enemy_position = np.array([5, 5])  # Position of the enemy

    def get_state(self):
        # print(np.concatenate([self.unit_position, self.enemy_position]))
        return np.concatenate([self.unit_position, self.enemy_position, [self.time]])

    def step(self, action):
        # Simulate unit movement based on the action taken
        win = 0
        done = False

        if action == 0:  # Move up
            self.unit_position[0] -= 1
        elif action == 1:  # Move down
            self.unit_position[0] += 1
        elif action == 2:  # Move left
            self.unit_position[1] -= 1
        elif action == 3:  # Move right
            self.unit_position[1] += 1

        # Compute reward based on the new position (simplified reward)
        distance = np.linalg.norm(self.unit_position - self.enemy_position)
        if distance < 1e-5:
            reward = 200
            done = True
            win = 1
        elif distance < 20:
            reward = 1 / (distance + 1e-8)
        else:
            reward = -distance

        # Penalize going out of bounds
        if (
            abs(self.unit_position[0]) > self.grid_size
            or abs(self.unit_position[1]) > self.grid_size
            or min(self.unit_position[1], self.unit_position[0]) < 0
        ):
            reward = -100
            done = True

        # time
        if self.time > 20:
            # print("FINISH REASON TIME")
            done = True
            return self.get_state(), reward, done, win
        # Return the new state and reward
        self.time += 1
        return self.get_state(), reward, done, win

    def _perform_step(self, action_id):
        ## performs action based on it's id in env
        pass

    def reset(self):
        self.unit_position = np.array([1, 1])  # Starting position of the unit
        self.enemy_position = np.array([5, 5])  # Position of the enemy
        self.time = 0
        return self.get_state()
