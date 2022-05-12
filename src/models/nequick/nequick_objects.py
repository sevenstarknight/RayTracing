from aux import *
import numpy as np


class NEQTime:
    def __init__(self, mth, universal_time):
        self.mth = int(mth)  # {01, 02, 03 ... 11, 12}
        self.universal_time = universal_time  # hours and decimals

    def __hash__(self):
        return hash((self.mth, self.universal_time))

    def __eq__(self, other):
        return (self.mth, self.universal_time) == (other.mth, other.universal_time)


class Position:
    def __init__(self, latitude, longitude):
        self.latitude = latitude  # degrees
        self.longitude = longitude  # degrees

    def __hash__(self):
        return hash((int(self.latitude), int(self.longitude)/2))

    def __eq__(self, other):
        # arbitrary design decision: decimal places in position have no significance
        return (int(self.latitude), int(self.longitude)/2) == (int(other.latitude), int(other.longitude)/2)


class GalileoBroadcast:
    def __init__(self, ai0, ai1, ai2):
        self.ai0 = ai0
        self.ai1 = ai1
        self.ai2 = ai2