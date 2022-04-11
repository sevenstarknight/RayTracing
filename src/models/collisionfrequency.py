from scipy import constants
import math

# ====================================================
# local imports
from models.msiseoutput_class import MSISEOutput
from models.irioutput_class import IRIOutput

# ====================================================
# constants
eChargeSq = constants.elementary_charge*constants.elementary_charge
k = constants.Boltzmann
pi = constants.pi
euler_mash = 0.5572


class ElectronIonCollisionFrequency():

    def estimateCollisionFreqs(self, iriOutputs: list[IRIOutput]) -> list[float]:
        collisionFreqs = []
        for iriOutput in iriOutputs:
            collisionFreqs.append(self.estimateCollisionFreq(iriOutput))

        return(collisionFreqs)

    def estimateCollisionFreq(self, iriOutput: IRIOutput) -> float:

        n_e = iriOutput.n_e
        n_i = iriOutput.nH_Ion + iriOutput.nHe_Ion + iriOutput.nN_Ion + iriOutput.nO_Ion

        T_e = iriOutput.T_e
        T_i = iriOutput.T_i

        lnLambda_i = self.lnLambda(n_e=n_e, T_e=T_e, n_i=n_i, T_i=T_i)

        return(3.63e-6*n_i*math.pow(T_e, 3/2)*lnLambda_i)

    def lnLambda(self,  n_e: float, T_e: float, n_i: float, T_i: float) -> float:

        kSqr_e = self.estimate_kSqrSube(n_e=n_e, T_e=T_e)
        kSqr_i = self.estimate_kSqrSubi(n_i=n_i, T_i=T_i)

        first = math.log((4*k/(euler_mash*euler_mash*eChargeSq))
                         * (T_e/math.sqrt(kSqr_e)))

        second = ((kSqr_e + kSqr_i)/kSqr_i) * \
            math.log(math.sqrt(kSqr_e + kSqr_i)/math.sqrt(kSqr_e))

        return(first + second)

    def estimate_kSqrSube(self, n_e: float, T_e: float) -> float:
        kSqr_e = (4.0*pi*eChargeSq/k)*(n_e/T_e)
        return(kSqr_e)

    def estimate_kSqrSubi(self, n_i: float, T_i: float) -> float:
        kSqr_e = (4.0*pi*eChargeSq/k)*(n_i/T_i)
        return(kSqr_e)


class ElectronNeutralCollisionFrequency():

    def estimateCollisionFreqs(self, iriOutputs: list[IRIOutput], msiseOutputs: list[MSISEOutput]) -> list[float]:
        collisionFreqs = []
        for idx in range(len(iriOutputs)):
            collisionFreqs.append(self.estimateCollisionFreq(
                iriOutput=iriOutputs.iloc(idx), msiseOutput=msiseOutputs.iloc(idx)))

        return(collisionFreqs)

    def estimateCollisionFreq(self, iriOutput: IRIOutput, msiseOutput: MSISEOutput) -> float:

        veN2 = 2.33e-11*msiseOutput.n2NumDensity * \
            (1 - 1.21e-4*iriOutput.T_e)*iriOutput.T_e

        veO2 = 1.82e-10*msiseOutput.o2NumDensity * \
            (1 + 3.6e-2*math.sqrt(iriOutput.T_e))*math.sqrt(iriOutput.T_e)

        veO = 8.9e-11*msiseOutput.oNumDensity * \
            (1 + 5.7e-4*iriOutput.T_e)*math.sqrt(iriOutput.T_e)

        veHe = 4.6e-10*msiseOutput.heNumDensity*math.sqrt(iriOutput.T_e)

        veH = 4.5e-9*msiseOutput.hNumDensity * \
            (1 - 1.35e-4*iriOutput.T_e)*math.sqrt(iriOutput.T_e)

        return(veN2 + veO2 + veO + veHe + veH)
