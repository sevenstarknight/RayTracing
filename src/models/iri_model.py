# ====================================================
# https://github.com/space-physics/iri2016
from iri2016 import IRI

# ====================================================
# local imports
from src.models.abstractspacephysics_model import AbstractSpacePhysicsModel
from src.models.irioutput_class import IRIOutput
from src.bindings.positional.coordinates_class import LLA_Coord
from src.bindings.positional.layer_class import Layer

from src.logger.simlogger import get_logger
LOGGER = get_logger(__name__)


class IRI_Model(AbstractSpacePhysicsModel):

    def generatePointEstimate(self,  layer: Layer) -> IRIOutput:
        lla: LLA_Coord = layer.lla
        altitude_m: float = layer.lla.altitude_m
        newAltitude_m: float = layer.newAltitude_m

        if(altitude_m > 120e3):
            # TODO
            altkmrange = [120e3/1000, 120e3/1000 + 1, 1.0]
        else:
            altkmrange = [altitude_m/1000,
                          newAltitude_m/1000, 1.0]

        try:
            iri = IRI(time=self.currentDateTime, altkmrange=altkmrange,
                      glat=lla.lat_deg, glon=lla.lon_deg)
            output = IRIOutput().from_xarray(iono=iri, altkmrange=altkmrange)

        except Exception as e:
            LOGGER.warning(str(e))
            LOGGER.warning(str(self.currentDateTime) +
                           str(altkmrange) + str(lla.lat_deg) + str(lla.lon_deg))
            output = IRIOutput.from_empty()

        return output

    def generateSetEstimate(self,  layers: list[Layer]) -> list[IRIOutput]:
        iriOutputs: list[IRIOutput] = []
        for layer in layers:
            iriOutputs.append(self.generatePointEstimate(layer=layer))

        return(iriOutputs)
