import numpy as np

class Quantization():
    def __init__(self, representationPoints: np.array, intervalEndPoints : np.array, denominator: np.array):
        self.representationPoints = representationPoints
        self.intervalEndPoints = intervalEndPoints
        self.denominator = denominator