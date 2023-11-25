import json
import random

import numpy as np
from logger import Attack, Move

from common.map import Map
from common.units import OBJECT_TO_CLASS_MAPPER
from montecarlo_simulation.montecarlo import MonteCarlo
from uniform_simulation.uniform import Uniform

ALLIES = json.load(open("input/allies.json", "r")).get("forces")
ENEMIES = json.load(open("input/enemies.json", "r")).get("forces")


class SimulationSession:
    def __init__(
        self, map: Map, allies: dict, enemies: dict, min_confidence_threshold=0.5, simulation = Uniform()) -> None:
        self.map = map
        self.min_confidence_threshold = min_confidence_threshold
        self.allies = self.__init_units(allies)
        self.enemies = self.__init_units(self.__filter_units(enemies))
        self.step = 0
        self.logs = {}
        self.dead_allies = []
        self.dead_enemies = []
        #class that returns next step for units 
        self.simulation = simulation

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

    def __make_moves(self, allies, enemies, disable):
        logs = []
        for allies_unit in allies:

            action = self.simulation.select_move(allies_unit,allies,enemies,self.map)
            
            if "move" in action[0]:
                log = Move(allies_unit)
                allies_unit.move(action[0])
                log.location = allies_unit._get_location()
                log.phase_number = self.step
            elif action[0] == "attack":
                reachable_targets = action[1]
                selected_target, is_target_destroyed = allies_unit.attack(
                    reachable_targets
                )
                log = Attack(allies_unit, selected_target, is_target_destroyed)
                log.phase_number = self.step
                if is_target_destroyed:
                    self.__getattribute__(f"dead_{disable}").append(selected_target)
            elif action[0] == "follow_vehicle":
                allies_unit._follow_wehicle(action[1])
            elif action[0] == "leave_vehicle":
                allies_unit._leave_vehicle()
            logs.append(log)
        return logs

    def _get_alive_units(self):
        not_destroyed = lambda unit: not unit.destroyed
        alive_allies = list(filter(not_destroyed, self.allies))
        alive_enemies = list(filter(not_destroyed, self.enemies))
        return alive_allies, alive_enemies

    def run_phase(self):
        """Units make their moves on this step"""
        print(self.step)
        self.logs[self.step] = {}
        alive_allies, alive_enemies = self._get_alive_units()
        # alies make their move
        allies_logs = self.__make_moves(alive_allies, alive_enemies, disable="enemies")
        self.logs[self.step]["allies"] = allies_logs
        alive_allies, alive_enemies = self._get_alive_units()
        
        if len(alive_enemies) == 0:
            return f"Victory"

        alive_allies, alive_enemies = self._get_alive_units()
        # enemies make their move
        enemies_logs = self.__make_moves(alive_enemies, alive_allies, disable="allies")
        self.logs[self.step]["enemies"] = enemies_logs
        alive_allies, alive_enemies = self._get_alive_units()
        if len(alive_allies) == 0:
            return f"Defeat"
        return True

    def run(self):
        """Start simulation process as a loop of phases"""
        outcome = True
        while outcome not in {"Victory", "Defeat"}:
            self.step += 1
            outcome = self.run_phase()
        self._save_logs_to_json()
        return self.logs
        

    def _save_logs_to_json(self):
        pass


if __name__ == "__main__":
    ss = SimulationSession(
        Map(terrain=np.ones(shape=(50, 50))), allies=ALLIES, enemies=ENEMIES, simulation= Uniform())
    simulation_result = ss.run()
    print(simulation_result)
