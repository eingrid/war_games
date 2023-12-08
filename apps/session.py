import json
import random
import os

import numpy as np
from utils import OUTCOMES, get_absolute_path
from logger import Attack, Move
from datetime import datetime
from collections import Counter

from common.map import Map
from common.units import OBJECT_TO_CLASS_MAPPER, UNIT_FIGHTING_IMPACT, Artillery
from montecarlo_simulation.montecarlo import MonteCarlo
from uniform_simulation.uniform import Uniform


import sys



ALLIES = json.load(open(get_absolute_path("/input/allies.json"), "r")).get("forces")
ENEMIES = json.load(open(get_absolute_path("/input/enemies.json"), "r")).get("forces")

from common.units import OBJECT_TO_INT_CLASS_MAPPER

class SimulationSession:
    def __init__(
        self,
        map: Map,
        allies: dict,
        enemies: dict,
        min_confidence_threshold=0.5,
        simulation=Uniform(),
    ) -> None:
        self.map = map
        self.min_confidence_threshold = min_confidence_threshold
        self.initial_allies_dict = allies
        self.initial_enemies_dict = enemies
        self.allies = self.__init_units(allies)
        self.enemies = self.__init_units(self.__filter_units(enemies))
        self.step = 0
        self.logs = {

            "allies_starting_position": {
                ally.name: ally._get_location() for ally in self.allies
            },
            "enemies_starting_position": {
                enemy.name: enemy._get_location() for enemy in self.enemies
            },
            "buttle_phases": {},

        }
        self.reward = 0
        self.dead_allies = []
        self.dead_enemies = []
        self.__init_action_map()

        # class that returns next step for units

        self.simulation = simulation

    def reset(self):
        self.map = self.map
        self.allies = self.__init_units(self.initial_allies_dict)
        self.enemies = self.__init_units(self.__filter_units(self.initial_enemies_dict))
        self.step = 0
        self.logs = {

            "allies_starting_position": {
                ally.name: ally._get_location() for ally in self.allies
            },
            "enemies_starting_position": {
                enemy.name: enemy._get_location() for enemy in self.enemies
            },
            "buttle_phases": {},

        }
        self.reward = 0
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
        return list(
            filter(
                lambda unit: unit["object_confidence"] > self.min_confidence_threshold,
                units,
            )
        )

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
        return list(
            map(
                lambda pair: OBJECT_TO_CLASS_MAPPER[pair[0]["object_name"]](
                    name=f"{pair[0]['object_name']}{pair[1]}", **pair[0]["location"]
                ),
                zip(units, random_ids),
            )
        )


    def __init_action_map(self):
        for allies_unit in self.allies:
            self.map.update_action_map(allies_unit.latitude, allies_unit.longtitude, 1)
        for enemy_unit in self.enemies:
            self.map.update_action_map(enemy_unit.latitude, enemy_unit.longtitude, 2)

    def __make_moves(self, allies, enemies, disable,can_move):
        logs = []
        allies.sort(key=lambda x: x.longtitude, reverse=True)
        leader_move=None
        for allies_unit in allies:
            available_actions = allies_unit._get_available_actions(allies, enemies, self.map, can_move)
            if(len(available_actions) == 0):
                continue
            
            # select move
            # TODO: waiting for feedback regarding unit moves unification
            if leader_move in available_actions:
                action = leader_move
            else:
                action = self.simulation.select_move(available_actions)

            if "move" in action[0]:
                log = Move(allies_unit)
                self.map.clear_unit(allies_unit.latitude,allies_unit.longtitude)
                allies_unit.move(action[0])
                if leader_move==None:
                    leader_move=action
                self.map.update_action_map(allies_unit.latitude, allies_unit.longtitude, 1)

                log.destination = allies_unit._get_location()
                log.phase_number = self.step
            elif action[0] == "attack":
                reachable_targets = action[1]
                selected_target, is_target_destroyed = allies_unit.attack(
                    reachable_targets
                )
                log = Attack(allies_unit, selected_target, is_target_destroyed)
                log.phase_number = self.step
                if is_target_destroyed:

                    self.map.clear_unit(selected_target.latitude, selected_target.longtitude)
                    self.__getattribute__(f"dead_{disable}").append(selected_target)
            elif action[0] == 'follow_vehicle':
                allies_unit._follow_wehicle(action[1])
            elif action[0] == 'leave_vehicle':
                allies_unit._leave_vehicle()
            logs.append(log._to_dict())
            print
        return logs

    def _get_alive_units(self):
        not_destroyed = lambda unit: not unit.destroyed
        alive_allies = list(filter(not_destroyed, self.allies))
        alive_enemies = list(filter(not_destroyed, self.enemies))
        return alive_allies, alive_enemies

    def _get_unit_strength(self, units_left) -> float:
        return sum([UNIT_FIGHTING_IMPACT[type(unit)] for unit in units_left])

    
    def run_phase(self):
        """Units make their moves on this step"""
        self.logs['buttle_phases'][self.step] = {}
        alive_allies, alive_enemies = self._get_alive_units()
        # alies make their move
        allies_logs = self.__make_moves(alive_allies, alive_enemies, disable='enemies', can_move=True)
        self.logs['buttle_phases'][self.step]['allies'] = allies_logs
        alive_allies, alive_enemies = self._get_alive_units()
        if(all(isinstance(unit, Artillery) for unit in alive_allies)):
            return f"Retreat"
        if len(alive_enemies) == 0:
            return f"Victory"
        
        alive_allies, alive_enemies = self._get_alive_units()
        # enemies make their move

        enemies_logs = self.__make_moves(alive_enemies, alive_allies, disable='allies', can_move=False)
        self.logs['buttle_phases'][self.step]['enemies'] = enemies_logs
        alive_allies, alive_enemies = self._get_alive_units()
        if len(alive_allies) == 0:
            return f"Defeat"
        return True

    def run_actor_critic_phase(self):
        """Runs actor critic"""
        ss, status = self.simulation.perform_step(ss=self)
        self.allies = ss.allies
        self.enemies = ss.enemies
        return ss, status

    def run_q_learning_agent(self):
        """Runs actor critic"""
        ss, status = self.simulation.perform_step(ss=self)
        self.allies = ss.allies
        self.enemies = ss.enemies
        return ss, status

    def run(self):
        """Start simulation process as a loop of phases"""
        outcome = True

        while outcome not in OUTCOMES:
            self.step += 1
            outcome = self.run_phase()
        self._save_logs_to_json()
        print(self.step)
        return self.logs
        
    def _save_logs_to_json(self, outcome):
        time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        teams = '_'.join([f"{class_name.lower()}-{amount}" for class_name, amount in Counter(obj.__class__.__name__ for obj in self.enemies).items()])
        logs = {
            'allies_starting_position': self.logs['allies_starting_position'],
            'enemies_starting_position': self.logs['enemies_starting_position'],
            'buttle_phases': self.logs['buttle_phases'],
            'score': self.reward,
            'outcome': outcome
            }
        file_path = get_absolute_path(f"/history_logs/{self.simulation.__class__.__name__}/{self.reward}__{time}__{teams}.json")
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w") as outfile:
            json.dump(logs, outfile)

if __name__ == '__main__':
    ss = SimulationSession(Map(frontline_longtitude=18, terrain=np.ones(shape=(20,20))), allies=ALLIES, enemies=ENEMIES, simulation= Uniform() )
    simulation_result = ss.run()
    print(simulation_result)
