"""CSV data is parsed here with compass headings being reversed and rotated 90 degrees.

Compass bearings start with 0 at top (typically 90) and increses in the clockwise direction."""

class Cluster:
    def __init__(self):
        self.heading: int=0
        self.speed:  int=0

    def set(self, speed, heading):
        self.speed = speed
        self.heading = heading
        
    def __str__(self) -> str:
        return f"heading: {self.heading} - speed: { self.speed }"


class ClusterPanel:

    def __init__(self):
        self.wind: Cluster = Cluster()
        self.water: Cluster = Cluster()
        self.craft: Cluster = Cluster()

    def update(self, csv_data):
        wn_speed, wn_heading, wt_speed, \
        wt_heading, ct_speed, ct_heading, \
        time= csv_data
        c = lambda x: -(x - 450) % 360
        self.wind.set(wn_speed, c(wn_heading))
        self.water.set(wt_speed, c(wt_heading))
        self.craft.set(ct_speed, c(ct_heading))
        self.time = time
        return self
    
    def __str__(self):
        return f"""
        Wind - Speed: {self.wind.speed} - Heading: {self.wind.heading}
        Water - Speed: {self.water.speed} - Heading: {self.water.heading}
        Craft - Speed: {self.craft.speed} - Heading: {self.craft.heading}
                """


