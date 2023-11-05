from units import MilitaryUnit


class Action:
    def __init__(self, unit: MilitaryUnit) -> None:
        self.unit = unit
        self.phase_number = None


class Move(Action):
    def __init__(self, unit: MilitaryUnit) -> None:
        self.start = unit._get_location()
        self.destination = None
        super().__init__(unit)

    def set_destination_location(self, *location):
        self.destination = location

    def get_destination_location(self):
        return self.destination
    
    location = property(get_destination_location, set_destination_location)


class Attack(Action):
    def __init__(self, unit: MilitaryUnit, target: MilitaryUnit, target_destroyed: bool) -> None:
        self.destroyed = target_destroyed
        self.target = target
        super().__init__(unit)
