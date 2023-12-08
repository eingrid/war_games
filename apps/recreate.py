import argparse
import json
import os
from utils import get_absolute_path
from common.units import *
from main import *
from visualization import *


ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


class RecreationSession(SimulationSession):
    def __init__(
        self, field_map: Map, allies: dict, enemies: dict, steps: dict, outcome: str) -> None:
        self.map = field_map
        self.allies = self.__init_units(allies)
        self.enemies = self.__init_units(enemies)
        self.num_phases = max(list(map(int, steps.keys())))
        self.steps = steps
        self.outcome = outcome

    def __init_units(self, units: list) -> list:
        """Convert units from dictionary format to MilitaryUnit object

        Args:
            units (list): Raw units in dictionary format

        Return:
            list
        """
        l = []
        for name, location in units.items():
            l.append(OBJECT_TO_CLASS_MAPPER[name[:-3]](name, *location))
        return l
    
    def run_phase(self, allies_actions, allies, enemies):
        """Units make their moves on this step"""
        if not allies_actions:
            return
        for action in allies_actions:
            unit = action['unit']
            target = action.get('target')
            destination = action.get('destination')
            if target:
                if action.get('destroyed'): 
                    target_unit = self.find_unit(enemies, target)
                    target_unit.destroyed = True
            elif destination:
                unit = self.find_unit(allies, unit)
                unit.location = destination

    def find_unit(self, units, name):
        indx = units.index(name)
        return units[indx]
    

class RecreationVisualization(Visualization):
    def run_simulation(self):
        represented = False
        while self.is_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_running = False

            if not represented:
                represented = True
                for i in range(1, self.ss.num_phases+1):
                    print(i)
                    actions = self.ss.steps[str(i)]
                    self.ss.run_phase(allies_actions=actions.get('allies'), allies=self.ss.allies, enemies=self.ss.enemies)
                    self.ss.run_phase(allies_actions=actions.get('enemies'), allies=self.ss.enemies, enemies=self.ss.allies)
                    current_map = self.ss.map
                    alive_allies, alive_enemies = self.ss._get_alive_units()
                    alies_strength = self.ss._get_unit_strength(alive_allies)
                    enemies_strength = self.ss._get_unit_strength(alive_enemies)
                    self.redraw(current_map, alive_allies, alive_enemies)
                    self._update_strength(alies_strength)
                    self._update_strength(enemies_strength,isAllies=False)

                    pygame.display.flip()
                    # Add a delay of 0.5s for visualization
                    pygame.time.wait(500)
                
                self._dispay_outcome(self.ss.outcome)
        
        pygame.quit()


def get_args():
    parser = argparse.ArgumentParser(description='Recreation of simulation')
    parser.add_argument('--file-name', 
                        type=str, 
                        default="", 
                        help='Path to file with simulation logs', 
                        dest='log_file_name')
    return parser.parse_args()

def open_file(path):
    with open(path, 'r') as file:
        content = json.load(file)
    return content


if __name__ == '__main__':
    args = get_args()
    file_name = args.log_file_name
    dict_logs = open_file(path=f"{ROOT_DIR}/history_logs/{file_name}")
    rs = RecreationSession(MAP, 
                           allies=dict_logs['allies_starting_position'],
                           enemies=dict_logs['enemies_starting_position'],
                           steps=dict_logs['buttle_phases'],
                           outcome=dict_logs['outcome'])
    visualization = RecreationVisualization(WIDTH_CELLS*18, HEIGHT_CELLS*18, session=rs)  # Set your desired window size
    visualization.run_simulation()
    