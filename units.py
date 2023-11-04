class MilitaryUnit:
    def __init__(self, name: str, longtitude: int, latitude: int, max_moving_speed: int, attack_range: int) -> None:
        self.name = name
        self.max_moving_speed = max_moving_speed
        self.attack_range = attack_range
        self.longtitude = longtitude
        self.latitude = latitude

    def __set_name__(self, owner, name):
        self.name = '_' + name

    def __get__(self, instance, owner):
        return getattr(instance, self.name)

    def __set__(self, instance, value):
        setattr(instance, self.name, value) 

    def get_location(self):
        return self.longtitude, self.latitude

    def fire(self):
        raise NotImplementedError

    def move_north(self, distance):
        self.latitude += distance

    def move_south(self, distance):
        self.latitude -= distance

    def move_west(self, distance):
        self.longtitude -= distance

    def move_east(self, distance):
        self.latitude += distance


class AirForce(MilitaryUnit):
    def __init__(self, name, longtitude, latitude, altitude, max_moving_speed, attack_range, max_vertical_speed, max_altitude) -> None:
        self.altitude = altitude
        self.max_altitude = max_altitude
        self.max_vertical_speed = max_vertical_speed
        super().__init__(name=name, 
                            longtitude=longtitude, 
                            latitude=latitude, 
                            max_moving_speed=max_moving_speed, 
                            attack_range=attack_range)

    def move_up(self, height):
        self.altitude += height

    def move_down(self, height):
        self.altitude -= height

class GroundForce(MilitaryUnit):
    def __init__(self, name, longtitude, latitude, max_moving_speed, attack_range) -> None:
        super().__init__(name=name, 
                        longtitude=longtitude, 
                        latitude=latitude, 
                        max_moving_speed=max_moving_speed, 
                        attack_range=attack_range)

class Vehicle(GroundForce):
    def __init__(self, name, longtitude, latitude) -> None:
        self.targets = [Vehicle, Submachine, ManPADS]
        super().__init__(name=name, 
                        longtitude=longtitude, 
                        latitude=latitude,  
                        max_moving_speed=10,
                        attack_range=1000,)

class Tank(GroundForce):
    def __init__(self, name, longtitude, latitude) -> None:
        self.targets = [Tank, Vehicle]
        super().__init__(name=name, 
                        longtitude=longtitude, 
                        latitude=latitude,  
                        max_moving_speed=5,
                        attack_range=1500)
        
class Submachine(GroundForce):
    def __init__(self, name, longtitude, latitude) -> None:
        self.targets = [Drone, ManPADS, Submachine]
        super().__init__(name=name, 
                        longtitude=longtitude, 
                        latitude=latitude,  
                        max_moving_speed=2,
                        attack_range=300)

class ManPADS(GroundForce):
    def __init__(self, name, longtitude, latitude) -> None:
        self.targets = [Helicopter, Tank, Vehicle]
        super().__init__(name=name, 
                        longtitude=longtitude, 
                        latitude=latitude, 
                        max_moving_speed=2,
                        attack_range=500)
        
class Artillery(GroundForce):
    def __init__(self, name, longtitude, latitude) -> None:
        self.targets = [Tank, Vehicle, ManPADS, Submachine]
        super().__init__(name=name, 
                        longtitude=longtitude, 
                        latitude=latitude, 
                        range=2000, 
                        max_moving_speed=2)    

class Bomber(AirForce):
    def __init__(self, name, longtitude, latitude, altitude) -> None:
        self.targets = [Bomber, Tank, Vehicle, Helicopter]
        super().__init__(name=name, 
                        longtitude=longtitude, 
                        latitude=latitude, 
                        altitude=altitude,
                        max_moving_speed=200, 
                        max_vertical_speed=50,
                        max_altitude=7000,
                        attack_range=5000)

class Helicopter(AirForce):
    def __init__(self, name, longtitude, latitude, altitude) -> None:
        self.targets = [Helicopter, Tank, Vehicle]
        super().__init__(name=name, 
                        longtitude=longtitude, 
                        latitude=latitude,  
                        altitude=altitude,
                        max_moving_speed=50, 
                        max_vertical_speed=50,
                        max_altitude=3000,
                        attack_range=1500)
        

class Drone(AirForce):
    def __init__(self, name, longtitude, latitude, altitude) -> None:
        self.targets = [Tank, Vehicle, ManPADS, Submachine]
        super().__init__(name=name, 
                        longtitude=longtitude, 
                        latitude=latitude, 
                        altitude=altitude,
                        max_moving_speed=20,
                        max_vertical_speed=5,
                        max_altitude=1000,
                        attack_range=1500)
        