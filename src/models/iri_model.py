# THIRDPARTY modules
# https://github.com/space-physics/iri2016
from iri2016 import IRI, geoprofile
from sigfig import round
from loguru import logger

# FIRSTPARTY modules
from src.models.abstractspacephysics_model import AbstractSpacePhysicsModel
from src.models.irioutput_class import IRIOutput
from src.bindings.positional.coordinates_class import LLA_Coord
from src.bindings.positional.layer_class import Layer


MIN_ALT_KM = 80
MAX_ALT_KM = 2000

class IRI_Model(AbstractSpacePhysicsModel):
    """
    http://www.physics.mcgill.ca/mist/memos/MIST_memo_46.pdf
    """

    def generatePointEstimate(self, layer:Layer) -> IRIOutput:

        lla1: LLA_Coord = layer.lla_p1
        lla2: LLA_Coord = layer.lla_p2

        altitude_p1_m: float = layer.lla_p1.altitude_m
        altitude_p2_m: float = layer.lla_p2.altitude_m

        if altitude_p1_m /1000 > MAX_ALT_KM:
            altitude_p1_km = MAX_ALT_KM
        elif altitude_p1_m /1000 < MIN_ALT_KM:
            altitude_p1_km = MIN_ALT_KM
        else:
            altitude_p1_km = altitude_p1_m /1000

        if altitude_p2_m /1000 > MAX_ALT_KM:
            altitude_p2_km = MAX_ALT_KM
        elif altitude_p2_m /1000 < MIN_ALT_KM:
            altitude_p2_km = MIN_ALT_KM
        else:
            altitude_p2_km = altitude_p2_m /1000

        # def IRI(time: T.Union[str, datetime], altkmrange: T.Sequence[float], glat: float, glon: float) -> xarray.Dataset:
        try:
            iri1 = IRI(glat=round(lla1.lat_deg, decimals=4), glon=round(lla1.lon_deg, decimals=4), 
                       altkmrange=[round(altitude_p1_km, decimals=4), round(altitude_p2_km, decimals=4), (altitude_p2_km + 1 - altitude_p1_km)/10], time=self.currentDateTime)
        except Exception as me:

            try:
                iri1 = IRI(glat=round(lla2.lat_deg, decimals=4), glon=round(lla2.lon_deg, decimals=4), 
                        altkmrange=[round(altitude_p1_km, decimals=4), round(altitude_p2_km, decimals=4), (altitude_p2_km + 1 - altitude_p1_km)/10], time=self.currentDateTime)
            except Exception as me:
                logger.error(str(me))


        output = IRIOutput().from_geoprofile(iono1=iri1)

        return output

    '''
    def generatePointEstimate(self, layer: Layer) -> IRIOutput:
        lla: LLA_Coord = layer.lla_p1
        altitude_p1_m: float = layer.lla_p1.altitude_m
        altitude_p2_m: float = layer.lla_p2.altitude_m

        if altitude_p1_m /1000 > MAX_ALT_KM:
            # TODO: is this reasonable?
            altkmrange = [MAX_ALT_KM - 1, MAX_ALT_KM , 1.0/10]
        elif altitude_p2_m / 1000 > MIN_ALT_KM and altitude_p1_m / 1000 < MIN_ALT_KM:
            altkmrange = [MIN_ALT_KM, altitude_p2_m / 1000, (altitude_p2_m / 1000 - MIN_ALT_KM)/10]
        else:
            altkmrange = [altitude_p1_m / 1000, altitude_p2_m / 1000, (altitude_p2_m / 1000 - altitude_p1_m / 1000)/10]
        


        """The International Reference Ionosphere (IRI) is the international standard for the specification of parameters
        in the Earths ionosphere. IRI is a data-based model that describes monthly averages of electron density,
        ion temperature, ion composition, and other parameters in the altitude range of 60 km - 2000 km, using
        the available ground and space-based observations of the ionospheric characteristics
        """

        # http://www.physics.mcgill.ca/mist/memos/MIST_memo_46.pdf
        
        try:

            if altitude_p2_m / 1000 < MIN_ALT_KM and altitude_p1_m / 1000 < MIN_ALT_KM:
                logger.warning("Altitude is below Minimum:")
                output = IRIOutput.from_empty()
            else:
                iri = IRI(
                        time=self.currentDateTime,
                        altkmrange=altkmrange,
                        glat=lla.lat_deg,
                        glon=lla.lon_deg,
                    )
                output = IRIOutput().from_xarray(iono=iri)


        except Exception as e:
            logger.warning("Something has gone wrong:")
            logger.warning(str(e))
            logger.warning(
                str(self.currentDateTime) + str(" ")
                + str(altkmrange) + str(" ")
                + str(lla.lat_deg) + str(" ")
                + str(lla.lon_deg) + str(" ")
            )
            output = IRIOutput.from_empty()


        return output
    '''

    def generateSetEstimate(self, layers: list[Layer]) -> list[IRIOutput]:
        iriOutputs: list[IRIOutput] = [
            self.generatePointEstimate(layer=layer) for layer in layers
        ]

        return iriOutputs
