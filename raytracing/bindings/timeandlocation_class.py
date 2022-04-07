import datetime
from bindings.coordinates_class import LLA

class TimeAndLocation():
    def __init__(self, eventTime_UTC:datetime, eventLocation_LLA:LLA):
        self.eventTime_UTC = eventTime_UTC
        self.eventLocation_LLA = eventLocation_LLA