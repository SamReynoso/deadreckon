
"""Data from the clusterpanel is used to calculate drift and compensatory craft heading"""


import numpy as np
import copy
from deadreckon.clusterpanel import ClusterPanel
from deadreckon.vector import Vector
import config
from cli import cli


class DeadReckon:
    time = 0

    def update(self, craft_speed, target_mag ,target_heading):
        self.craft_speed = craft_speed
        self.target = Vector(name="target").from_degrees(target_mag, target_heading)

    def run(self, clusterpanel: ClusterPanel):
        time_delta = clusterpanel.time - self.time
        self.time  = clusterpanel.time
        craft_mag = self.craft_speed * time_delta
        self.vectors = VectorHandler(self.target)
        self.vectors.update(clusterpanel, time_delta)
        self.vectors.find_crosswind()
        self.vectors.gen_windtravel()
        self.vectors.gen_drift()
        self.vectors.gen_craft(craft_mag)
        return self
    
    def fetch(self):
        if config.DEBUG:
            return [
                self.vectors.target,
                self.vectors.wind, self.vectors.water,
                self.vectors.crosswind, 
                self.vectors.windtravel,
                self.vectors.drift,
                self.vectors.craft
            ]
        return[
            self.vectors.target, self.vectors.wind,
            self.vectors.water, self.vectors.windtravel,
            self.vectors.craft
        ]
 
class VectorHandler:
    def __init__(self, target: Vector):
        self.target = target

    def update(self, clusterpanel: ClusterPanel, time_delta: int):
        self.wind: Vector = Vector(name="wind").from_cluster(clusterpanel.wind, time_delta)
        self.water: Vector = Vector(name="water").from_cluster(clusterpanel.water, time_delta)
        
    def copy(self, vector: Vector, name="None"):
        vector_copy = copy.deepcopy(vector)
        vector_copy.name = name
        return vector_copy

    def find_crosswind(self):
        wn = self.wind
        tar = self.target
        if wn.mag != 0 and tar.mag != 0:
            dot = np.dot(wn.function(), tar.function())
            scale = dot / tar.mag
            projection = [ (point / tar.mag) * scale for point in tar.function() ]
            self.crosswind = Vector(name="crosswind").from_point(
                tuple(np.subtract(wn.function(), projection))
            )
        else:
            self.crosswind = Vector(name="crosswind")
    
    def gen_windtravel(self):
        self.windtravel = self.copy(self.crosswind, name="windtravel")
        self.windtravel.line_from(self.water._to)

    def gen_drift(self):
        trav = self.windtravel
        tar = self.target
        dot = np.dot(trav.function(), tar.function())
        scale = dot / self.target.mag
        projection = [ (point / tar.mag) * scale for point in tar.function() ]
        self.drift = Vector(name="drift").from_point(
            tuple(np.subtract(trav.function(), projection))
        )

    def gen_craft(self, craft_mag):
        if craft_mag == 0:
            self.craft = Vector(name="craft")
            thetaA = 0
        else:    
            if self.drift.mag > craft_mag:
                    cli.readout.unreachable()
                    craft_theta = self.target.theta
                    thetaA = 0
            else:
                thetaA = np.arccos(self.drift.mag/craft_mag)
                handedness = ((self.target.theta - self.drift.theta) % (2*np.pi)) / (np.pi/2)
                if handedness < 0 or handedness > 2:
                    craft_theta = self.drift.theta - (np.pi - thetaA)
                else:
                    craft_theta = self.drift.theta + (np.pi - thetaA)
            self.craft = Vector(name="craft").from_theta(craft_mag, craft_theta)
            self.craft.line_from(self.windtravel._to)

        if config.DEBUG:
            cli.readout.craft_info(
                self.target,
                Vector(name="travel").from_point(self.windtravel._to), 
                self.drift,
                thetaA,
                self.craft
                )


