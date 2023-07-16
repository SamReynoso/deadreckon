import numpy as np
import api
from deadreckon.clusterpanel import ClusterPanel
from deadreckon.deadreckon import DeadReckon
from deadreckon.vector import Vector
from deadreckon.coordhandlers import gen_coord_str
import config

def second_to_degree(val: int):
    return val / 3_600

def degree_to_radian(degrees):
    return degrees / (180 / np.pi)

def radian_to_degree(radians):
    return (radians * (180 / np.pi) + 360) % 360

def get_meter_scaler(lat_seconds):
    radians = degree_to_radian(second_to_degree(lat_seconds))
    lat_meters_per_degree = 111_132.92 \
        - 559.82 * np.cos(2*radians) \
        + 1.175 * np.cos(4*radians) \
        - 0.002_3 * np.cos(6*radians)
    long_meters_per_degree = 111_412.84 * np.cos(radians) \
        - 93.5 * np.cos(3*radians) \
        + 0.118 * np.cos(5*radians)
    scaler_in_seconds = lambda x: 1 / (x / 3_600)
    lat_scaler = scaler_in_seconds(lat_meters_per_degree)
    long_scaler = scaler_in_seconds(long_meters_per_degree)
    return lat_scaler, long_scaler

class GPS:
    def __init__(self, origin, destination, craft_speed):
        self.origin = origin
        self.location = origin
        self.destination = destination
        self.craft_speed = craft_speed
        self.deadreckon = DeadReckon()
  
    def calc_mag(self):
        c = lambda x: degree_to_radian(second_to_degree(x))
        lat1 = c(self.location[0])
        lat2 = c(self.destination[0])
        long_delta = c(self.destination[0] - self.location[0])
        lat_delta = c(lat2 - lat1)

        a = pow(np.sin(lat_delta/2), 2) + (np.cos(lat1))*np.cos(lat2)*pow((long_delta/2),2)
        d = 2*6_371_000*np.arctan2(np.sqrt(a), np.sqrt(1-a))
        return d


    def calc_heading(self):
        c = lambda x: degree_to_radian(second_to_degree(x))
        long_delta = c( self.destination[1] - self.location[1] )
        lat1 = c( self.location[0] )
        lat2 = c( self.destination[0] )
        f1 = np.sin(long_delta) * np.cos(lat2)
        f2 = np.cos(lat1)*np.sin(lat2) - np.sin(lat1)*np.cos(lat2)*np.cos(long_delta)
        theta = np.arctan2(f1, f2)
        heading = radian_to_degree(theta)
        return heading
    
    def main(self):
        csv_data = api.fetch_instruments()
        clusterpanel = ClusterPanel().update(csv_data)
        self.deadreckon.update(self.craft_speed, self.calc_mag(), self.calc_heading())
        self.deadreckon.run(clusterpanel)
        self.vectors = self.translate()
        if not config.DEBUG:
            craft = self.vectors[-1]
            if craft.name == "craft":
                self.location = craft._to

    def translate(self) -> list[Vector]:
        vectors = self.deadreckon.fetch()
        if config.DEBUG:
            return vectors
        translated = []
        for vector in vectors:
            vector = convert(vector, self.location[1])
            vector = shift(vector, self.location)
            translated.append(vector)
        return translated

    def save_csv(self, ):
        craft_csv_data = self.craft_speed, np.round(radian_to_degree(self.vectors[-1].theta), 1)
        coord_string = gen_coord_str(self.location) 
        api.update_craft(craft_csv_data)
        api.send_coord([coord_string])



def convert(vector: Vector, lat_seconds):
    lat_scaler, long_scaler = get_meter_scaler(lat_seconds)
    converter = lambda x: (x[0] * lat_scaler, x[1] * long_scaler)
    tail = converter(vector._from)
    head = converter(vector._to)
    vector._from = tail
    vector._to = head
    return vector

def shift(vector: Vector, location):
    shift = lambda x: (x[0] + location[0], x[1] + location[1])
    tail = shift(vector._from)
    head = shift(vector._to)
    vector._from = tail
    vector._to = head
    return vector