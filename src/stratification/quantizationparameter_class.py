from src.stratification.stratificationmethod_enum import StratificationMethod


class QuantizationParameter():
    def __init__(self, stratificationMethod: StratificationMethod, nQuant: int = None, epsilon : float = None):
        self.stratificationMethod = stratificationMethod
        self.nQuant = nQuant
        self.epsilon = epsilon