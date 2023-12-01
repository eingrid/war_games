# Environment simulation
import numpy as np

class Environment:
    def __init__(self, grid_size):
        self.grid_size = grid_size
        self.unit_position = np.array([1, 1])  # Starting position of the unit
        self.enemy_position = np.array([5, 5])  # Position of the enemy
    
    def get_state(self):
        # print(np.concatenate([self.unit_position, self.enemy_position]))
        return np.concatenate([self.unit_position, self.enemy_position])
    
    def step(self, action):
        # Simulate unit movement based on the action taken
        done = False

        self._perform_step(action)
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
        elif distance < 20:
            reward = 1 / (distance + 1e-8)
        else:
            reward = -distance
        
        # Penalize going out of bounds
        if abs(self.unit_position[0]) > self.grid_size or abs(self.unit_position[1]) > self.grid_size:
            reward = -100
            done = True
        # Return the new state and reward
        return self.get_state(), reward, done

    def _perform_step(self,action_id):
        ## performs action based on it's id in env
        pass

    def reset(self):
        self.unit_position = np.array([1, 1])  # Starting position of the unit
        self.enemy_position = np.array([5, 5])  # Position of the enemy
        return self.get_state()