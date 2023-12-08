from common.units import MilitaryUnit


class Action:
    def __init__(self, unit: MilitaryUnit) -> None:
        self.unit = unit
        self.phase_number = None

    def _to_dict(self):
        raise NotImplementedError


class Move(Action):
    def __init__(self, unit: MilitaryUnit) -> None:
        self.start = unit._get_location()
        self._destination = None
        super().__init__(unit)

    def set_destination_location(self, location):
        self._destination = location

    def get_destination_location(self):
        return self._destination

    def _to_dict(self):
        return {
            "unit": self.unit.name,
            "start": self.start,
            "destination": self._destination,
        }

    destination = property(get_destination_location, set_destination_location)


class Attack(Action):
    def __init__(
        self, unit: MilitaryUnit, target: MilitaryUnit, target_destroyed: bool
    ) -> None:
        self.destroyed = target_destroyed
        self.target = target
        super().__init__(unit)

    def _to_dict(self):
        return {
            "unit": self.unit.name,
            "destroyed": self.destroyed,
            "target": self.target.name,
        }
