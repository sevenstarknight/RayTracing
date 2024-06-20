
# FIRSTPARTY modules
from src.bindings.positional.coordinates_class import ECEF_Coord
from src.bindings.positional.timeandlocation_class import TimeAndLocation
from src.bindings.models.ionospherestate_class import IonosphereState
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

    def __init__(self, frequency_hz: float, dispersionModel: DispersionModel, transportMode: TransportMode,
                 startTimeAndLocation: TimeAndLocation, ionosphereState: IonosphereState):
        self.startTimeAndLocation = startTimeAndLocation

        # make the model
        igrf = IGRF_Model(
            currentDateTime=startTimeAndLocation.eventTime_UTC, ionosphereState=ionosphereState)
        iri = IRI_Model(
            currentDateTime=startTimeAndLocation.eventTime_UTC, ionosphereState=ionosphereState)
        msise = MSISE_Model(
            currentDateTime=startTimeAndLocation.eventTime_UTC, ionosphereState=ionosphereState)

        spm = SpacePhysicsModels(igrf=igrf, msise=msise, iri=iri)

        # model the index of refraction
        if (dispersionModel is DispersionModel.X_MODEL):
            self.refractionModel = XModel(
                spacePhysicsModels=spm, frequency_hz=frequency_hz, transportMode=transportMode)
        elif (dispersionModel is DispersionModel.XY_MODEL):
            self.refractionModel = XYModel(
                spacePhysicsModels=spm, frequency_hz=frequency_hz, transportMode=transportMode)
        elif (dispersionModel is DispersionModel.XYZ_MODEL):
            self.refractionModel = XYZModel(
                spacePhysicsModels=spm, frequency_hz=frequency_hz, transportMode=transportMode)
        else:
            raise Exception("Dispersion Model Unknown")

    def estimateIndexN(self, sat_ECEF: ECEF_Coord,  heightStratification_m: list[float]) -> list[complex]:

        slantPathGenerator = SlantPathGenerator()
        # make layers
        layers = slantPathGenerator.estimateSlantPath(
            self.startTimeAndLocation, sat_ECEF, heightStratification_m)

        # Loop over layers
        indexNs = [self.refractionModel.estimateIndexOfRefraction(layer=layer) for layer in layers]
        
        # tack on an open layer at the nd 
        indexNs.append(indexNs[-1])

        return (indexNs)
