from map import Map
from models import OBJECT_TO_CLASS_MAPPER
from logger import Attack, Move
import json
import random

FOLDER_PATH = 'intro to ds/war_gaming/input/'

ALLIES = json.load(open(FOLDER_PATH + 'allies.json', 'r')).get('forces')
ENEMIES = json.load(open(FOLDER_PATH + 'enemies.json', 'r')).get('forces')


class SimulationSession:
    def __init__(self, map: Map, allies: dict, enemies: dict, min_confidence_threshold=0.5) -> None:
        self.map = map
        self.min_confidence_threshold = min_confidence_threshold
        self.allies = self.__init_units(allies)
        self.enemies = self.__init_units(self.__filter_units(enemies))
        self.step = 0
        self.logs = []

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

    def __filter_allowed_actions(self):
        """Filter actions that are avaliable for the unit on a current step"""
        raise NotImplementedError

    def __choose_next_action(self):
        """Select action for a user on a current step"""
        raise NotImplementedError

    def __run_phase(self):
        """Units make their moves on this step"""
        # PSEUDO CODE
        # for unit in units:
        #       filter_allowed_actions(unit)
        #       choose_next_action(unit)
        #       make_move(unit)
        raise NotImplementedError

    def run(self):
        """Start simulation process as a loop of phases
        """
        while True:
            self.step += 1
            self.__run_phase()


if __name__ == '__main__':
    ss = SimulationSession(Map(), allies=ALLIES, enemies=ENEMIES)
    ss.run()