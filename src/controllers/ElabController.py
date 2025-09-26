
import csv
from datetime import datetime
import pandas as pd

class ElabController:

    

    def __init__(self, elab_service):
        self.elab_service = elab_service













    """METODI PER VCS"""
    def elabVCS(self, df, dfOut, nomePa, trasportatore):
        try:
            for index, row in df.iterrows():

                dfOut.loc[index, 0] = "Comune di " + nomePa
                dfOut.loc[index, 1] = row[2]
                dfOut.loc[index, 2] = row[1]
                dfOut.loc[index, 3] = trasportatore["nome"]
                dfOut.loc[index, 4] = row[6]
                dfOut.loc[index, 5] = row[5]
                dfOut.loc[index, 6] = row[4]
                dfOut.loc[index, 7] = row[3]

                if df.loc[index, 7] == "1":
                    dfOut.loc[index, 8] = "Comune di " + nomePa + ("(CDR)")
                else:
                    dfOut.loc[index, 8] = "Comune di " + nomePa + ("(M)")
            
            return dfOut

        except Exception as e:
            print(f"Errore imprevisto durante l'elaborazione VCS: {e}")
            return None