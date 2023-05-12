from dataclasses import dataclass
from datetime import datetime
# ====================================================
# local imports
from src.bindings.positional.coordinates_class import LLA_Coord

@dataclass
class TimeAndLocation():
    eventTime_UTC : datetime
    eventLocation_LLA : LLA_Coord