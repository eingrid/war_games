from models import MilitaryUnit


class Action:
    def __init__(self, unit: MilitaryUnit, phase_number: int) -> None:
        self.unit = unit
        self.phase_number = phase_number


class Move(Action):
    def __init__(self, unit: MilitaryUnit, start_location: tuple, destination_location: tuple, phase_number: int) -> None:
        self.start = start_location
        self.destination = destination_location
        super().__init__(unit, phase_number)


class Attack(Action):
    def __init__(self, unit: MilitaryUnit, target: MilitaryUnit, target_destroyed: bool, phase_number: int) -> None:
        self.destroyed = target_destroyed
        self.target = target
        super().__init__(unit, phase_number)
