# ====================================================
# https://github.com/space-physics/iri2016
from iri2016 import IRI, geoprofile
from loguru import logger

# ====================================================
# local imports
from src.models.abstractspacephysics_model import AbstractSpacePhysicsModel
from src.models.irioutput_class import IRIOutput
from src.bindings.positional.coordinates_class import LLA_Coord
from src.bindings.positional.layer_class import Layer


class IRI_Model(AbstractSpacePhysicsModel):
    def generatePointEstimate(self, layer: Layer) -> IRIOutput:
        lla: LLA_Coord = layer.lla_p1
        altitude_p1_m: float = layer.lla_p1.altitude_m
        altitude_p2_m: float = layer.lla_p2.altitude_m

        if altitude_p1_m > 2000e3:
            # TODO: is this reasonable?
            altkmrange = [2000e3 / 1000 - 1, 2000e3 / 1000 , 1.0/10]
        else:
            altkmrange = [altitude_p1_m / 1000, altitude_p2_m / 1000, (altitude_p2_m / 1000 - altitude_p1_m / 1000)/10]
        


        """The International Reference Ionosphere (IRI) is the international standard for the specification of parameters
        in the Earths ionosphere. IRI is a data-based model that describes monthly averages of electron density,
        ion temperature, ion composition, and other parameters in the altitude range of 50 km - 2000 km, using
        the available ground and space-based observations of the ionospheric characteristics
        """

        # http://www.physics.mcgill.ca/mist/memos/MIST_memo_46.pdf
        if altitude_p2_m / 1000 > 50:
            try:
        
                iri = IRI(
                    time=self.currentDateTime,
                    altkmrange=altkmrange,
                    glat=lla.lat_deg,
                    glon=lla.lon_deg,
                )
                output = IRIOutput().from_xarray(iono=iri)

            except Exception as e:
                logger.warning("Altitude is below 50km:")
                logger.warning(str(e))
                logger.warning(
                    str(self.currentDateTime) + str(" ")
                    + str(altkmrange) + str(" ")
                    + str(lla.lat_deg) + str(" ")
                    + str(lla.lon_deg) + str(" ")
                )
                output = IRIOutput.from_empty()
        else:
            logger.warning("Altitude is below 50km:")
            output = IRIOutput.from_empty()

        return output

    def generateSetEstimate(self, layers: list[Layer]) -> list[IRIOutput]:
        iriOutputs: list[IRIOutput] = [
            self.generatePointEstimate(layer=layer) for layer in layers
        ]

        return iriOutputs
