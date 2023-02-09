# ====================================================
# https://github.com/space-physics/wmm2020
import igrf

# ====================================================
# local imports
from src.models.abstractspacephysics_model import AbstractSpacePhysicsModel
from src.models.igrfoutput_class import IGRFOutput
from src.bindings.positional.coordinates_class import LLA_Coord
from src.bindings.positional.layer_class import Layer

class IGRF_Model(AbstractSpacePhysicsModel):

    def generatePointEstimate(self,  layer: Layer) -> IGRFOutput:
        lla : LLA_Coord = layer.lla
        mag = igrf.igrf(self.currentDateTime, glat=lla.lat_deg,
                        glon=lla.lon_deg, alt_km=lla.altitude_m/1000.0)
        return(IGRFOutput(mag))

    def generateSetEstimate(self,  layers: list[Layer]) -> list[IGRFOutput]:
        igrfOutputs : list[IGRFOutput] = []
        for layer in layers:
            igrfOutputs.append(self.generatePointEstimate(layer=layer))

        return(igrfOutputs)

