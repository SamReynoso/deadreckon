
from matplotlib import pyplot as plt
import config
from deadreckon.gps import GPS


def plot_append(locations: list) -> tuple[list]:
    x = []
    y = []
    for location in locations:
        lat, long = location
        c = lambda x: x / 3_600
        x.append(c(long))
        y.append(c(lat))
    return x, y

def plotter(gps: GPS):
    plt.ion()
    plt.gca().set_aspect('equal')
    plt.title('Path to Titanic')
    if config.DEBUG is False:
        prime = [gps.origin, gps.destination]
        x, y = plot_append(prime)
        plt.plot(x, y, "--b")
        x, y = plot_append([gps.location])
        plt.scatter(x, y)
    target = gps.vectors[0]
    x,y = target.plot()
    plt.plot(x,y,"--r")
    for vector in gps.vectors[1:]:
        x,y = vector.plot()
        plt.plot(x,y)
    plt.pause(config.PAUSE)
    plt.cla()


