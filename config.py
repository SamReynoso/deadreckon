from deadreckon.coordhandlers import from_coord_string


DEBUG = True
if DEBUG:
    ELAPSE = 3_600
    PAUSE = 1.5
elif DEBUG is False:
    ELAPSE = 600
    PAUSE = .5


STOP_AT_COMPLETION = True
WITHIN_TARGET = 1_000

class Case:
    one = "40°43'32\" N 50°56'49\" W", "41°43'32\" N 49°56'49\" W"
    two = "41°43'32\" N 49°56'49\" W", "40°43'32\" N 50°56'49\" W"
    three = "41°43'32\" N 50°56'49\" W", "40°43'32\" N 49°56'49\" W"
    four = "40°43'32\" N 49°56'49\" W", "41°43'32\" N 50°56'49\" W"

BEGINNING, END = Case().one
ORIGIN = from_coord_string(BEGINNING)
DESTINATION = from_coord_string(END)

CRAFT_SPEED = 3
LIMIT= 200
