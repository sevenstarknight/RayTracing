import math
from cmath import sqrt
from scipy import constants
from loguru import logger

# ====================================================
# local imports
from src.indexrefractionmodels.abstract_refraction import AbstractIndexRefraction
from src.bindings.positional.layer_class import Layer


class XModel(AbstractIndexRefraction):
    def estimateIndexOfRefraction(self, layer: Layer) -> complex:
        try:
            iriOutput = self.spacePhysicsModels.iri.generatePointEstimate(layer=layer)
        except Exception as me:
            logger.error(str(me))

        n_e = iriOutput.n_e
        if n_e == -1:
            nSq = 1.0
        else:
            angularFreq_sq = (2 * math.pi * self.frequency_hz) ** 2
            angularFreq_p_sq = (
                (constants.elementary_charge**2)
                * n_e
                / (constants.epsilon_0 * constants.electron_mass)
            )
            bigX = angularFreq_p_sq / angularFreq_sq

            nSq = 1 - bigX

        return sqrt(nSq)
