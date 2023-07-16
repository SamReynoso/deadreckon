from mock_data.mock import Mock
from deadreckon.gps import GPS
from cli import cli
import config

from matplotlib import pyplot as plt
import numpy as np

def pretty(location):
    lat, long = [np.round(val / 3_600, 2) for val in location]
    return lat, long

class Locals:
    def __init__(self, coord_pair):
        self.lat = coord_pair[0]
        self.long = coord_pair[1]

    def plot(self, x: list, y:list) -> tuple[list]:
        if config.DEBUG:
            x.append(self.lat)
            y.append(self.long)
            return x, y 
        c = lambda x: x / 3_600
        x.append(c(self.long))
        y.append(c(self.lat))
        return x, y


def plot(gps: GPS):

    plt.ion()
    plt.gca().set_aspect('equal')
    plt.title('Path to Titanic')
    vectors = gps.vectors
    target = vectors[0]
    x,y = target.plot()
    plt.plot(x,y,"--r")

    if not config.DEBUG:
        x, y = Locals(gps.origin).plot([],[])
        x, y = Locals(gps.destination).plot(x, y)
        plt.plot(x, y, "--b")
        x, y = Locals(gps.location).plot([],[])
        plt.scatter(x, y)
    for vector in vectors[1:]:
        x,y = vector.plot()
        plt.plot(x,y)

    delay = config.PAUSE
    plt.pause(delay)
    plt.cla()
    

def main():
        cli.clear()
        origin, destination, craft_speed, limit, selection = cli.run()
        suc = False
        if selection == "r":
            cli.clear()
            gps = GPS(origin, destination, craft_speed)
            for i in range(limit):
                cli.readout.status(i)
                gps.main()
                gps.save_csv()
                plot(gps)
                if gps.deadreckon.vectors.target.mag < 1_000:
                    suc = True
                    if config.STOP_AT_COMPLETION:
                        break
                MOCK.next()
                cli.clear()
            if suc:
                cli.success()
        cli.clear()


if __name__ == "__main__":
    MOCK = Mock()
    MOCK.set_defaults()
    main()