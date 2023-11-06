from map import Map
from units import OBJECT_TO_CLASS_MAPPER
from logger import Attack, Move
import json
import random

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors as c

import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

ALLIES = json.load(open(ROOT_DIR + '/input/allies.json', 'r')).get('forces')
ENEMIES = json.load(open(ROOT_DIR + '/input/enemies.json', 'r')).get('forces')

class SimulationSession:
    def __init__(self, map: Map, allies: dict, enemies: dict, min_confidence_threshold=0.5) -> None:
        self.map = map
        self.min_confidence_threshold = min_confidence_threshold
        self.allies = self.__init_units(allies)
        self.enemies = self.__init_units(self.__filter_units(enemies))
        self.step = 0
        self.logs = {}
        self.dead_allies = []
        self.dead_enemies = []
        self.__init_action_map()

    def __filter_units(self, units):
        """Filter units with detection confidence less than min confidence threshold

        Args:
            units (list): Raw units in dictionary format

        Return:
            list
        """
        return list(filter(lambda unit: unit['object_confidence'] > self.min_confidence_threshold, units))
    
    def __init_units(self, units: list) -> list:
        """Convert units from dictionary format to MilitaryUnit object

        Args: 
            units (list): Raw units in dictionary format

        Return:
            list
        """
        random_ids = random.sample(range(100, 1000), len(units))
        # unit_entities = []
        # for idx, unit in enumerate(units):
        #     unit_class = OBJECT_TO_CLASS_MAPPER[unit['object_name']]
        #     unit_entity = unit_class(name=f"{unit['object_name']}{random_id[idx]}", **unit['location'])
        #     unit_entities.append(unit_entity)
        # return unit_entities
        return list(map(lambda pair: OBJECT_TO_CLASS_MAPPER[pair[0]['object_name']](name=f"{pair[0]['object_name']}{pair[1]}", **pair[0]['location']), zip(units, random_ids)))
    
    def __init_action_map(self):
        for allies_unit in self.allies:
            self.map.update_action_map(allies_unit.latitude, allies_unit.longtitude, 1)
        for enemy_unit in self.enemies:
            self.map.update_action_map(enemy_unit.latitude, enemy_unit.longtitude, 2)

    def __make_moves(self, allies, enemies, disable,can_move):
        logs = []
        for allies_unit in allies:
            avaliable_actions = allies_unit.get_avaliable_actions(allies, enemies, self.map, can_move)
            if(len(avaliable_actions) == 0):
                continue
            generated_index = np.random.randint(0, len(avaliable_actions))
            # select move
            action = avaliable_actions[generated_index]
            if 'move' in action[0]:
                log = Move(allies_unit)
                self.map.clear_unit(allies_unit.latitude,allies_unit.longtitude)
                allies_unit.move(action[0])
                self.map.update_action_map(allies_unit.latitude, allies_unit.longtitude, 1)
                log.location = allies_unit._get_location()
                log.phase_number = self.step
            elif action[0] == 'attack':
                reachable_targets = action[1]
                selected_target, is_target_destroyed = allies_unit.attack(reachable_targets)
                log = Attack(allies_unit, selected_target, is_target_destroyed)
                log.phase_number = self.step
                if is_target_destroyed:
                    self.__getattribute__(f"dead_{disable}").append(selected_target)
            #Ignore for now
            # elif action[0] == 'follow_vehicle':
            #     allies_unit._follow_wehicle(action[1])
            # elif action[0] == 'leave_vehicle':
            #     allies_unit._leave_vehicle()
            logs.append(log)
            print
        return logs
    
    def __get_alive_units(self):
        not_destroyed = lambda unit: not unit.destroyed
        alive_allies = list(filter(not_destroyed, self.allies))
        alive_enemies = list(filter(not_destroyed, self.enemies))
        return alive_allies, alive_enemies
    
    def __run_phase(self):
        """Units make their moves on this step"""
        self.logs[self.step] = {}
        alive_allies, alive_enemies = self.__get_alive_units()
        allies_logs = self.__make_moves(alive_allies, alive_enemies, disable='enemies',can_move=True)
        self.logs[self.step]['allies'] = allies_logs
        alive_allies, alive_enemies = self.__get_alive_units()
        if len(alive_enemies) == 0:
            print ("Victory")
            return f"Victory"
        
        alive_allies, alive_enemies = self.__get_alive_units()
        enemies_logs = self.__make_moves(alive_enemies, alive_allies, disable='allies',can_move=False)
        self.logs[self.step]['enemies'] = enemies_logs
        alive_allies, alive_enemies = self.__get_alive_units()
        if len(alive_allies) == 0:
            print ("Defeat")
            return f"Defeat"
        return True
        
    def run(self):
        """Start simulation process as a loop of phases
        """
        outcome = True
        
        while outcome not in {'Victory', 'Defeat'}:
            self.plot_action_map()
            self.step += 1
            outcome = self.__run_phase()
        self._save_logs_to_json()
        print(self.step)
        plt.show()
        return self.logs
    
    def _save_logs_to_json(self):
        pass

    def plot_action_map(self):
        cMap = c.ListedColormap(['w','b', 'r'])
        plt.pcolormesh(self.map.action_map, edgecolors='k', linewidth=2,cmap=cMap)
        ax = plt.gca()
        ax.set_aspect('equal')
        # plt.show()

if __name__ == '__main__':
    ss = SimulationSession(Map(frontline_longtitude=15, terrain=np.ones(shape=(20,20))), allies=ALLIES, enemies=ENEMIES, )
    simulation_result = ss.run()
    print(simulation_result)