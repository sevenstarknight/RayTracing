# ====================================================
# local imports
from src.bindings.coordinates_class import ECEF_Coord
from src.bindings.timeandlocation_class import TimeAndLocation
from src.bindings.ionospherestate_class import IonosphereState
from src.indexrefractionmodels.xmodel import XModel
from src.indexrefractionmodels.xymodel import XYModel
from src.indexrefractionmodels.xyzmodel import XYZModel
from src.indexrefractionmodels.dispersionmodels_enum import DispersionModel
from src.indexrefractionmodels.transportmodes_enum import TransportMode

from src.models.igrf_model import IGRF_Model
from src.models.iri_model import IRI_Model
from src.models.msise_model import MSISE_Model
from src.models.spacephysicsmodels import SpacePhysicsModels
from src.positional.slantpathgenerator import SlantPathGenerator

class IndexOfRefractionGenerator():

    def __init__(self, frequency_hz: float, dispersionModel: DispersionModel, transportMode: TransportMode):
        self.frequency_hz = frequency_hz
        self.dispersionModel = dispersionModel
        self.transportMode = transportMode

    def estimateIndexN(self, startTimeAndLocation: TimeAndLocation, sat_ECEF: ECEF_Coord, heightStratification_m: list[float]) -> list[complex]:

        slantPathGenerator = SlantPathGenerator()
        # make LLAs
        slantRayStates = slantPathGenerator.estimateSlantPath(
            startTimeAndLocation, sat_ECEF, heightStratification_m)

        # make the model
        ionosphereState = IonosphereState(10.0, 10.0, 3.0)
        igrf = IGRF_Model(
            currentDateTime=startTimeAndLocation.eventTime_UTC, ionosphereState=ionosphereState)
        iri = IRI_Model(currentDateTime=startTimeAndLocation.eventTime_UTC,
                        ionosphereState=ionosphereState)
        msise = MSISE_Model(
            currentDateTime=startTimeAndLocation.eventTime_UTC, ionosphereState=ionosphereState)

        spm = SpacePhysicsModels(igrf=igrf, msise=msise, iri=iri)

        # model the index of refraction
        if(self.dispersionModel is DispersionModel.X_MODEL):
            refractionModel = XModel(spacePhysicsModels=spm, frequency_hz=self.frequency_hz, transportMode=self.transportMode)
        elif(self.dispersionModel is DispersionModel.XY_MODEL):
            refractionModel = XYModel(spacePhysicsModels=spm, frequency_hz=self.frequency_hz, transportMode=self.transportMode)
        elif(self.dispersionModel is DispersionModel.XYZ_MODEL):
            refractionModel = XYZModel(spacePhysicsModels=spm, frequency_hz=self.frequency_hz, transportMode=self.transportMode)
        else:
            raise Exception("Dispersion Model Unknown")

        indexNs = []
        for rayState in slantRayStates:
            indexN = refractionModel.estimateIndexOfRefraction(currentState=rayState)
            indexNs.append(indexN)

        return(indexNs)
