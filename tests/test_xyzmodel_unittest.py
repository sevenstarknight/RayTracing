import unittest
from datetime import datetime

# ====================================================
# https://pyproj4.github.io/pyproj/stable/
import pyproj

# ====================================================
# local imports
from src.bindings import coordinates_class
from src.bindings.coordinates_class import LLA
from src.bindings.ionospherestate_class import IonosphereState
from src.bindings.satelliteinformation_class import SatelliteInformation
from src.bindings.timeandlocation_class import TimeAndLocation
from src.indexrefractionmodels.xyzmodel import XYZModel
from src.models.igrf_model import IGRF_Model
from src.models.iri_model import IRI_Model
from src.models.msise_model import MSISE_Model
from src.models.spacephysicsmodels import SpacePhysicsModels
from src.raystate_class import RayState
from src.positional.satellitepositiongenerator import SatellitePositionGenerator
from src.positional.slantpathgenerator import SlantPathGenerator

# ====================================================
# constants
ecef = pyproj.Proj(proj='geocent', ellps='WGS84', datum='WGS84')
lla = pyproj.Proj(proj='latlong', ellps='WGS84', datum='WGS84')


class TestXYZModel(unittest.TestCase):

    def test_xyzModel(self):

        ap = [1, 2, 3, 4, 2, 2, 1]
        ionosphereState = IonosphereState(20.5, 20.6, ap)
        currentDateTime = datetime(2012, 9, 15, 13, 14, 30)

        event_LLA = LLA(0.0, 0.0, 0.0)
        rayState = RayState(exitAzimuth_deg=0.0,
                            exitElevation_deg=45.0, lla=event_LLA, nIndex=1.0)

        s = '1 25544U 98067A   19343.69339541  .00001764  00000-0  38792-4 0  9991'
        t = '2 25544  51.6439 211.2001 0007417  17.6667  85.6398 15.50103472202482'
        name = "Test"

        satelliteInformation = SatelliteInformation(name=name, s=s, t=t)

        # Initial Starting Point
        satPosGenerator = SatellitePositionGenerator(satelliteInformation)
        currentDateTime = datetime(2012, 9, 15, 13, 14, 30)
        sat_ECEF = satPosGenerator.estimatePosition_ECEF(currentDateTime)

        # expected height, assume minimal change in position with range projection
        lon_deg, lat_deg, alt_m = pyproj.transform(
            ecef, lla, sat_ECEF.x_m, sat_ECEF.y_m, sat_ECEF.z_m, radians=False)

        event_LLA = coordinates_class.LLA(lat_deg, lon_deg, 0.0)

        timeAndLocation = TimeAndLocation(
            eventLocation_LLA=event_LLA, eventTime_UTC=currentDateTime)

        # ======================================================
        heights_m = [0, 100, 1000, 10000, 100000, 1000000]

        # make LLAs
        slantPathGenerator = SlantPathGenerator()
        # make LLAs
        listOfSlant_RayState = slantPathGenerator.estimateSlantPath(
            timeAndLocation, sat_ECEF, heights_m)

        # make the model
        ionosphereState = IonosphereState(10.0, 10.0, [3.0, 3.0, 3.0])
        igrf = IGRF_Model(
            currentDateTime=timeAndLocation.eventTime_UTC, ionosphereState=ionosphereState)
        iri = IRI_Model(currentDateTime=timeAndLocation.eventTime_UTC,
                        ionosphereState=ionosphereState)
        msise = MSISE_Model(
            currentDateTime=timeAndLocation.eventTime_UTC, ionosphereState=ionosphereState)

        spm = SpacePhysicsModels(igrf=igrf, msise=msise, iri=iri)

        # model the index of refraction
        xyzModel = XYZModel(spacePhysicsModels=spm, frequency_hz=10e6)

        indexNs = []
        for rayState in listOfSlant_RayState:
            indexN = xyzModel.estimateIndexOfRefraction(currentState=rayState)
            indexNs.append(indexN)

        self.assertTrue(len(indexNs) == len(heights_m))