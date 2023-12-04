import pygame
from session import SimulationSession
from common.map import Map 
from enums import Cell, TroopImage

CELL_SIZE = 18

class Visualization:
    def __init__(self, width, height,session : SimulationSession):
        pygame.init()
        self.ss = session
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Monte Carlo Simulation Visualization')
        self.clock = pygame.time.Clock()
        self.is_running = True

    def redraw(self,map : Map,allies,enemies):
        terrain = map.terrain
        img = pygame.image.load("textures/EMPTY_TEX.png")
        self.screen.blit(img, (100, 100)) 
        for x in range(terrain.shape[0]):
            for y in range(terrain.shape[1]):
                cell_type_value = terrain[x,y]

                for cell in Cell:
                    if cell.value["value"] == cell_type_value:
                        self.screen.blit(cell.value["image"], (x * CELL_SIZE, y * CELL_SIZE))
                        break

        # Draw troops on the grid
        for ally in allies:
            for troop in TroopImage:
                
                if troop.value["name"] in ally.name:
                    self.screen.blit(troop.value['image'], (ally.latitude * CELL_SIZE, ally.longtitude * CELL_SIZE))

        for enemy in enemies:
            for troop in TroopImage:
                if troop.value["name"] in enemy.name:
                    self.screen.blit(pygame.transform.flip(troop.value['image'], True, False), (enemy.latitude * CELL_SIZE, enemy.longtitude * CELL_SIZE))

        pygame.display.flip()

    def run_simulation(self, type):
        outcome = True

        if type == 'MonteCarlo':
            while outcome not in {"Victory", "Defeat"}:
                self.ss.step += 1
                outcome = self.ss.run_phase()
                current_map = self.ss.map
                alive_allies,alive_enemies = self.ss._get_alive_units()
                self.redraw(current_map,alive_allies,alive_enemies)

                # Add a delay of 1 for visualization
                pygame.time.wait(1000)
                
            self.ss._save_logs_to_json()
        elif type == 'actor_critic':
            while outcome not in ("Victory","Defeat"):
                self.ss.step += 1
                ss,outcome = self.ss.run_actor_critic_phase()
                current_map = ss.map
                
                alive_allies,alive_enemies = ss._get_alive_units()
                self.redraw(current_map,alive_allies,alive_enemies)

                # Add a delay of 1 for visualization
                pygame.time.wait(1000)
        elif type == 'Q_learning':
            while outcome not in ("Victory","Defeat"):
                self.ss.step += 1
                ss,outcome = self.ss.run_q_learning_agent()
                current_map = ss.map

                alive_allies,alive_enemies = ss._get_alive_units()
                self.redraw(current_map,alive_allies,alive_enemies)

                # Add a delay of 1 for visualization
                # pygame.time.wait(1000)
                pygame.time.wait(300)
            print(outcome)
        pygame.quit()

    def simulate_and_visualize_best(self,n):
        """Run/train simulation n times and visualize best"""
        return NotImplementedError()