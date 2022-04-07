from abc import ABC, abstractmethod
from datetime import datetime

## ====================================================
# specialized imports
# https://github.com/space-physics/iri2016
import iri2016

## ====================================================
# local imports
from raystate_class import RayState
from bindings.ionospherestate_class import IonosphereState
from models.spacephysicsmodels import SpacePhysicsModels

class AbstractIndexRefraction(ABC):
 
    def __init__(self, frequency_hz : float, spacePhysicsModels: SpacePhysicsModels):
        self.frequency_hz = frequency_hz
        self.spacePhysicsModels = spacePhysicsModels
        super().__init__()
    
    @abstractmethod
    def estimateIndexOfRefraction(self, currentState : RayState) ->complex:
        pass