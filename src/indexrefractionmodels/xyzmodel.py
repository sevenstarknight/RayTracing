import math
from cmath import sqrt
from scipy import constants
import numpy as np
from loguru import logger
# ====================================================
# local imports
from src.bindings.positional.coordinates_class import AER_Coord, ENU_Coord
from src.bindings.vector_class import VectorArray
from src.indexrefractionmodels.abstract_refraction import AbstractIndexRefraction
from src.indexrefractionmodels.transportmodes_enum import TransportMode
from src.bindings.positional.layer_class import Layer
from src.positional.locationconverter_computations import convertFromAER2ENU
from src.models.collisionfrequency import ElectronIonCollisionFrequency, ElectronNeutralCollisionFrequency


class XYZModel(AbstractIndexRefraction):

    def estimateIndexOfRefraction(self, layer: Layer) -> complex:

        iriOutput = self.spacePhysicsModels.iri.generatePointEstimate(
            layer=layer)

        n_e = iriOutput.n_e

        if (n_e == -1.0):
            nSq = 1.0
        else:
            # Atmosphere Model
            msiseOuput = self.spacePhysicsModels.msise.generatePointEstimate(
                layer=layer)

            neutralCollisionFrequency = ElectronNeutralCollisionFrequency()
            electronIonCollisionFrequency = ElectronIonCollisionFrequency()

            v_en = neutralCollisionFrequency.estimateCollisionFreq(
                iriOutput=iriOutput, msiseOutput=msiseOuput)
            v_ei = electronIonCollisionFrequency.estimateCollisionFreq(
                iriOutput=iriOutput)
            v_e = v_en + v_ei

            # Magnetic Field Given Current State
            igrfOutput = self.spacePhysicsModels.igrf.generatePointEstimate(
                layer=layer)

            aer = AER_Coord(ele_deg=layer.aer.ele_deg,
                            az_deg=layer.aer.az_deg, range_m=1.0)
            enu: ENU_Coord = convertFromAER2ENU(aer=aer)

            b_SEZ = VectorArray(-igrfOutput.Bn,
                                igrfOutput.Be, igrfOutput.Bu)

            ray_SEZ = VectorArray(-enu.n_m, enu.e_m, enu.u_m)

            dotAB = np.dot(b_SEZ.data, ray_SEZ.data)
            cosTheta = dotAB/(np.linalg.norm(b_SEZ.data) *
                              np.linalg.norm(ray_SEZ.data))

            # Big X and Big Y
            angularFreq = 2*math.pi*self.frequency_hz
            angularFreq_sq = (angularFreq)**2
            angularFreq_p_sq = (constants.elementary_charge **
                                2)*n_e/(constants.epsilon_0*constants.electron_mass)

            bigX = angularFreq_p_sq/angularFreq_sq

            totalIGRF = igrfOutput.getMagnitude()*10e-9
            gyroFreq = constants.elementary_charge*totalIGRF / constants.electron_mass
            bigY = gyroFreq / angularFreq

            bigZ = v_e/angularFreq

            bigX_Tilda = bigX/(1 - complex(0, -bigZ))
            bigY_Tilda = bigY/(1 - complex(0, -bigZ))

            eta_perp = 1 - bigX_Tilda/(1 - bigY_Tilda*bigY_Tilda)
            eta_cross = bigX_Tilda*bigY_Tilda/(1 - bigY_Tilda*bigY_Tilda)
            eta_par = 1 - bigX_Tilda

            cosTheta_sq = cosTheta*cosTheta
            sinTheta_sq = 1 - cosTheta_sq

            b = eta_perp*eta_perp - eta_cross*eta_cross - eta_par*eta_perp

            if (self.transportMode is TransportMode.ORDINARY_MODE):
                num = b*sinTheta_sq + 2*eta_perp*eta_par + \
                    sqrt(b*b*sinTheta_sq*sinTheta_sq + 4*eta_cross *
                         eta_cross*eta_par*eta_par*cosTheta_sq)
            elif (self.transportMode is TransportMode.EXTRAORDINARY_MODE):
                num = b*sinTheta_sq + 2*eta_perp*eta_par - \
                    sqrt(b*b*sinTheta_sq*sinTheta_sq + 4*eta_cross *
                         eta_cross*eta_par*eta_par*cosTheta_sq)
            else:
                logger.warning("TransportMode Model Not Understood")
                raise Exception("TransportMode Model Not Understood")

            denom = 2*(eta_par*sinTheta_sq + eta_par*cosTheta_sq)

            nSq = num/denom

        return (sqrt(nSq))
