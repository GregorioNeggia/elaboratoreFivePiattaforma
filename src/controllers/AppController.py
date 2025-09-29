

import pandas as pd


class AppController:

    def __init__(self, csv_controller, config, elab_controller, columns):
        self.csv_controller = csv_controller
        self.config = config
        self.elab_controller = elab_controller
        self.columns = columns





    def apri_elaboratore(self, scelta, root):
        """
        Apre la finestra di elaborazione come Toplevel, nascondendo la root principale.
        Quando il Toplevel viene chiuso, la root viene mostrata di nuovo.
        """
        from tkinter import Toplevel
        from views.ElabView import ElaboratoreView

        # Nascondi la finestra principale
        try:
            root.withdraw()
        except Exception:
            pass

        # Crea una nuova finestra per l'elaboratore
        elab_window = Toplevel(root)
        elab_window.title(f"Elaboratore - {scelta}")
        elab_window.geometry("800x600")

        # Crea la vista dell'elaboratore passando la scelta e il controller
        elab_view = ElaboratoreView(elab_window, scelta, self)

        # Quando l'utente chiude la finestra, mostra di nuovo la root
        def on_close():
            try:
                elab_window.destroy()
            except Exception:
                pass
            try:
                root.deiconify()
            except Exception:
                pass

        elab_window.protocol("WM_DELETE_WINDOW", on_close)

    def apriInfo(self):
        from views.InfoView import InfoView
        InfoView()


    




    def elaborazione(self, nomePa, trasportatore, scelta, pathIn, percentuale=None):
        
        elab_config = self.config["ELABORATORE_CONFIG"].get(scelta)
        if not elab_config:
            raise ValueError(f"Configurazione non trovata per la scelta: {scelta}")

        metodoImportNome = elab_config["import_method"]
        metodoElabNome = elab_config["process_method"]

        metodoImport = getattr(self.csv_controller, metodoImportNome)
        metodoElab = getattr(self.elab_controller, metodoElabNome)

        try:
            df = metodoImport(pathIn)
            dfOut = metodoElab(df, self.columns, nomePa, trasportatore, percentuale if self.config.get("percentuale") is not None else None)
            return dfOut

        except AttributeError as e:
            print(f"Errore: Metodo non trovato - {e}")
        except Exception as e:
            print(f"Errore imprevisto durante l'elaborazione: {e}")
        return None




            
