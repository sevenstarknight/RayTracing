from xarray import Dataset


class IRIOutput():

    def __init__(self):
        self.n_e: float = 0
        self.T_n: float = 0
        self.T_i: float = 0
        self.T_e: float = 0

        self.nO_Ion: float = 0
        self.nH_Ion: float = 0
        self.nHe_Ion: float = 0
        self.nCI_Ion: float = 0
        self.nN_Ion: float = 0

    @classmethod
    def from_xarray(cls, iono: Dataset):
        df = iono.to_dataframe()
        classIri = cls()


        ne_1 = df["ne"].iloc[0].item()
        ne_2 = df["ne"].iloc[1].item()

        # forward/backward mean estimate
        if ne_1 < 0 and ne_2 > 0:
            classIri.n_e = ne_2
        elif ne_1 > 0 and ne_2 < 0:
            classIri.n_e = ne_1
        else:
            classIri.n_e = (ne_2 + ne_1)/2.0

        classIri.T_n = (df["Tn"].iloc[0].item()+df["Tn"].iloc[1].item())/2
        classIri.T_i = (df["Ti"].iloc[0].item()+df["Ti"].iloc[1].item())/2
        classIri.T_e = (df["Te"].iloc[0].item()+df["Te"].iloc[0].item())/2

        classIri.nO_Ion = (df["nO+"].iloc[0].item() +
                           df["nO+"].iloc[0].item())/2
        classIri.nH_Ion = (df["nH+"].iloc[0].item() +
                           df["nH+"].iloc[0].item())/2
        classIri.nHe_Ion = (df["nHe+"].iloc[0].item() +
                            df["nHe+"].iloc[0].item())/2
        classIri.nCI_Ion = (df["nCI"].iloc[0].item() +
                            df["nCI"].iloc[0].item())/2
        classIri.nN_Ion = (df["nN+"].iloc[0].item() +
                           df["nN+"].iloc[0].item())/2

        return(classIri)

    # 'ne', 'Tn', 'Ti', 'Te', 'nO+', 'nH+', 'nHe+', 'nCI', 'nN+'
    @classmethod
    def from_empty(cls):
        classIri = cls()

        classIri.n_e = -1.0

        classIri.T_n = -1.0
        classIri.T_i = -1.0
        classIri.T_e = -1.0

        classIri.nO_Ion = -1.0
        classIri.nH_Ion = -1.0
        classIri.nHe_Ion = -1.0
        classIri.nCI_Ion = -1.0
        classIri.nN_Ion = -1.0

        return classIri
