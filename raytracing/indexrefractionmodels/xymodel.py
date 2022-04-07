import math
from scipy import constants
import numpy as np

## ====================================================
# specialized imports
#https://geospace-code.github.io/pymap3d/index.html
import pymap3d

## ====================================================
# local imports
from bindings.vector_class import VectorArray
from raytracing.indexrefractionmodels.abstract_refraction import AbstractIndexRefraction
from raystate_class import RayState

class XYModel(AbstractIndexRefraction):

    def estimateIndexOfRefraction(self, currentState : RayState) -> complex:

        # Ionosphere model
        iriOutput = self.spacePhysicsModels.iri.generatePointEstimate(rayPoint=currentState.lla)
        n_e = iriOutput["ne"][0].item()

        if(n_e == -1.0):
            nSq = 1.0
        else:
            ## Magnetic Field Given Current State
            bNED_T = self.spacePhysicsModels.igrf.generatePointEstimate(rayPoint=currentState.lla)
            east,north,up = pymap3d.aer2enu(currentState.exitAzimuth_deg, currentState.exitElevation_deg, 1.0, deg=True)

            b_SEZ = VectorArray(-bNED_T.north.item(), bNED_T.east.item(), bNED_T.down.item())
            ray_SEZ = VectorArray(north, east, -up)
            dotAB = np.dot(b_SEZ.data, ray_SEZ.data)
            cosTheta = dotAB/(np.linalg.norm(b_SEZ)*np.linalg.norm(ray_SEZ))

            # Big X and Big Y
            angularFreq_sq = (2*math.pi*self.frequency_hz)**2
            angularFreq_p_sq = (constants.elementary_charge**2)*n_e/(constants.electron_mass)

            bigX = angularFreq_p_sq/angularFreq_sq
            bigY = constants.elementary_charge*bNED_T.total.item()/(constants.electron_mass*math.sqrt(angularFreq_sq))

            eta_perp = 1 - bigX/(1- bigY*bigY)
            eta_cross = bigX*bigY/(1- bigY*bigY)
            eta_par = 1- bigX

            cosTheta_sq = cosTheta*cosTheta
            sinTheta_sq = 1 - cosTheta_sq

            b = eta_perp*eta_perp - eta_cross*eta_cross - eta_par*eta_perp

            num = b*sinTheta_sq + 2*eta_perp*eta_par + math.sqrt(b*b*sinTheta_sq*sinTheta_sq + 4*eta_cross*eta_cross*eta_par*eta_par*cosTheta_sq)
            denom = 2*(eta_par*sinTheta_sq + eta_par*cosTheta_sq)

            nSq = num/denom

        return(nSq)