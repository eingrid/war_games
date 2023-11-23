import numpy as np


class MilitaryUnit:
    def __init__(
        self,
        name: str,
        longtitude: int,
        latitude: int,
        attack_range: int,
        accuracy: float,
        vulnerability: float,
    ) -> None:
        self.name = name
        self.longtitude = longtitude
        self.latitude = latitude
        self.attack_range = attack_range
        self.accuracy = accuracy
        self.vulnerability = vulnerability
        self.destroyed = False

    def __set_name__(self, owner, name):
        self.name = "_" + name

    def __get__(self, instance, owner):
        return getattr(instance, self.name)

    def __set__(self, instance, value):
        setattr(instance, self.name, value)

    def __sub__(self, instance):
        return (
            (self.latitude - instance.latitude) ** 2
            + (self.longtitude - instance.longtitude) ** 2
        ) ** 0.5

    def _get_location(self):
        return self.longtitude, self.latitude

    def _attack(self, enemies):
        reachable_targets = self.__scan_targets(enemies)
        selected_target = self.__select_target(reachable_targets)
        attack_result = self.__fire_on_positions(selected_target)
        return attack_result

    def __fire_on_positions(self, target):
        if np.random() < target.vulnerability:
            target.destroyed = True
            return target.destroyed

    def __get_euclidian_distance(self, unit):
        return (
            (self.longtitude - unit.longtitude) ** 2
            + (self.longtitude - unit.longtitude) ** 2
        ) ** 0.5

    def __scan_targets(self, enemies):
        return list(
            filter(
                lambda enemy: self.__get_euclidian_distance(self, enemy)
                <= self.attack_range,
                enemies,
            )
        )

    def __select_target(self, enemies):  # how to select target
        pass

    def _move_north(self):
        self.latitude += 1

    def _move_south(self):
        self.latitude -= 1

    def _move_west(self):
        self.longtitude -= 1

    def _move_east(self):
        self.latitude += 1


class AirForce(MilitaryUnit):
    def __init__(
        self,
        name: str,
        longtitude: int,
        latitude: int,
        altitude: int,
        attack_range: int,
        min_altitude: int,
        max_altitude: int,
        accuracy: float,
        vulnerability: float,
    ) -> None:
        self.altitude = altitude
        self.max_altitude = max_altitude
        self.min_altitude = min_altitude
        self.timeout = 0
        self.going_home = False
        self.steps_to_airport = 0
        super().__init__(
            name, longtitude, latitude, attack_range, accuracy, vulnerability
        )

    def _move_up(self, height):
        self.altitude = min(self.altitude + height, self.max_altitude)

    def _move_down(self, height):
        self.altitude = max(self.altitude - height, self.min_altitude)


class GroundForce(MilitaryUnit):
    def __init__(
        self,
        name: str,
        longtitude: int,
        latitude: int,
        attack_range: int,
        accuracy: float,
        vulnerability: float,
    ) -> None:
        # self.permeability = 1.0
        super().__init__(
            name, longtitude, latitude, attack_range, accuracy, vulnerability
        )


class ArmoredTransport(GroundForce):
    def __init__(
        self,
        name: str,
        longtitude: int,
        latitude: int,
        attack_range: int,
        accuracy: float,
        vulnerability: float,
    ) -> None:
        self.unit_slot = None
        super().__init__(
            name, longtitude, latitude, attack_range, accuracy, vulnerability
        )


class Troops(GroundForce):
    def __init__(
        self,
        name: str,
        longtitude: int,
        latitude: int,
        attack_range: int,
        accuracy: float,
        vulnerability: float,
    ) -> None:
        self.covered_by_vehicle = None
        super().__init__(
            name, longtitude, latitude, attack_range, accuracy, vulnerability
        )

    def _follow_vehicle(self, unit):
        unit.unit_slot = self
        self.covered_by_vehicle = unit

    def _leave_vehicle(self):
        vehicle = self.covered_by_vehicle
        self.covered_by_vehicle = None
        vehicle.unit_slot = None

    def _is_covered_by_vehicle(self):
        return self.covered_by_vehicle is None


class ArmoredPersonnelCarriers(ArmoredTransport):
    def __init__(self, name, longtitude, latitude) -> None:
        self.actions = ["move_north", "move_south", "move_west, move_east", "attack"]
        self.targets = [ArmoredPersonnelCarriers, Stormtrooper, MLRS]
        super().__init__(
            name,
            longtitude,
            latitude,
            attack_range=1000,
            accuracy=0.5,
            vulnerability=0.5,
        )


class Tank(ArmoredTransport):
    def __init__(self, name, longtitude, latitude) -> None:
        self.actions = ["move_north", "move_south", "move_west, move_east", "attack"]
        self.targets = [Tank, ArmoredPersonnelCarriers, Stormtrooper]
        super().__init__(
            name,
            longtitude,
            latitude,
            attack_range=1500,
            accuracy=0.5,
            vulnerability=0.5,
        )


class Stormtrooper(Troops):
    def __init__(self, name, longtitude, latitude) -> None:
        self.actions = [
            "move_north",
            "move_south",
            "move_west, move_east",
            "attack",
            "follow_vehicle",
            "leave_vehicle",
        ]
        self.targets = [MLRS, Stormtrooper, Drone]
        super().__init__(
            name,
            longtitude,
            latitude,
            attack_range=300,
            accuracy=0.5,
            vulnerability=0.5,
        )


class MLRS(Troops):
    def __init__(self, name, longtitude, latitude) -> None:
        self.actions = [
            "move_north",
            "move_south",
            "move_west, move_east",
            "attack",
            "follow_vehicle",
            "leave_vehicle",
        ]
        self.targets = [Helicopter, Tank, ArmoredPersonnelCarriers]
        super().__init__(
            name,
            longtitude,
            latitude,
            attack_range=500,
            accuracy=0.5,
            vulnerability=0.5,
        )


class Artillery(GroundForce):
    def __init__(self, name, longtitude, latitude) -> None:
        self.actions = ["attack"]
        self.targets = [Tank, ArmoredPersonnelCarriers, Stormtrooper, MLRS]
        super().__init__(
            name,
            longtitude,
            latitude,
            attack_range=2000,
            accuracy=0.5,
            vulnerability=0.2,
        )


class Bomber(AirForce):
    def __init__(self, name, longtitude, latitude) -> None:
        self.targets = [Tank, ArmoredPersonnelCarriers, Stormtrooper, MLRS]
        super().__init__(
            name,
            longtitude,
            latitude,
            altitude=0,
            attack_range=3000,
            min_altitude=25,
            max_altitude=12000,
            accuracy=0.5,
            vulnerability=0.2,
        )


class Fighter(AirForce):
    def __init__(self, name, longtitude, latitude) -> None:
        self.targets = [
            Bomber,
            Fighter,
            Helicopter,
        ]
        super().__init__(
            name,
            longtitude,
            latitude,
            altitude=0,
            attack_range=4000,
            min_altitude=50,
            max_altitude=12000,
            accuracy=0.5,
            vulnerability=0.2,
        )


class Helicopter(AirForce):
    def __init__(self, name, longtitude, latitude) -> None:
        self.targets = [Tank, ArmoredPersonnelCarriers, Helicopter]
        super().__init__(
            name,
            longtitude,
            latitude,
            altitude=0,
            attack_range=3000,
            min_altitude=10,
            max_altitude=3000,
            accuracy=0.5,
            vulnerability=0.2,
        )


class Drone(AirForce):
    def __init__(self, name, longtitude, latitude) -> None:
        self.targets = [Tank, ArmoredPersonnelCarriers, MLRS, Stormtrooper]
        super().__init__(
            name,
            longtitude,
            latitude,
            altitude=0,
            attack_range=5000,
            min_altitude=5,
            max_altitude=1000,
            accuracy=0.5,
            vulnerability=0.2,
        )


OBJECT_TO_CLASS_MAPPER = {
    "drone": Drone,
    "helicopter": Helicopter,
    "bomber": Bomber,
    "fighter": Fighter,
    "artillery": Artillery,
    "mlrs": MLRS,
    "stormtrooper": Stormtrooper,
    "tank": Tank,
    "armored_vehicle": ArmoredPersonnelCarriers,
}

tank = Tank(name="smth", longtitude=2, latitude=5)
mlrs = MLRS(name="smth", longtitude=2, latitude=5)
print(tank - mlrs)
