from deadreckon.coordhandlers import from_coord_string


DEBUG = False
if DEBUG:
    ELAPSE = 1200
    PAUSE = 1.5
elif not DEBUG:
    ELAPSE = 600
    PAUSE = .05

STOP_AT_COMPLETION = False

class Case:
    one = "40°43'32\" N 50°56'49\" W", "41°43'32\" N 49°56'49\" W"
    two = "41°43'32\" N 49°56'49\" W", "40°43'32\" N 50°56'49\" W"
    three = "41°43'32\" N 50°56'49\" W", "40°43'32\" N 49°56'49\" W"
    four = "40°43'32\" N 49°56'49\" W", "41°43'32\" N 50°56'49\" W"

BEGINNING, END = Case().four
ORIGIN = from_coord_string(BEGINNING)
DESTINATION = from_coord_string(END)

CRAFT_SPEED = 10
LIMIT= 1000
