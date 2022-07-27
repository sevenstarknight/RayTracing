
from datetime import datetime

# ====================================================
# https://pyproj4.github.io/pyproj/stable/
import pyproj

# ====================================================
# local imports
from src.bindings.coordinates_class import LLA_Coord
from src.bindings.ionospherestate_class import IonosphereState
from src.bindings.satelliteinformation_class import SatelliteInformation
from src.bindings.timeandlocation_class import TimeAndLocation
from src.indexrefractionmodels.dispersionmodels_enum import DispersionModel
from src.indexrefractionmodels.transportmodes_enum import TransportMode
from src.positional.satellitepositiongenerator import SatellitePositionGenerator
from src.raypatheffects import EstimateRayPathEffects
from src.stratification.quantizationparameter_class import QuantizationParameter
from src.stratification.stratificationmethod_enum import StratificationMethod

# ====================================================
# constants
ECEF = pyproj.Proj(proj='geocent', ellps='WGS84', datum='WGS84')
LLA = pyproj.Proj(proj='latlong', ellps='WGS84', datum='WGS84')

class EndToEndDemo():

    def __init__(self):
        s = '1 25544U 98067A   19343.69339541  .00001764  00000-0  38792-4 0  9991'
        t = '2 25544  51.6439 211.2001 0007417  17.6667  85.6398 15.50103472202482'
        name = "Test"

        self.ionosphereState = IonosphereState(120.0, 150.0, [3.0, 5.0, 6.0, 6.0, 6.0, 6.0, 5.0])

        self.satelliteInformation = SatelliteInformation(name=name, s=s, t=t)

        # Initial Starting Point
        satPosGenerator = SatellitePositionGenerator(self.satelliteInformation)
        currentDateTime = datetime(2012, 9, 15, 13, 14, 30)
        sat_ECEF = satPosGenerator.estimatePosition_ECEF(currentDateTime)

        # ======================================================
        # expected height, assume minimal change in position with range projection
        lon_deg, lat_deg, alt_m = pyproj.transform(
            ECEF, LLA, sat_ECEF.x_m, sat_ECEF.y_m, sat_ECEF.z_m, radians=False)

        event_LLA = LLA_Coord(lat_deg, lon_deg, 0.0)
        self.timeAndLocation = TimeAndLocation(
            eventLocation_LLA=event_LLA, eventTime_UTC=currentDateTime)

        self.freq_Hz = 500e6


    def execute_X(self, quantizationParameter:QuantizationParameter):
        
        optimizer = EstimateRayPathEffects(timeAndLocation=self.timeAndLocation, 
        dispersionModel=DispersionModel.X_MODEL, transportMode=TransportMode.PLASMA_MODE)

        transIonosphereEffects = optimizer.estimate(
            freq_Hz=self.freq_Hz, satelliteInformation=self.satelliteInformation, quantizationParameter=quantizationParameter, 
            ionosphereState=self.ionosphereState)

        return(transIonosphereEffects)


    
    def execute_XY(self, quantizationParameter:QuantizationParameter ):

        optimizer = EstimateRayPathEffects(timeAndLocation=self.timeAndLocation, 
        dispersionModel=DispersionModel.XY_MODEL, transportMode=TransportMode.ORDINARY_MODE)

        transIonosphereEffects = optimizer.estimate(
            freq_Hz=self.freq_Hz, satelliteInformation=self.satelliteInformation, quantizationParameter=quantizationParameter, 
            ionosphereState=self.ionosphereState)

        return(transIonosphereEffects)


    def execute_XYZ(self, quantizationParameter:QuantizationParameter):
        optimizer = EstimateRayPathEffects(timeAndLocation=self.timeAndLocation, 
        dispersionModel=DispersionModel.XYZ_MODEL, transportMode=TransportMode.ORDINARY_MODE)

        transIonosphereEffects = optimizer.estimate(
            freq_Hz=self.freq_Hz, satelliteInformation=self.satelliteInformation, quantizationParameter=quantizationParameter, 
            ionosphereState=self.ionosphereState)

        return(transIonosphereEffects)