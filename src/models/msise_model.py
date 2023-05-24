# ====================================================
# https://pypi.org/project/nrlmsise00/
from nrlmsise00 import msise_model

# ====================================================
# local imports
from src.models.abstractspacephysics_model import AbstractSpacePhysicsModel
from src.models.msiseoutput_class import MSISEOutput
from src.bindings.positional.coordinates_class import LLA_Coord
from src.bindings.positional.layer_class import Layer


class MSISE_Model(AbstractSpacePhysicsModel):
    def generatePointEstimate(self, layer: Layer) -> MSISEOutput:
        # Atmosphere Model
        lla: LLA_Coord = layer.lla
        ds, ts = msise_model(
            time=self.currentDateTime,
            alt=lla.altitude_m / 1000,
            lat=lla.lat_deg,
            lon=lla.lon_deg,
            f107a=self.ionosphereState.f107a,
            f107=self.ionosphereState.f107,
            ap=self.ionosphereState.ap[0],
            ap_a=self.ionosphereState.ap,
        )
        return MSISEOutput(ds, ts)

    def generateSetEstimate(self, layers: list[Layer]) -> list[MSISEOutput]:
        msiseOutputs: list[MSISEOutput] = [
            self.generatePointEstimate(layer=layer) for layer in layers
        ]

        return msiseOutputs
