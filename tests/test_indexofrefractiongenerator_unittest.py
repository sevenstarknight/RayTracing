import unittest
# https://pyproj4.github.io/pyproj/stable/
import pyproj
from datetime import datetime
from raytracing.indexofrefractiongenerator import IndexOfRefractionGenerator

from raytracing.bindings import coordinates_class
from raytracing.bindings.satelliteinformation_class import SatelliteInformation
from raytracing.bindings.timeandlocation_class import TimeAndLocation
from raytracing.satellitepositiongenerator import SatellitePositionGenerator

ecef = pyproj.Proj(proj='geocent', ellps='WGS84', datum='WGS84')
lla = pyproj.Proj(proj='latlong', ellps='WGS84', datum='WGS84')

class TestIndexOfRefractionGenerator(unittest.TestCase):

    def test_IndexOfRefractionGenerator(self):

        s = '1 25544U 98067A   19343.69339541  .00001764  00000-0  38792-4 0  9991'
        t = '2 25544  51.6439 211.2001 0007417  17.6667  85.6398 15.50103472202482'
        name = "Test"

        satelliteInformation = SatelliteInformation(name=name, s=s, t=t)

        # Initial Starting Point
        satPosGenerator = SatellitePositionGenerator(satelliteInformation)
        currentDateTime = datetime(2012, 9, 15, 13, 14, 30)
        sat_ECEF = satPosGenerator.estimatePosition_ECEF(currentDateTime)

        #expected height, assume minimal change in position with range projection
        lon_deg, lat_deg, alt_m = pyproj.transform(ecef, lla, sat_ECEF.x_m, sat_ECEF.y_m, sat_ECEF.z_m, radians=False)

        event_LLA = coordinates_class.LLA(lat_deg, lon_deg, 0.0) 
        # construct the atmospheric model
        indexOfRefractionGenerator = IndexOfRefractionGenerator(frequency_hz=10e6)
        
        timeAndLocation = TimeAndLocation(eventLocation_LLA =  event_LLA, eventTime_UTC = currentDateTime)

        # ======================================================
        heights_m = [0, 100, 1000, 10000, 100000, 1000000]

        indexN = indexOfRefractionGenerator.estimateIndexN(startTimeAndLocation=timeAndLocation,
         heightStratification_m=heights_m, sat_ECEF=sat_ECEF)

        self.assertEqual(len(indexN), len(heights_m))


    def test_EstimateSlantPath(self):

        s = '1 25544U 98067A   19343.69339541  .00001764  00000-0  38792-4 0  9991'
        t = '2 25544  51.6439 211.2001 0007417  17.6667  85.6398 15.50103472202482'
        name = "Test"

        satelliteInformation = SatelliteInformation(name=name, s=s, t=t)

        # Initial Starting Point
        satPosGenerator = SatellitePositionGenerator(satelliteInformation)
        currentDateTime = datetime(2012, 9, 15, 13, 14, 30)
        sat_ECEF = satPosGenerator.estimatePosition_ECEF(currentDateTime)

        #expected height, assume minimal change in position with range projection
        lon_deg, lat_deg, alt_m = pyproj.transform(ecef, lla, sat_ECEF.x_m, sat_ECEF.y_m, sat_ECEF.z_m, radians=False)

        event_LLA = coordinates_class.LLA(lat_deg, lon_deg, 0.0) 
        # construct the atmospheric model
        indexOfRefractionGenerator = IndexOfRefractionGenerator(frequency_hz=10e6)
        
        timeAndLocation = TimeAndLocation(eventLocation_LLA =  event_LLA, eventTime_UTC = currentDateTime)

        # ======================================================
        heights_m = [0, 100, 1000, 10000, 100000, 1000000]

        rayPathList = indexOfRefractionGenerator.estimateSlantPath(startTimeAndLocation=timeAndLocation,
         heightStratification_m=heights_m, sat_ECEF=sat_ECEF)

        self.assertEqual(len(rayPathList), len(heights_m))


if __name__ == '__main__':
    unittest.main()
