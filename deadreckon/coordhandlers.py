"""Converts between string format and digital format.

(Degrees North/South, Degrees East/West) <--> +-float, +-float """


def coord_parser(degree_minute_second_str: str) -> float:
    degrees, m_s = degree_minute_second_str.split("°")
    minutes, seconds_dirty = m_s.split("'")
    seconds = seconds_dirty[:-1]
    return sum([int(degrees) * 3_600, int(minutes) * 60, int(seconds)])

def coord_encoder(_seconds: float) -> str:
    _seconds = abs(_seconds)
    degrees = int(_seconds // 3_600)
    minutes = int(_seconds % 3_600 // 60)
    seconds = int(_seconds % 3_600 % 60)
    degree_minute_second_str = f"{ degrees }°{ minutes }'{seconds }\""
    return degree_minute_second_str


def from_coord_string(cooredanet_str: str):
    lat_string, north, long_string, east = cooredanet_str.split(" ")
    lat_seconds = coord_parser(lat_string)
    long_seconds = coord_parser(long_string)
    if north == "S":
        lat_seconds = 0 - lat_seconds
    if east == "W":
        long_seconds = 0 - long_seconds
    return lat_seconds, long_seconds

def gen_coord_str(location):
    lat_seconds, long_seconds = location
    if long_seconds >= 0:
        ns = "N"
    else:
        ns = "S"
    if long_seconds >= 0:
        ew = "E"
    else:
        ew = "W"
    lat_string = coord_encoder(lat_seconds)
    long_string = coord_encoder(long_seconds)
    return  f"{ lat_string } { ns } {long_string } { ew }"