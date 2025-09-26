import csv
import io
import pandas as pd





class CSVController:

    PATH_OUT = "utils/Csv/import(13).csv"

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


    




    """metodi upload CSV"""

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


    def upload_csvAPRICA(path):
        pass





    """METODI PER VCS"""

    def uploadCSV_VCS(path):
        
        colonne_da_leggere = [1,5,6,8,9,10,12]

        try:
            with open(path, mode='r', encoding='utf-8') as file:
                
                df = pd.read_csv(file, usecols=colonne_da_leggere)
                
                return df
        except FileNotFoundError:
            print(f"Errore: Il file '{path}' non è stato trovato.")
        except pd.errors.EmptyDataError:
            print(f"Errore: Il file '{path}' è vuoto o non contiene dati validi.")
        except Exception as e:
            print(f"Errore imprevisto: {e}")


    
    


