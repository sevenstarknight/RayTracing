import unittest
from datetime import datetime
import pandas as pd

# ====================================================
# https://pyproj4.github.io/pyproj/stable/
import pyproj

# ====================================================
# local imports
from src.bindings.coordinates_class import LLA_Coord
from src.bindings.satelliteinformation_class import SatelliteInformation
from src.bindings.timeandlocation_class import TimeAndLocation
from src.bindings.ionospherestate_class import IonosphereState
from src.indexrefractionmodels.dispersionmodels_enum import DispersionModel
from src.indexrefractionmodels.transportmodes_enum import TransportMode
from src.positional.satellitepositiongenerator import SatellitePositionGenerator
from src.stratification.quantizationparameter_class import QuantizationParameter
from src.stratification.stratificationmethod_enum import StratificationMethod
from src.raypatheffects import EstimateRayPathEffects
# ====================================================
# constants
ECEF = pyproj.Proj(proj='geocent', ellps='WGS84', datum='WGS84')
LLA = pyproj.Proj(proj='latlong', ellps='WGS84', datum='WGS84')

class TestStratificationIntegration(unittest.TestCase):

    def test_StratificationOptimizer(self):

        s = '1 25544U 98067A   19343.69339541  .00001764  00000-0  38792-4 0  9991'
        t = '2 25544  51.6439 211.2001 0007417  17.6667  85.6398 15.50103472202482'
        name = "Test"

        satelliteInformation = SatelliteInformation(name=name, s=s, t=t)
        satPosGenerator = SatellitePositionGenerator(satelliteInformation)

        # Initial Starting Point
        currentDateTime = datetime(2021, 1, 26, 12, 0, 0)
        sat_ECEF = satPosGenerator.estimatePosition_ECEF(currentDateTime)

        # expected height, assume minimal change in position with range projection
        lon_deg, lat_deg, alt_m = pyproj.transform(
            ECEF, LLA, sat_ECEF.x_m, sat_ECEF.y_m, sat_ECEF.z_m, radians=False)

        event_LLA = LLA_Coord(lat_deg, lon_deg, 0.0)
        timeAndLocation = TimeAndLocation(
            eventLocation_LLA=event_LLA, eventTime_UTC=currentDateTime)


        ionosphereState = IonosphereState(150.0, 150.0, 3.0)

        # ======================================================
        estimateRayPathEffects = EstimateRayPathEffects(
            timeAndLocation=timeAndLocation, dispersionModel=DispersionModel.X_MODEL, transportMode=TransportMode.PLASMA_MODE)

        freq_Hz = 1000*6

        quantizationParameter = QuantizationParameter(StratificationMethod.DECIMATION_MODEL,nQuant=10)

        transIonosphereEffects = estimateRayPathEffects.estimate(freq_Hz=freq_Hz, quantizationParameter=quantizationParameter, 
        ionosphereState=ionosphereState, satelliteInformation=satelliteInformation)

        print(transIonosphereEffects.totalIonoDelay_sec)
        print(transIonosphereEffects.totalIonoLoss_db)

        rayStates = transIonosphereEffects.rayStates
        listTmp = []
        columnNames = []
        for rayState in rayStates:
            tmpList = rayState.generateList()
            listTmp.append(tmpList)
            columnNames = rayState.generateColumnNames()

        df = pd.DataFrame(listTmp, columns = columnNames, dtype = float)