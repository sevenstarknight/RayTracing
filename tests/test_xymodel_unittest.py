import unittest
from datetime import datetime
# https://pyproj4.github.io/pyproj/stable/
import pyproj
from raytracing.indexofrefractiongenerator import IndexOfRefractionGenerator
from raytracing.bindings import coordinates_class
## ====================================================
# local imports
from raytracing.bindings.coordinates_class import LLA
from raytracing.bindings.ionospherestate_class import IonosphereState
from raytracing.bindings.satelliteinformation_class import SatelliteInformation
from raytracing.bindings.timeandlocation_class import TimeAndLocation
from raytracing.indexrefractionmodels.dispersionmodels_enum import DispersionModel
from raytracing.indexrefractionmodels.xymodel import XYModel
from raytracing.models.igrf_model import IGRF_Model
from raytracing.models.iri_model import IRI_Model
from raytracing.models.msise_model import MSISE_Model
from raytracing.models.spacephysicsmodels import SpacePhysicsModels
from raytracing.raystate_class import RayState
from raytracing.satellitepositiongenerator import SatellitePositionGenerator

ecef = pyproj.Proj(proj='geocent', ellps='WGS84', datum='WGS84')
lla = pyproj.Proj(proj='latlong', ellps='WGS84', datum='WGS84')


class TestXYModel(unittest.TestCase):

    def test_xyModel(self):
        
        ap = [1,2,3,4,2,2,1]
        ionosphereState = IonosphereState(20.5, 20.6, ap)
        currentDateTime = datetime(2012, 9, 15, 13, 14, 30)
        
        event_LLA = LLA(0.0, 0.0, 0.0) 
        rayState = RayState(exitAzimuth_deg=0.0, exitElevation_deg=45.0, lla = event_LLA, nIndex=1.0)

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
        
        timeAndLocation = TimeAndLocation(eventLocation_LLA =  event_LLA, eventTime_UTC = currentDateTime)

        # ======================================================
        heights_m = [0, 100, 1000, 10000, 100000, 1000000]

        # make LLAs
        indexOfRefractionGenerator = IndexOfRefractionGenerator(frequency_hz=10e6, dispersionModel=DispersionModel.X_MODEL)
        listOfSlant_RayState = indexOfRefractionGenerator.estimateSlantPath(timeAndLocation, sat_ECEF, heights_m)

        # make the model
        ionosphereState = IonosphereState(10.0, 10.0, 3.0)
        igrf = IGRF_Model(currentDateTime=timeAndLocation.eventTime_UTC, ionosphereState=ionosphereState)
        iri = IRI_Model(currentDateTime=timeAndLocation.eventTime_UTC, ionosphereState=ionosphereState)
        msise = MSISE_Model(currentDateTime=timeAndLocation.eventTime_UTC, ionosphereState=ionosphereState)

        spm = SpacePhysicsModels(igrf=igrf, msise=msise, iri=iri)

        # model the index of refraction
        xyModel = XYModel(spacePhysicsModels=spm, frequency_hz=10e6)

        listIndexN = []
        for rayState in listOfSlant_RayState:
            indexN = xyModel.estimateIndexOfRefraction(currentState = rayState)
            listIndexN.append(indexN)

        self.assertTrue(len(listIndexN) == len(heights_m))