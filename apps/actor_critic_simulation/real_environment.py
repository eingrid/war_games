# Environment simulation
import numpy as np
from common.map import Map
from session import SimulationSession
from uniform_simulation.uniform import Uniform
import json
import numpy as np
from common.units import OBJECT_TO_INT_CLASS_MAPPER

ALLIES = json.load(open("/run/media/eingrid/ec26c78b-20bc-47f1-b2d5-33a92d92c9b6/UCU/Intro to ds/apps/input/allies.json", "r")).get("forces")
ENEMIES = json.load(open("/run/media/eingrid/ec26c78b-20bc-47f1-b2d5-33a92d92c9b6/UCU/Intro to ds/apps/input/enemies.json", "r")).get("forces")

WIDTH_CELLS = 20
HEIGHT_CELLS = 20 


class Environment:
    def __init__(self):
        self.time = 0 
        self.map = Map(terrain=np.ones(shape=(WIDTH_CELLS, HEIGHT_CELLS)))
        self.ss = SimulationSession(self.map, allies=ALLIES, enemies=ENEMIES, simulation= Uniform())

    @classmethod
    def from_simulation_session(cls, ss):
        environment = cls()  # Initialize an instance of Environment
        environment.ss = ss  # Assign the provided SimulationSession object to the environment's ss attribute
        return environment
        
    
    def get_state(self):
        """State is a map values and position of allies and enemies on the map"""
        terrain = self.ss.map.terrain
        allies = self.ss.allies
        enemies = self.ss.enemies
        allies_position_and_type = []
        enemies_position_and_type = [] 
        for ally in allies:
            allies_position_and_type.extend([ally.latitude, ally.longtitude,self._map_name_to_int(ally.name), int(ally.destroyed),1])

        for enemy in enemies:
            enemies_position_and_type.extend([enemy.latitude, enemy.longtitude,self._map_name_to_int(enemy.name),int(enemy.destroyed),-5])
        # state = np.concatenate([terrain.reshape(-1,),allies_position_and_type,enemies_position_and_type,[self.time]])
        state = np.concatenate([allies_position_and_type,enemies_position_and_type,[self.time]])
        # ####print(np.concatenate([self.unit_position, self.enemy_position]))
        return state #np.concatenate([self.unit_position, self.enemy_position])

    def _map_name_to_int(self, name):
        for k,v in OBJECT_TO_INT_CLASS_MAPPER.items():
            if k in name or name in k:
                return v
        raise ValueError(f"Can't map troop class to int, Troop name {name}")

    def _make_action(self,action,number_of_units,number_of_actions_per_unit):

        action = self.map_action_number_to_vector(action,number_of_units,number_of_actions_per_unit)
        done = False
        #if action was made wrong we need to penalize model, so we need reward_per_action here
        reward_per_action = 0

        unit_index = 0
        attack = 0
        
        #iterate through actions and take action for unit
        for i in range(0, len(action), number_of_actions_per_unit):
            unit_action = action[i:i + 5]
            if self.ss.allies[unit_index].destroyed == False:
                alive_allies, alive_enemies = self.ss._get_alive_units()

                avaliable_actions = self.ss.allies[unit_index].get_avaliable_actions(
                    alive_allies, alive_enemies, self.ss.map
                )
                unit_coords = np.array([self.ss.allies[unit_index].latitude,self.ss.allies[unit_index].longtitude])
                enemies_cords = np.array([[enemy.latitude,enemy.longtitude]for enemy in alive_enemies])

                min_distance_before = np.min(np.linalg.norm(unit_coords - enemies_cords,axis=1,ord=1))
                # ##print(min_distance_before)
                # ###print(avaliable_actions, self.ss.allies[unit_index].latitude, self.ss.allies[unit_index].longtitude)
                possible_actions = []
                reachable_targets = None
                for actions in avaliable_actions:
                    if len(actions) == 2 and actions[0] == 'attack':
                        ##print('attack possible')
                        reward_per_action += 1000
                        possible_actions.append('attack')
                        reachable_targets = actions[1]
                        ##print(actions)
                    else:
                        possible_actions.append(actions[0])
                # ###print(avaliable_actions)
                # ###print(possible_actions)
                # if move in available actions we perform it, else we penalize model by giving negative reward
                # ##print("Latitude: ", self.ss.allies[0].latitude, " Longtitude: ", self.ss.allies[0].longtitude )
                if unit_action == [1,0,0,0,0]:
                    # ##print('longtitude + 1')
                    if 'move_east' in possible_actions:
                        self.ss.allies[unit_index]._move_east()
                        reward_per_action += 100
                    else:
                        done = False
                        #print('wrong move')
                        reward_per_action -= 100

                elif unit_action == [0,1,0,0,0]:
                    # ##print('longtitude - 1')
                    if 'move_west' in possible_actions:
                        self.ss.allies[unit_index]._move_west()
                        reward_per_action += 100
                    else:
                        done = False
                        reward_per_action -= 100
                        #print('wrong move')

                elif unit_action == [0,0,1,0,0]:
                    # ##print('latitude + 1')
                    self.ss.allies[unit_index]._move_north()
                    if 'move_north' in possible_actions:
                        # ###print('norrth before move', self.ss.allies[unit_index].latitude,self.ss.allies[unit_index].longtitude)
                        # ###print('norrth after move', self.ss.allies[unit_index].latitude,self.ss.allies[unit_index].longtitude)
                        reward_per_action += 100
                        # ###print(self.ss.map.max_latitude,self.ss.map.max_longtitude)
                    else:
                        done = False
                        #print('wrong move')
                        reward_per_action -= 100

                elif unit_action == [0,0,0,1,0]:
                    # ##print('latitude - 1')
                    if 'move_south' in possible_actions:
                        self.ss.allies[unit_index]._move_south()
                        reward_per_action += 100
                    else:
                        done = False
                        #print('wrong move')
                        reward_per_action -= 100
                elif unit_action == [0,0,0,0,1]:
                    # attack = -10
                    ##print('attacking')
                    ##print(reachable_targets)
                    if 'attack' in possible_actions and reachable_targets is not None:
                        selected_target, is_target_destroyed = self.ss.allies[unit_index].attack(reachable_targets)
                        if is_target_destroyed:
                            self.ss.__getattribute__(f"dead_enemies").append(selected_target)
                            print('Kill')
                            alive_allies, alive_enemies = self.ss._get_alive_units()
                            ##print(alive_enemies)
                            reward_per_action += 2000
                        else:
                            reward_per_action += 500
                    else:
                        #print('wrong attack')
                        done = False
                        reward_per_action -= 1000
                unit_coords = np.array([self.ss.allies[unit_index].latitude,self.ss.allies[unit_index].longtitude])
                min_distance_after = np.min(np.linalg.norm(unit_coords - enemies_cords,axis=1,ord=1))

                if min_distance_before - min_distance_after > 0 and not done:
                    reward_per_action += 500
                elif min_distance_before - min_distance_after < 0 and not done:
                    reward_per_action -= 500

            unit_index += 1

        return reward_per_action,done
        

    def _make_enemy_action(self):
        reward_for_enemy_move = 0
        alive_allies, alive_enemies = self.ss._get_alive_units()
        for enemy in alive_enemies:
            avaliable_actions = enemy.get_avaliable_actions(
                alive_enemies, alive_allies, self.ss.map
            )
            for action in avaliable_actions:
                #allow only attack actions
                if len(action) != 2:
                    continue
                reachable_targets = action[1]
                if len(reachable_targets) == 0:
                    continue 
                
                # selected_target, is_target_destroyed = enemy.attack(reachable_targets)
                # if is_target_destroyed:
                #     self.ss.__getattribute__(f"dead_allies").append(selected_target)
                #     ###print("our ally was destroyed")
                #     reward_for_enemy_move -= 5000
                    
        return reward_for_enemy_move
        

    # TODO UPDATE ACTUAL POSITIONS           
    def step(self, action,number_of_units,number_of_actions_per_unit=5):
        reward = 0

        # reward = -self.time
        if self.time >= 30:
            ###print("Time finish")
            return self.get_state(), 0, True, 0
        # Simulate unit movement based on the action taken
        # ###print('time reward :', reward)
        # make new action and update the session
        reward_after_our_move,done = self._make_action(action,number_of_units,number_of_actions_per_unit)
        # ###print('our move reward :', reward_after_our_move)

        alive_allies, alive_enemies = self.ss._get_alive_units()

        if len(alive_enemies) == 0:
            ####print("all enemies are dead")
            done = True
            reward = reward_after_our_move + 1_000_000
            return self.get_state(), reward, done, +1
        
        reward_after_enemy_move = self._make_enemy_action()
        # ###print('enemy move reward :', reward_after_enemy_move)

        if len(alive_allies) == 0:
            ####print("all allies are dead")
            done = True
            reward += reward_after_our_move + reward_after_enemy_move - 100_000
            return self.get_state(), reward, done, -1

        reward = reward + reward_after_enemy_move + reward_after_our_move
        # ###print('total reward:', reward)
        
        # Compute reward based on the new position (simplified reward)
        # distance = np.linalg.norm(self.unit_position - self.enemy_position)
        # if distance < 1e-5:
        #     reward = 200
        #     done = True
        # elif distance < 20:
        #     reward = 1 / (distance + 1e-8)
        # else:
        #     reward = -distance
        
        # # Penalize going out of bounds
        # if abs(self.unit_position[0]) > self.grid_size or abs(self.unit_position[1]) > self.grid_size:
        #     reward = -100
        #     done = True
        # Return the new state and reward
        self.time += 1
        return self.get_state(), reward, done, 0

    def reset(self):
        self.time = 0 
        self.ss = SimulationSession(self.map, allies=ALLIES, enemies=ENEMIES, simulation= Uniform())
        return self.get_state()

    def map_action_number_to_vector(self,action_number, num_units, num_actions):
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
