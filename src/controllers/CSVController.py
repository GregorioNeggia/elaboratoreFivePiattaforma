import csv
import io
import pandas as pd





class CSVController:


    def __init__(self, csv_service):
        self.csv_service = csv_service




    def upload_csv(path):
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


    


