import numpy as np

from src.models.nequick.nequickg_model import NequickG_bottomside, NequickG_parameters, NequickG_topside

class NequickG:
    def __init__(self, parameters: NequickG_parameters):
        # self.Para = parameters
        self.hmF2 = parameters.hmF2
        topside_para = parameters.topside_para()
        bottomside_para = parameters.bottomside_para()
        self.topside = NequickG_topside(*topside_para)
        self.bottomside = NequickG_bottomside(*bottomside_para)

    def electrondensity(self, h):
        """

        :param h: [km]
        :return: electron density [m^-3]
        """
        h = np.array(h)

        mask1 = h < self.hmF2
        mask2 = np.logical_not(mask1)

        h_bot = h[mask1]
        h_top = h[mask2]

        N = np.empty(np.shape(h))

        N[mask1] = self.bottomside.electrondensity(h_bot)
        N[mask2] = self.topside.electrondensity(h_top)

        assert (not np.any(N < 0))

        return N

    def vTEC(self, h1, h2, tolerance=None):
        """
        Vertical TEC numerical Integration
        :param h1: integration lower endpoint
        :param h2: integration higher endpoint
        :param tolerance:
        :return:
        """

        assert (h2 > h1)

        if tolerance == None:
            if h1 < 1000:
                tolerance = 0.001
            else:
                tolerance = 0.01

        n = 8

        GN1 = self.__single_quad(h1, h2, n)
        n *= 2
        GN2 = self.__single_quad(h1, h2, n)  # TODO: there is repeated work here. can be optimized

        count = 1
        while (abs(GN2 - GN1) > tolerance * abs(GN1)) and count < 20:
            GN1 = GN2
            n *= 2
            GN2 = self.__single_quad(h1, h2, n)
            count += 1

        if count == 20:
            print("vTEC integration did not converge")

        return (GN2 + (GN2 - GN1) / 15.0)


    def vTEC_ratio(self):
        bot = self.vTEC(0, self.hmF2)
        top = self.vTEC(self.hmF2, 20000)

        return top / bot

    def __single_quad(self, h1, h2, n):

        delta = float(h2 - h1) / n

        g = .5773502691896 * delta  # delta / sqrt(3)
        y = h1 + (delta - g) / 2.0

        h = np.empty(2 * n)
        I = np.arange(n)
        h[0::2] = y + I * delta
        h[1::2] = y + I * delta + g
        N = self.electrondensity(h)
        GN = delta / 2.0 * np.sum(N)

        return GN