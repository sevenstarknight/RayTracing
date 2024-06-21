# STDLIB modules
import math
from cmath import sqrt

# THIRDPARTY modules
from scipy import constants
import numpy as np
from loguru import logger

# FIRSTPARTY modules
from src.bindings.positional.coordinates_class import AER_Coord, ENU_Coord
from src.bindings.vector_class import VectorArray
from src.indexrefractionmodels.abstract_refraction import AbstractIndexRefraction
from src.indexrefractionmodels.transportmodes_enum import TransportMode
from src.bindings.positional.layer_class import Layer
from src.positional.locationconverter_computations import LocationConverterComputation 


class XYModel(AbstractIndexRefraction):

    def estimateIndexOfRefraction(self, layer: Layer) -> complex:

        # Ionosphere model
        iriOutput = self.spacePhysicsModels.iri.generatePointEstimate(
            layer=layer)
        n_e = iriOutput.n_e

        if np.isnan(n_e):
            nSq = 1.0
        else:
            # Magnetic Field Given Current State
            igrfOutput = self.spacePhysicsModels.igrf.generatePointEstimate(
                layer=layer)

            aer = AER_Coord(ele_deg=layer.aer.ele_deg,
                            az_deg=layer.aer.az_deg, range_m=1.0)
            enu: ENU_Coord = LocationConverterComputation.convertFromAER2ENU(aer=aer)

            b_SEZ = VectorArray(-igrfOutput.Bn, igrfOutput.Be, igrfOutput.Bu)

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

            eta_perp = 1 - bigX/(1 - bigY*bigY)
            eta_cross = bigX*bigY/(1 - bigY*bigY)
            eta_par = 1 - bigX

            cosTheta_sq = cosTheta*cosTheta
            sinTheta_sq = 1 - cosTheta_sq

            b = eta_perp*eta_perp - eta_cross*eta_cross - eta_par*eta_perp

            if (self.transportMode is TransportMode.ORDINARY_MODE):
                num = b*sinTheta_sq + 2*eta_perp*eta_par + \
                    math.sqrt(b*b*sinTheta_sq*sinTheta_sq + 4*eta_cross *
                              eta_cross*eta_par*eta_par*cosTheta_sq)
            elif (self.transportMode is TransportMode.EXTRAORDINARY_MODE):
                num = b*sinTheta_sq + 2*eta_perp*eta_par - \
                    math.sqrt(b*b*sinTheta_sq*sinTheta_sq + 4*eta_cross *
                              eta_cross*eta_par*eta_par*cosTheta_sq)
            else:
                logger.warning("TransportMode Model Not Understood")
                raise Exception("TransportMode Model Not Understood")

            denom = 2*(eta_par*sinTheta_sq + eta_par*cosTheta_sq)

            nSq = num/denom

        return (sqrt(nSq))
