import pygame
from utils import get_absolute_path
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
        img = pygame.image.load(get_absolute_path("/textures/EMPTY_TEX.png"))
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
                    self.screen.blit(troop.value['image'], (ally.longtitude * CELL_SIZE, ally.latitude * CELL_SIZE))

        for enemy in enemies:
            for troop in TroopImage:
                if troop.value["name"] in enemy.name:
                    self.screen.blit(pygame.transform.flip(troop.value['image'], True, False), (enemy.longtitude * CELL_SIZE, enemy.latitude * CELL_SIZE))

        pygame.display.flip()

    def run_simulation(self):
        outcome = True
        
        
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            while outcome not in {"Victory", "Defeat"}:
                self.ss.step += 1
                outcome = self.ss.run_phase()
                current_map = self.ss.map
                alive_allies,alive_enemies = self.ss._get_alive_units()
                self.redraw(current_map,alive_allies,alive_enemies)

                # Add a delay of 0.5s for visualization
                pygame.time.wait(500)
                
            self.ss._save_logs_to_json()

        pygame.quit()

    def simulate_and_visualize_best(self,n):
        """Run/train simulation n times and visualize best"""
        return NotImplementedError()