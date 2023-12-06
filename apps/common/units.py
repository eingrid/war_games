import numpy as np
from common.map import Map

class MilitaryUnit:
    def __init__(
        self,
        name: str,
        longtitude: int,
        latitude: int,
        altitude: int,
        attack_range: int,
        passability: float,
        min_attack_range = None
    ) -> None:
        if(passability < 0 or passability > 1):
            raise ValueError('passabiity should be between 0 and 1')
        self.name = name
        self.longtitude = longtitude
        self.latitude = latitude
        self.altitude = altitude
        self.attack_range = attack_range
        self.destroyed = False
        self.passability = passability   
        self.min_attack_range = min_attack_range if min_attack_range is not None else 0


    def __set_name__(self, name):
        self.name = "_" + name

    def __get__(self, instance):
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

    def __get_euclidian_distance(self, unit):
        return (
            (self.longtitude - unit.longtitude) ** 2
            + (self.latitude - unit.latitude) ** 2
            + (self.altitude - unit.altitude**2)
        ) ** 0.5

    def _scan_range(self, enemies):
        return list(
            filter(
                lambda enemy: self.__get_euclidian_distance(enemy) <= self.attack_range,
                enemies,
            )
        )

    def __get_targets(self):
        return list(DESTROYING_PROBABILITY[self.__class__].keys())

    def _fire(self, enemy_unit, field_coeff=1.0):
        if (
            np.random.rand()
            < DESTROYING_PROBABILITY[self.__class__][enemy_unit.__class__] * field_coeff
        ):
            enemy_unit.destroyed = True
            return True
        return False

    def _move_north(self):
        self.latitude += 1

    def _move_south(self):
        self.latitude -= 1

    def _move_west(self):
        self.longtitude -= 1

    def _move_east(self):
        self.longtitude += 1

    def _get_available_moves(self, map: Map):
        avaliable_moves = []
        if (self.longtitude < (map.frontline_longtitude - 1)) and map.can_move_to_point(self.latitude,self.longtitude + 1,self.passability):
            avaliable_moves.append(('move_east',))
        if (self.latitude < (map.max_latitude - 1)) and  map.can_move_to_point(self.latitude+1,self.longtitude,self.passability):
            avaliable_moves.append(('move_north',))
        if (self.latitude > 0) and  map.can_move_to_point(self.latitude-1,self.longtitude,self.passability):
            avaliable_moves.append(('move_south',))
        # Allow to move back if there is no other option
        if(len(avaliable_moves) == 0 and (self.longtitude != 0)):
            avaliable_moves.append(('move_west',))
        return avaliable_moves

    def _get_reachable_priority_targets(self, enemies):  # how to select target
        targets_in_range = self._scan_range(enemies)
        return list(
            filter(
                lambda unit: unit.__class__ in self.__get_targets(), targets_in_range
            )
        )

    def attack(self, reachable_targets):
        random_index = np.random.randint(0, len(reachable_targets))
        selected_target = reachable_targets[random_index]
        return selected_target, self._fire(selected_target)

    def move(self, func):
        self.__getattribute__(f"_{func}")()


class GroundForce(MilitaryUnit):
    def __init__(
        self,
        name: str,
        longtitude: int,
        latitude: int,
        altitude: int,
        attack_range: int,
        passability: float,
        min_attack_range = None
    ) -> None:
        # self.permeability = 1.0
        super().__init__(name, longtitude, latitude, altitude, attack_range,passability, min_attack_range)


class ArmoredTransport(GroundForce):
    def __init__(
        self,
        name: str,
        longtitude: int,
        latitude: int,
        altitude: int,
        attack_range: int
    ) -> None:
        self.troops_slot = None
        super().__init__(name, longtitude, latitude, altitude, attack_range,UNIT_PASSABILITY["armored_transport"])

    def get_avaliable_actions(self, allies, enemies, map, can_move):
        avaliable_moves = []
        # attack
        reachable_priority_targets = self._get_reachable_priority_targets(enemies)
        if len(reachable_priority_targets) > 0:
            avaliable_moves.append(('attack', reachable_priority_targets))
        #moves
        elif (can_move):
            avaliable_moves.extend(self._get_available_moves(map))
        return avaliable_moves

    def move(self, func):
        move_func = self.__getattribute__(f"_{func}")
        move_func()
        if self.troops_slot:
            self.troops_slot.move_func()


class ArmoredPersonnelCarriers(ArmoredTransport):
    def __init__(self, name: str, longtitude: int, latitude: int, altitude=0) -> None:
        super().__init__(name, longtitude, latitude, altitude, attack_range=1000)


class Tank(ArmoredTransport):
    def __init__(self, name: str, longtitude: int, latitude: int, altitude=0) -> None:
        super().__init__(name, 
                         longtitude, 
                         latitude,
                         altitude, 
                         attack_range=5)


class Troops(GroundForce):
    def __init__(
        self,
        name: str,
        longtitude: int,
        latitude: int,
        altitude: int,
        attack_range: int,
    ) -> None:
        self.covered_by_vehicle = None
        super().__init__(name, longtitude, latitude, altitude, attack_range,UNIT_PASSABILITY["troops"])

    def _follow_vehicle(self, unit):
        unit.troops_slot = self
        self.covered_by_vehicle = unit

    def _leave_vehicle(self):
        vehicle = self.covered_by_vehicle
        self.covered_by_vehicle = None
        vehicle.troops_slot = None

    def _is_covered_by_vehicle(self):
        return self.covered_by_vehicle is None
    
    def get_avaliable_actions(self, allies, enemies, map, can_move):
        avaliable_moves = []
        # attack
        reachable_priority_targets = self._get_reachable_priority_targets(enemies)
        if len(reachable_priority_targets) > 0:
            avaliable_moves.append(('attack', reachable_priority_targets))
        elif (can_move):
            avaliable_moves.extend(self._get_available_moves(map))
        #intereaction with armored vehicle
        if self.covered_by_vehicle:
            avaliable_moves.append(('leave_vehicle', self.covered_by_vehicle))
        elif not self.covered_by_vehicle:
            vehicles_in_same_field = list(filter(lambda unit: isinstance(unit, ArmoredTransport) and 
                                                            not unit.troops_slot and 
                                                            not unit.destroyed and 
                                                            self._get_location() == unit._get_location(), 
                                                            allies))
            if len(vehicles_in_same_field) > 0:
                avaliable_moves.append(('follow_vehicle', vehicles_in_same_field))
            #move
            avaliable_moves.extend(self._get_avaliable_moves(map))
        return avaliable_moves


class Stormtrooper(Troops):
    def __init__(self, name, longtitude, latitude, altitude=0) -> None:
        super().__init__(name, longtitude, latitude, altitude, attack_range=300)


class MLRS(Troops):
    def __init__(self, name, longtitude, latitude, altitude=0,passability=0.5) -> None:
        super().__init__(name, longtitude, latitude, altitude, attack_range=500)


class Artillery(GroundForce):
    def __init__(self, name, longtitude, latitude, altitude=0) -> None:
        super().__init__(name, 
                         longtitude, 
                         latitude, 
                         altitude,
                         attack_range=float('inf'),
                         passability=UNIT_PASSABILITY["armored_transport"],
                         min_attack_range=10)
        self.steps_from_last_shot=ARTILLERY_RECHARGE_STEPS_COUNT
        
    def get_avaliable_actions(self, allies, enemies, map, can_move):
        avaliable_moves = []

        # recharge
        if(self.steps_from_last_shot < ARTILLERY_RECHARGE_STEPS_COUNT):
            self.steps_from_last_shot += 1
            return avaliable_moves
        
        # attack
        reachable_priority_targets = self._get_reachable_priority_targets(enemies)
        if len(reachable_priority_targets) > 0:
            avaliable_moves.append(("attack", reachable_priority_targets))
            self.steps_from_last_shot = 0
        return avaliable_moves


class AirForce(MilitaryUnit):
    def __init__(
        self,
        name: str,
        longtitude: int,
        latitude: int,
        altitude: int,
        attack_range: int,
        delta_altitude: int,
        min_altitude: int,
        max_altitude: int,
    ) -> None:
        self.max_altitude = max_altitude
        self.min_altitude = min_altitude
        self.delta_altitude = delta_altitude
        self.timeout = 0
        self.going_home = False
        self.steps_to_airport = 0
        super().__init__(name, longtitude, latitude, altitude, attack_range,UNIT_PASSABILITY["air_force"])

    def _move_up(self):
        self.altitude += self.delta_altitude

    def _move_down(self):
        self.altitude -= self.delta_altitude

    def get_avaliable_actions(self, allies, enemies, map):
        avaliable_actions = []
        # attack
        reachable_priority_targets = self._get_reachable_priority_targets(enemies)
        if len(reachable_priority_targets) > 0:
            avaliable_actions.append(("attack", reachable_priority_targets))
        # moves
        avaliable_actions.extend(self._get_avaliable_moves(map))
        # increase/decrease altitude
        if self.altitude + self.delta_altitude < self.max_altitude:
            avaliable_actions.append(
                "move_up",
            )
        if self.altitude - self.delta_altitude > self.min_altitude:
            avaliable_actions.append(
                "move_up",
            )
        return avaliable_actions


class Bomber(AirForce):
    def __init__(self, name, longtitude, latitude, altitude=0) -> None:
        super().__init__(
            name,
            longtitude,
            latitude,
            altitude,
            attack_range=3000,
            min_altitude=25,
            max_altitude=12000,
        )


class Fighter(AirForce):
    def __init__(self, name, longtitude, latitude, altitude=0) -> None:
        super().__init__(
            name,
            longtitude,
            latitude,
            altitude,
            attack_range=4000,
            min_altitude=50,
            max_altitude=12000,
        )


class Helicopter(AirForce):
    def __init__(self, name, longtitude, latitude, altitude=0) -> None:
        super().__init__(
            name,
            longtitude,
            latitude,
            altitude,
            attack_range=3000,
            min_altitude=10,
            max_altitude=3000,
        )


class Drone(AirForce):
    def __init__(self, name, longtitude, latitude, altitude=0) -> None:
        super().__init__(
            name,
            longtitude,
            latitude,
            altitude,
            attack_range=5000,
            min_altitude=5,
            max_altitude=1000,
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

# simulation settings
ARTILLERY_RECHARGE_STEPS_COUNT = 4

UNIT_PASSABILITY={
    "air_force":1,
    "armored_transport":0,
    "troops":0.5
}

UNIT_FIGHTING_IMPACT={
    Artillery: 0.8,
    MLRS: 0.6,
    Stormtrooper: 0.5,
    Tank: 0.8,
}

DESTROYING_PROBABILITY = {
    Drone: {Tank: 0.0, ArmoredPersonnelCarriers: 0.0, MLRS: 0.0, Stormtrooper: 0.0},
    Helicopter: {
        Tank: 0.0,
        ArmoredPersonnelCarriers: 0.0,
        MLRS: 0.0,
        Stormtrooper: 0.0,
        Artillery: 0.0,
    },
    Fighter: {Bomber: 0.0, Fighter: 0.0, Drone: 0.0},
    Bomber: {
        Tank: 0.0,
        ArmoredPersonnelCarriers: 0.0,
        MLRS: 0.0,
        Stormtrooper: 0.0,
        Artillery: 0.0,
    },
    Artillery: {
        Tank: 0.1,
        ArmoredPersonnelCarriers: 0.1,
        MLRS: 0.2,
        Stormtrooper: 0.2,
        Artillery: 0.1,
    },
    MLRS: {
        Tank: 0.5,
        ArmoredPersonnelCarriers: 0.5,
    },
    Stormtrooper: {
        MLRS: 0.5,
        Stormtrooper: 0.5,
    },
    Tank: {
        Tank: 0.5,
        ArmoredPersonnelCarriers: 0.0,
        MLRS: 0.5,
        Stormtrooper: 0.5,
        Artillery: 0.5,
    },
    ArmoredPersonnelCarriers: {
        ArmoredPersonnelCarriers: 0.0,
        MLRS: 0.0,
        Stormtrooper: 0.0,
    },
}
