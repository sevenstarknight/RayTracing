# ====================================================
# https://github.com/klaundal/ppigrf
import ppigrf
# ====================================================
# local imports
from src.models.abstractspacephysics_model import AbstractSpacePhysicsModel
from src.models.igrfoutput_class import IGRFOutput
from src.bindings.positional.coordinates_class import LLA_Coord
from src.bindings.positional.layer_class import Layer

class IGRF_Model(AbstractSpacePhysicsModel):

    def generatePointEstimate(self,  layer: Layer) -> IGRFOutput:
        lla : LLA_Coord = layer.lla
        mag = ppigrf.igrf(date=self.currentDateTime, lat=lla.lat_deg,
                        lon=lla.lon_deg, h=lla.altitude_m/1000.0)
        return(IGRFOutput(mag))

    def generateSetEstimate(self,  layers: list[Layer]) -> list[IGRFOutput]:
        igrfOutputs : list[IGRFOutput] = []
        for layer in layers:
            igrfOutputs.append(self.generatePointEstimate(layer=layer))

        return(igrfOutputs)

