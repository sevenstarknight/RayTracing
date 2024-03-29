from datetime import datetime

# ====================================================
# https://pyproj4.github.io/pyproj/stable/
import pyproj

# ====================================================
# local imports
from src.bindings.positional.coordinates_class import LLA_Coord, ECEF_Coord
from src.bindings.positional.layer_class import Layer
from src.bindings.positional.satelliteinformation_class import SatelliteInformation
from src.bindings.positional.timeandlocation_class import TimeAndLocation
from src.positional.satellitepositiongenerator import SatellitePositionGenerator
from src.positional.slantpathgenerator import SlantPathGenerator

# ====================================================
# constants
ECEF = pyproj.Proj(proj='geocent', ellps='WGS84', datum='WGS84')
LLA = pyproj.Proj(proj='latlong', ellps='WGS84', datum='WGS84')


def satPosition() -> ECEF_Coord:
    s = '1 25544U 98067A   19343.69339541  .00001764  00000-0  38792-4 0  9991'
    t = '2 25544  51.6439 211.2001 0007417  17.6667  85.6398 15.50103472202482'
    name = "Test"

    satelliteInformation = SatelliteInformation(name=name, s=s, t=t)

    satPosGenerator = SatellitePositionGenerator(satelliteInformation)

    dateTime = datetime(2012, 9, 15, 13, 14, 30)

    testECEF = satPosGenerator.estimatePosition_ECEF(dateTime)
    return(testECEF)


def generateSlantPath() -> list[Layer]:
    event_LLA = LLA_Coord(0.0, 0.0, 0.0)

    dateTime = datetime(2012, 9, 15, 13, 14, 30)

    sat_ECEF = satPosition()

    # expected height, assume minimal change in position with range projection
    lon_deg, lat_deg, alt_m = pyproj.transform(
        ECEF, LLA, sat_ECEF.x_m, sat_ECEF.y_m, sat_ECEF.z_m, radians=False)

    event_LLA = LLA_Coord(lat_deg, lon_deg, 0.0)
    # construct the atmospheric model
    # make LLAs
    slantPathGenerator = SlantPathGenerator()
    # make LLAs
    timeAndLocation = TimeAndLocation(
        eventLocation_LLA=event_LLA, eventTime_UTC=dateTime)

    # ======================================================
    heights_m = [0, 100, 1000, 10000, 100000, 1000000]

    slantLayers : list[Layer] = slantPathGenerator.estimateSlantPath(startTimeAndLocation=timeAndLocation,
                                                     heightStratification_m=heights_m, sat_ECEF=sat_ECEF)

    return(slantLayers)
