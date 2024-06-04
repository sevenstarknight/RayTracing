import unittest
from datetime import datetime

# ====================================================
# https://pyproj4.github.io/pyproj/stable/
import pyproj
# ====================================================
# local imports
from src.bindings.models.ionospherestate_class import IonosphereState
from src.indexrefractionmodels.dispersionmodels_enum import DispersionModel
from src.indexrefractionmodels.transportmodes_enum import TransportMode
from src.raytracer.raypathoptimizer import RayPathOptimizer
from unittests.unittest_computations import standardSatelliteInformation, standardStartingPoint

# ====================================================
# constants
ECEF = pyproj.Proj(proj='geocent', ellps='WGS84', datum='WGS84')
LLA = pyproj.Proj(proj='latlong', ellps='WGS84', datum='WGS84')


class TestRayPathOptimization(unittest.TestCase):

    def setUp(self):
        self.satelliteInformation = standardSatelliteInformation()

        self.timeAndLocation = standardStartingPoint(self.satelliteInformation )

        self.ionosphereState = IonosphereState(10.0, 10.0, 3.0)

        # ======================================================
        self.heights_m = [0, 100, 1000, 10000, 100000, 1000000]

    def test_RayPathOptimizationX(self):


        optimizer = RayPathOptimizer(freq_hz= 1000e6,  timeAndLocation=self.timeAndLocation, 
        heights_m=self.heights_m, dispersionModel=DispersionModel.X_MODEL, 
            transportMode=TransportMode.PLASMA_MODE, ionosphereState= self.ionosphereState)
        rayState = optimizer.optimize(self.satelliteInformation)

        self.assertTrue(rayState is not None)


    def test_RayPathOptimizationXY(self):

        optimizer = RayPathOptimizer(freq_hz= 100e6, timeAndLocation=self.timeAndLocation, heights_m=self.heights_m, dispersionModel=DispersionModel.XY_MODEL, 
            transportMode=TransportMode.ORDINARY_MODE, ionosphereState= self.ionosphereState)
        rayState = optimizer.optimize(self.satelliteInformation)

        self.assertTrue(rayState is not None)

if __name__ == '__main__':
    unittest.main()
