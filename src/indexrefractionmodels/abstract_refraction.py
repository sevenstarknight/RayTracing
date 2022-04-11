from abc import ABC, abstractmethod
# ====================================================
# local imports
from raystate_class import RayState
from models.spacephysicsmodels import SpacePhysicsModels


class AbstractIndexRefraction(ABC):

    def __init__(self, frequency_hz: float, spacePhysicsModels: SpacePhysicsModels):
        self.frequency_hz = frequency_hz
        self.spacePhysicsModels = spacePhysicsModels
        super().__init__()

    @abstractmethod
    def estimateIndexOfRefraction(self, currentState: RayState) -> complex:
        pass