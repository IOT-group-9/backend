from piccolo.table import Table
from piccolo.columns import Varchar, Boolean, ForeignKey, Integer

class Arduino(Table):
    ip_address = Varchar(unique=True, index=True)

class ParkingPlace(Table):
    location = Varchar()
    no_of_levels = Integer()

class Map(Table):
    parking_place = ForeignKey(references=ParkingPlace)
    level_no = Integer()
    max_x1 = Integer()
    max_y1 = Integer()
    max_x2 = Integer()
    max_y2 = Integer()

class MapSlot(Table):
    map = ForeignKey(references=Map)
    x1 = Integer()
    y1 = Integer()
    x2 = Integer()
    y2 = Integer()
    arduino = ForeignKey(references=Arduino, null=True)
    occupied = Boolean(default=False)

class Display(Table):
    connection = Varchar()  # or whatever type connection should be
    parking_place = ForeignKey(references=ParkingPlace)
