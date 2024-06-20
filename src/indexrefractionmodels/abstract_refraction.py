# STDLIB modules
from abc import ABC, abstractmethod

# FIRSTPARTY modules
from src.models.spacephysicsmodels import SpacePhysicsModels
from src.indexrefractionmodels.transportmodes_enum import TransportMode
from src.bindings.positional.layer_class import Layer


class AbstractIndexRefraction(ABC):
    def __init__(
        self,
        frequency_hz: float,
        spacePhysicsModels: SpacePhysicsModels,
        transportMode: TransportMode,
    ):
        self.frequency_hz = frequency_hz
        self.spacePhysicsModels = spacePhysicsModels
        self.transportMode = transportMode

    @abstractmethod
    def estimateIndexOfRefraction(self, layer: Layer) -> complex:
        pass
