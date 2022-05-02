from abc import ABC, abstractmethod

# ====================================================
# local imports
from src.raystate_class import RayState
from src.models.spacephysicsmodels import SpacePhysicsModels
from src.indexrefractionmodels.transportmodes_enum import TransportMode

class AbstractIndexRefraction(ABC):

    def __init__(self, frequency_hz: float, spacePhysicsModels: SpacePhysicsModels, transportMode: TransportMode):
        self.frequency_hz = frequency_hz
        self.spacePhysicsModels = spacePhysicsModels
        self.transportMode = transportMode
        super().__init__()

    @abstractmethod
    def estimateIndexOfRefraction(self, currentState: RayState) -> complex:
        pass
