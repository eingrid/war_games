# Environment simulation
import numpy as np
from visualization import Visualization
from common.map import Map
from session import SimulationSession
from uniform_simulation.uniform import Uniform
import json
import numpy as np
from common.models import OBJECT_TO_INT_CLASS_MAPPER

ALLIES = json.load(open("input/allies.json", "r")).get("forces")
ENEMIES = json.load(open("input/enemies.json", "r")).get("forces")


class Environment:
    def __init__(self, grid_size):
        WIDTH_CELLS = 50
        HEIGHT_CELLS = 50 
        self.ss = SimulationSession(Map(terrain=np.ones(shape=(WIDTH_CELLS, HEIGHT_CELLS))), allies=ALLIES, enemies=ENEMIES, simulation= Uniform())
        # self.grid_size = grid_size
        # self.unit_position = np.array([1, 1])  # Starting position of the unit
        # self.enemy_position = np.array([5, 5])  # Position of the enemy
    
    def get_state(self):
        """State is a map values and position of allies and enemies on the map"""
        terrain = self.ss.map.terrain
        allies = self.ss.allies
        enemies = self.ss.enemies
        allies_position_and_type = []
        enemies_position_and_type = [] 
        for ally in allies:
            allies_position_and_type.extend([ally.latitude, ally.longtitudem,self._map_name_to_int(ally.name)])

        for enemy in enemies:
            enemies_position_and_type.extend([enemy.latitude, enemy.longtitudem,self._map_name_to_int(enemy.name)])

        state = np.concatenate(terrain.reshape(-1,),allies_position_and_type,)
        # print(np.concatenate([self.unit_position, self.enemy_position]))
        return state#np.concatenate([self.unit_position, self.enemy_position])

    def _map_name_to_int(self, name):
        for k,v in OBJECT_TO_INT_CLASS_MAPPER:
            if k in name or name in k:
                return v
        raise ValueError(f"Can't map troop class to int, Troop name {name}")

    def _make_action(self,action,number_of_units,number_of_actions_per_unit):

        alive_allies, alive_enemies = self.ss._get_alive_units()
        action = self.map_action_number_to_vector(action,number_of_units,number_of_actions_per_unit)

        #if action was made wrong we need to penalize model, so we need reward_per_action here
        reward_per_action = 0

        unit_index = 0
        #iterate through actions and take action for unit
        for i in range(0, action, number_of_actions_per_unit):
            unit_action = action[i:i + 5]
            if self.ss.allies[unit_index].alive:

                avaliable_actions = self.ss.allies[unit_index].get_avaliable_actions(
                    alive_allies, alive_enemies, self.ss.map
                )
                possible_actions = []
                reachable_targets = None
                for actions in avaliable_actions:
                    if len(actions) == 2 and actions[0] == 'attack':
                        possible_actions.append('attack')
                        reachable_targets = actions[1]
                    else:
                        possible_actions.append(action)
                        
                # if move in available actions we perform it, else we penalize model by giving negative reward
                if unit_action == [1,0,0,0,0]:
                    if 'move_east' in possible_actions:
                        self.ss.allies[unit_index]._move_east()
                    else:
                        reward_per_action -= 100
                elif unit_action == [0,1,0,0,0]:
                    if 'move_west' in possible_actions:
                        self.ss.allies[unit_index]._move_west()
                    else:
                        reward_per_action -= 100
                elif unit_action == [0,0,1,0,0]:
                    if 'move_north' in possible_actions:
                        self.ss.allies[unit_index]._move_north()
                    else:
                        reward_per_action -= 100
                elif unit_action == [0,0,0,1,0]:
                    if 'move_south' in possible_actions:
                        self.ss.allies[unit_index]._move_south()
                    else:
                        reward_per_action -= 100
                elif unit_action == [0,0,0,0,1]:
                    if 'attack' in possible_actions and reachable_targets is not None:
                        selected_target, is_target_destroyed = self.ss.allies[unit_index].attack(reachable_targets)
                        if is_target_destroyed:
                            self.ss.__getattribute__(f"dead_enemy").append(selected_target)
                            reward_per_action += 100
                    else:
                        reward_per_action -= 100
                
                
            
            unit_index += 1
        return reward_per_action
        

    def _make_enemy_action(self,)
    
    def step(self, action,number_of_units,number_of_actions_per_unit=5):
        # Simulate unit movement based on the action taken
        done = False

        # make new action and update the session
        reward_per_our_action = self._make_action(action,number_of_units,number_of_actions_per_unit)
        self._make_enemy_action()
        # if action == 0:  # Move up
        #     self.unit_position[0] -= 1
        # elif action == 1:  # Move down
        #     self.unit_position[0] += 1
        # elif action == 2:  # Move left
        #     self.unit_position[1] -= 1
        # elif action == 3:  # Move right
        #     self.unit_position[1] += 1


        
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

    def reset(self):
        self.ss = SimulationSession(Map(terrain=np.ones(shape=(WIDTH_CELLS, HEIGHT_CELLS))), allies=ALLIES, enemies=ENEMIES, simulation= Uniform())
        return self.get_state()

    def map_action_number_to_vector(action_number, num_units, num_actions):
        """Maps action number to a specific actions to take in vector form

            [1,0,0,0,0] -> unit moves east.
            [0,1,0,0,0] -> unit moves west.
            [0,0,1,0,0] -> unit moves north.
            [0,0,0,1,0] -> unit moves south.
            [0,0,0,0,1] -> unit attacks.
        """
        actions = []
        for i in range(num_units):
            unit_action = action_number % num_actions
            action_vector = [0] * num_actions
            action_vector[unit_action] = 1
            actions = action_vector + actions
            action_number //= num_actions
        return actions


    def action_mapping(self,unit_action:list):
