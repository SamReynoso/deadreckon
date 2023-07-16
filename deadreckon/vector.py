import numpy as np
import config
from deadreckon.clusterpanel import Cluster

def use_trig(theta):
    if theta == 0:
        x_scaler = 1
        y_scaler = 0
    else:
        x_scaler = np.cos(theta)
        y_scaler = np.sin(theta)
    return x_scaler, y_scaler

def point_mag(p: tuple):
    return np.sqrt( p[0]**2 + p[1]**2)

def degree_theta(degrees):
    return degrees * (np.pi / 180)

def point_theta(point: tuple):
    if point == (0,0):
        return 0
    theta = np.arctan2(point[1], point[0])
    return theta

class Vector:
    def __init__(self, name="None"):
        self.name = name
        self._from: tuple = 0, 0
        self._to: tuple = 0, 0

    def from_cluster(self, cluster: Cluster, time_delta):
        self.mag = cluster.speed * time_delta
        return self.from_degrees(self.mag, cluster.heading)

    def from_degrees(self, mag, degrees):
        self.mag = mag
        self.theta = degree_theta(degrees)
        x_scaler, y_scaler = use_trig(self.theta)
        self._to = (
            self.mag * x_scaler,
            self.mag * y_scaler
        )
        return self

    def from_theta(self, mag, theta):
        self.mag = mag
        self.theta = theta
        lat_scaler, long_scaler = use_trig(self.theta)
        self._to = (
            self.mag * lat_scaler,
            self.mag * long_scaler
        )
        return self

    def from_point(self, point: tuple):
        self.mag = point_mag(point)
        self.theta = point_theta(point)
        self._from = 0, 0
        self._to = point
        return self


    def function(self) -> tuple:
        return self._to[0] - self._from[0], self._to[1] - self._from[1]

    def line_from(self, new_tail: tuple):
        self._to = tuple(np.add(self.function(), new_tail))
        self._from = new_tail

    def plot(self):
        c = lambda x: x / 3_600
        lat = (c(self._from[0]), c(self._to[0]))
        long = (c(self._from[1]), c(self._to[1]))
        if config.DEBUG:
            return lat, long
        return long, lat 

    def __str__(self):
        if self.name != "None":
            string = f"Vector-'{ self.name }': { self._from } -> { self._to }\
                Theta: { self.theta } -- Mag { self.mag }"
        else:
            string = f"Vector: { self._from } -> { self._to }"
        return string
