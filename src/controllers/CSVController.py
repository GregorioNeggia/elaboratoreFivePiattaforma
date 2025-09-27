import csv
import io
import pandas as pd
import json

PATH_OUT = "utils/Csv/import(13).csv"
PATH_TRASP = "utils/Db/Trasportatori.json"

class CSVController:

    

    def __init__(self, csv_service):
        self.csv_service = csv_service

    

    def uploadOutput(self):
        try:
            with open(self.PATH_OUT, mode='r', encoding='utf-8') as file:
                df = pd.read_csv(file)
                return df
        except FileNotFoundError:
            print(f"Errore: Il file '{self.PATH_OUT}' non è stato trovato.")
        except pd.errors.EmptyDataError:
            print(f"Errore: Il file '{self.PATH_OUT}' è vuoto o non contiene dati validi.")
        except Exception as e:
            print(f"Errore imprevisto: {e}")

            

    def caricaTrasp(PATH_TRASP, idTrasp):
        try:
            with open(PATH_TRASP, 'r', encoding='utf-8') as file:
                data = json.load(file)
                for item in data:
                    if item['id'] == idTrasp:
                        print(f"Trasportatore con id '{idTrasp}' trovato: {item}")
                        return item
                    else:
                        print(f"Trasportatore con id '{idTrasp}' non trovato.")
                return None
        except FileNotFoundError:
            print(f"Errore: Il file '{PATH_TRASP}' non è stato trovato.")
        except json.JSONDecodeError:
            print(f"Errore: Il file '{PATH_TRASP}' non contiene JSON valido.")
        except Exception as e:
            print(f"Errore imprevisto: {e}")
        return None
    

    
    

    

    """CARICAMENTI CSV"""




    """METODI PER GECO"""
    def upload_csvGECO(path):
        try:
            with open(path, mode='r', encoding='utf-8') as file:
                csv_reader = csv.reader(file)
                data = [row for row in csv_reader]
                return pd.DataFrame(data[1:], columns=data[0])
        except FileNotFoundError:
            print(f"Errore: Il file '{path}' non è stato trovato.")
        except pd.errors.EmptyDataError:
            print(f"Errore: Il file '{path}' è vuoto o non contiene dati validi.")
        except Exception as e:
            print(f"Errore imprevisto: {e}")

    






    """METODI PER APRICA"""
    def upload_csvAPRICA(path):
        pass





    """METODI PER VCS"""
    @staticmethod
    def uploadCSV_VCS(path):
        
        colonne_da_leggere = [1,5,6,8,9,10,12]

        try:
            with open(path, mode='r', encoding='utf-8') as file:
                
                df = pd.read_csv(file, usecols=colonne_da_leggere)

                df['CDR'] = df.iloc[:, 0].apply(lambda x: 1 if "Centro raccolta" in str(x) else 0)

                return df
        except FileNotFoundError:
            print(f"Errore: Il file '{path}' non è stato trovato.")
        except pd.errors.EmptyDataError:
            print(f"Errore: Il file '{path}' è vuoto o non contiene dati validi.")
        except Exception as e:
            print(f"Errore imprevisto: {e}")





    """METODI PER ALTRO"""
    @staticmethod
    def upload_csvALTRO(path):
        pass


    """METODO EXPORT CSV"""
    @staticmethod
    def exportCSV(dfOut, Path):
        try:
            dfOut.to_csv(Path, index=False, header=False, sep=';')
            print(f"File CSV esportato con successo in '{Path}'")
        except Exception as e:
            print(f"Errore durante l'esportazione del file CSV: {e}")
    


