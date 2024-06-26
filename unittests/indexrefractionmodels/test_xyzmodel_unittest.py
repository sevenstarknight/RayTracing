# STDLIB modules
import unittest
from datetime import datetime

# FIRSTPARTY modules
from src.bindings.positional.coordinates_class import LLA_Coord
from src.bindings.models.ionospherestate_class import IonosphereState
from src.bindings.positional.layer_class import Layer
from src.bindings.positional.satelliteinformation_class import SatelliteInformation
from src.bindings.positional.timeandlocation_class import TimeAndLocation
from src.indexrefractionmodels.xyzmodel import XYZModel
from src.indexrefractionmodels.transportmodes_enum import TransportMode
from src.models.igrf_model import IGRF_Model
from src.models.iri_model import IRI_Model
from src.models.msise_model import MSISE_Model
from src.models.spacephysicsmodels import SpacePhysicsModels
from src.positional.locationconverter_computations import LocationConverterComputation
from src.positional.satellitepositiongenerator import SatellitePositionGenerator
from src.positional.slantpathgenerator import SlantPathGenerator


class TestXYZModel(unittest.TestCase):

    def test_xyzModel(self):

        ap = [1.0, 2.0, 3.0, 4.0, 2.0, 2.0, 1.0]
        ionosphereState = IonosphereState(f107 = 20.5, f107a =  20.6, ap = ap)
        currentDateTime = datetime(2012, 9, 15, 13, 14, 30)

        event_LLA = LLA_Coord(0.0, 0.0, 0.0)

        s = '1 25544U 98067A   19343.69339541  .00001764  00000-0  38792-4 0  9991'
        t = '2 25544  51.6439 211.2001 0007417  17.6667  85.6398 15.50103472202482'
        name = "Test"

        satelliteInformation = SatelliteInformation(name=name, s=s, t=t)

        # Initial Starting Point
        satPosGenerator = SatellitePositionGenerator(satelliteInformation)
        currentDateTime = datetime(2012, 9, 15, 13, 14, 30)
        sat_ECEF = satPosGenerator.estimatePosition_ECEF(currentDateTime)

        # expected height, assume minimal change in position with range projection
        event_LLA: LLA_Coord = LocationConverterComputation.convertFromECEFtoLLA(ecef=sat_ECEF)
        event_LLA.setAltitude(0.0)

        timeAndLocation = TimeAndLocation(
            eventLocation_LLA=event_LLA, eventTime_UTC=currentDateTime)

        # ======================================================
        heights_m = [0, 100, 1000, 10000, 100000, 1000000]

        # make LLAs
        slantPathGenerator = SlantPathGenerator()
        # make LLAs
        slantLayers : list[Layer] = slantPathGenerator.estimateSlantPath(
            timeAndLocation, sat_ECEF, heights_m)

        # make the model
        igrf = IGRF_Model(
            currentDateTime=timeAndLocation.eventTime_UTC, ionosphereState=ionosphereState)
        iri = IRI_Model(currentDateTime=timeAndLocation.eventTime_UTC,
                        ionosphereState=ionosphereState)
        msise = MSISE_Model(
            currentDateTime=timeAndLocation.eventTime_UTC, ionosphereState=ionosphereState)

        spm = SpacePhysicsModels(igrf=igrf, msise=msise, iri=iri)

        # model the index of refraction
        xyzModel = XYZModel(spacePhysicsModels=spm, frequency_hz=10e6, transportMode=TransportMode.ORDINARY_MODE)

        indexNs = []
        for layer in slantLayers:
            indexN = xyzModel.estimateIndexOfRefraction(layer=layer)
            indexNs.append(indexN)

        self.assertTrue(len(indexNs) == len(heights_m) - 1)
