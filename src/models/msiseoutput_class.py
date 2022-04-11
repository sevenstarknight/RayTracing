class MSISEOutput():

    '''
    The output has the same order as the C reference code, in particular:

    d[0] - He number density [cm⁻³]
    d[1] - O number density [cm⁻³]
    d[2] - N2 number density [cm⁻³]
    d[3] - O2 number density [cm⁻³]
    d[4] - Ar number density [cm⁻³]
    d[5] - total mass density [g cm⁻³]) (includes d[8] in gtd7d())
    d[6] - H number density [cm⁻³]
    d[7] - N number density [cm⁻³]
    d[8] - Anomalous oxygen number density [cm⁻³]
    t[0] - exospheric temperature [K]
    t[1] - temperature at alt [K]
    '''

    def __init__(self, d: list, t: list):
        self.heNumDensity = d[0]
        self.oNumDensity = d[1]
        self.n2NumDensity = d[2]
        self.o2NumDensity = d[3]
        self.arNumDensity = d[4]
        self.totalMass = d[5]
        self.hNumDensity = d[6]
        self.nNumDensity = d[7]
        self.anomONumDensity = d[8]

        self.exoTemp = t[0]
        self.tmpAtAlt = t[1]
