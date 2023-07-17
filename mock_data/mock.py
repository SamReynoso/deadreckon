"""The Mock class controls the generation of mock sensor data.

Wind and water-current data (direction and speed) are simulated randomly here. 
The data is validated and then saved to CSV for use by the main program"""

import random
import config
import api

class Mock:
    class Cluster:
        heading: int=None
        speed: int=None

        def update_speed(self, val):
            if self.speed + val < 0:
                self.speed = 0
            else:
                self.speed += val

        def update_heading(self, val):
            self.heading = (self.heading + val) % 360

    def __init__(self):
        api.inits()
        self.wind = self.Cluster()
        self.water = self.Cluster()
        self.craft = self.Cluster()
        self.time: int = 0

    def set_defaults(self):
        self.wind.heading = 0
        self.wind.speed = 1
        self.water.heading = 110
        self.water.speed = 1
        self.craft.heading = 0
        self.craft.speed = 0
        api.send_instruments(self.get_row())

    def get_row(self):
        return [
            self.wind.speed, self.wind.heading,
            self.water.speed, self.water.heading,
            self.craft.speed, self.craft.heading,
            self.time
            ]

    def update_wind(self, heading: int, speed: int):
        if speed > 5:
            speed = 5
        self.wind.update_heading(heading)
        self.wind.update_speed(speed)

    def update_water(self, heading: int, speed: int):
        if speed > 5:
            speed = 5
        self.water.update_heading(heading)
        self.water.update_speed(speed)

    def next(self) -> list:
        self.time += config.ELAPSE
        self.update_wind(heading=random.randint(-1,1), speed=random.randint(-1,1))
        self.update_water(heading=random.randint(-2,2), speed=random.randint(-1,1))
        api.send_instruments(self.get_row())