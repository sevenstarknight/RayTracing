import math
from scipy import constants

## ====================================================
# local imports
from raytracing.indexrefractionmodels.abstract_refraction import AbstractIndexRefraction
from raystate_class import RayState

class XModel(AbstractIndexRefraction):

    def estimateIndexOfRefraction(self, currentState : RayState) -> complex:

        iriOutput = self.spacePhysicsModels.iri.generatePointEstimate(rayPoint=currentState.lla)

        n_e = iriOutput.iono["ne"].iloc[0].item()
        if(n_e == -1):
            nSq = 1.0
        else:
            angularFreq_sq = (2*math.pi*self.frequency_hz)**2
            angularFreq_p_sq = (constants.elementary_charge**2)*n_e/(constants.electron_mass)
            bigX = angularFreq_p_sq/angularFreq_sq

            nSq = 1 - bigX

        return(nSq)

