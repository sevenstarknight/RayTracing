from datetime import datetime

# ====================================================
# local imports
from src.bindings.positional.coordinates_class import LLA_Coord
from src.bindings.positional.satelliteinformation_class import SatelliteInformation
from src.bindings.positional.timeandlocation_class import TimeAndLocation
from src.positional.locationconverter_computations import convertFromECEFtoLLA
from src.positional.satellitepositiongenerator import SatellitePositionGenerator
from src.bindings.positional.satelliteinformation_class import SatelliteInformation
from src.positional.satellitepositiongenerator import SatellitePositionGenerator


def standardSatelliteInformation():

    s = '1 25544U 98067A   19343.69339541  .00001764  00000-0  38792-4 0  9991'
    t = '2 25544  51.6439 211.2001 0007417  17.6667  85.6398 15.50103472202482'
    name = "Test"

    satelliteInformation = SatelliteInformation(name=name, s=s, t=t)

    return satelliteInformation

def standardStartingPoint(satelliteInformation : SatelliteInformation):
        # Initial Starting Point
        satPosGenerator = SatellitePositionGenerator(satelliteInformation)

        currentDateTime = datetime(2012, 9, 15, 13, 14, 30)
        sat_ECEF = satPosGenerator.estimatePosition_ECEF(currentDateTime)

        # expected height, assume minimal change in position with range projection
        event_LLA = convertFromECEFtoLLA(sat_ECEF)
        event_LLA.setAltitude(0.0)

        timeAndLocation = TimeAndLocation(
            eventLocation_LLA=event_LLA, eventTime_UTC=currentDateTime)

        return timeAndLocation