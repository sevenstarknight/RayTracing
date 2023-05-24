from xarray import Dataset
import pandas as pd

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
        df : pd.DataFrame = iono.to_dataframe()
        classIri = cls()

        classIri.n_e  = df["ne"].iloc[0]

        classIri.T_n = df["Tn"].iloc[0]
        classIri.T_i = df["Ti"].iloc[0]
        classIri.T_e = df["Te"].iloc[0]

        classIri.nO_Ion = df["nO+"].iloc[0]
        classIri.nH_Ion = df["nH+"].iloc[0] 
        classIri.nHe_Ion = df["nHe+"].iloc[0] 
        classIri.nCI_Ion = df["nCI"].iloc[0]
        classIri.nN_Ion = df["nN+"].iloc[0]

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


    def doesExist(self) -> bool:
        if(self.n_e == -1.0):
            return False
        else:
            return True
