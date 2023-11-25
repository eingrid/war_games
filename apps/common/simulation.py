from abc import ABC, abstractmethod

class Simulation(ABC):
    @abstractmethod
    def select_move(self):
        """
        Abstract method representing the logic for the selecting move in the simulation.
        This method should be implemented in subclasses.
        """
        pass