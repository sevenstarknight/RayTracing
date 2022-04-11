import math
from datetime import datetime
from scipy import constants
import numpy as np

# ====================================================
# specialized imports
# https://geospace-code.github.io/pymap3d/index.html
import pymap3d

# ====================================================
# local imports
from bindings.vector_class import VectorArray

from indexrefractionmodels.abstract_refraction import AbstractIndexRefraction
from raystate_class import RayState
from models.collisionfrequency import ElectronIonCollisionFrequency, ElectronNeutralCollisionFrequency


class XYZModel(AbstractIndexRefraction):

    # datetime(2009, 6, 21, 8, 3, 20)
    def estimateIndexOfRefraction(self, currentDateTime: datetime, currentState: RayState) -> complex:

        iriOutput = self.spacePhysicsModels.iri.generatePointEstimate(
            rayPoint=currentState.lla)

        n_e = iriOutput.n_e

        if(n_e == -1.0):
            nSq = 1.0
        else:
            # Atmosphere Model
            msiseOuput = self.spacePhysicsModels.msise.generatePointEstimate(
                rayPoint=currentState.lla)

            neutralCollisionFrequency = ElectronNeutralCollisionFrequency()
            electronIonCollisionFrequency = ElectronIonCollisionFrequency()

            v_en = neutralCollisionFrequency.estimateCollisionFreq(
                iriOutput=iriOutput, msiseOutput=msiseOuput)
            v_ei = electronIonCollisionFrequency.estimateCollisionFreq(
                msiseOutput=msiseOuput)
            v_e = v_en + v_ei

            # Magnetic Field Given Current State
            igrfOutput = self.spacePhysicsModels.igrf.generatePointEstimate(
                rayPoint=currentState.lla)
            east, north, up = pymap3d.aer2enu(
                currentState.exitAzimuth_deg, currentState.exitElevation_deg, 1.0, deg=True)

            b_SEZ = VectorArray(-igrfOutput.igrf['north'].iloc[0],
                                igrfOutput.igrf['east'].iloc[0], igrfOutput.igrf['down'].iloc[0])
            ray_SEZ = VectorArray(north, east, -up)
            dotAB = np.dot(b_SEZ.data, ray_SEZ.data)
            cosTheta = dotAB/(np.linalg.norm(b_SEZ.data) *
                              np.linalg.norm(ray_SEZ.data))

            # Big X and Big Y
            angularFreq_sq = (2*math.pi*self.frequency_hz)**2
            angularFreq_p_sq = (constants.elementary_charge **
                                2)*n_e/(constants.electron_mass)

            bigX = angularFreq_p_sq/angularFreq_sq

            bigY = constants.elementary_charge*igrfOutput.igrf.total.item() / \
                (constants.electron_mass*math.sqrt(angularFreq_sq))

            bigZ = v_e/angularFreq_sq

            bigX_Tilda = bigX/(1 - complex(0, -bigZ))
            bigY_Tilda = bigY/(1 - complex(0, -bigZ))

            eta_perp = 1 - bigX_Tilda/(1 - bigY_Tilda*bigY_Tilda)
            eta_cross = bigX_Tilda*bigY_Tilda/(1 - bigY_Tilda*bigY_Tilda)
            eta_par = 1 - bigX_Tilda

            cosTheta_sq = cosTheta*cosTheta
            sinTheta_sq = 1 - cosTheta_sq

            b = eta_perp*eta_perp - eta_cross*eta_cross - eta_par*eta_perp

            num = b*sinTheta_sq + 2*eta_perp*eta_par + \
                math.sqrt(b*b*sinTheta_sq*sinTheta_sq + 4*eta_cross *
                          eta_cross*eta_par*eta_par*cosTheta_sq)
            denom = 2*(eta_par*sinTheta_sq + eta_par*cosTheta_sq)

            nSq = num/denom

        return(nSq)
