
from utils.config.configuration import OUTPUT_COLUMNS




import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
import json
from tkinter import filedialog
from controllers.CSVController import CSVController

class ElaboratoreView:
    def __init__(self, root, scelta, AppController):
        self.root = root
        self.scelta = scelta
        self.columns = OUTPUT_COLUMNS
        self.AppController = AppController

        self.root.title(f"ELABORATORE - {self.scelta}")
        self.root.geometry("1000x500")

        # Frame principale
        self.main_frame = ttk.Frame(self.root, padding="20")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Label titolo
        self.title_label = ttk.Label(self.main_frame, text=f"ELABORATORE \n {self.scelta}", font=("Arial", 18, "bold"), anchor="center", justify="center")
        self.title_label.pack(pady=(0, 20), fill=tk.X)

        # Frame bottoni
        self.button_frame = ttk.Frame(self.main_frame)
        self.button_frame.pack(pady=(0, 20))

        self.import_btn = ttk.Button(self.button_frame, text="IMPORTA", command=self.importa)
        self.import_btn.grid(row=0, column=0, padx=10)

        self.export_btn = ttk.Button(self.button_frame, text="ESPORTA", command=self.esporta)
        self.export_btn.grid(row=0, column=1, padx=10)

        # Label tabella
        self.table_label = ttk.Label(self.main_frame, text="ANTEPRIMA ESPORTAZIONE", font=("Arial", 12, "bold"))
        self.table_label.pack(pady=(10, 5))

        # Tabella (Treeview)
        self.table = ttk.Treeview(self.main_frame, columns=self.columns, show="headings", height=10)
        for col in self.columns:
            self.table.heading(col, text=col)
            self.table.column(col, width=100, anchor=tk.CENTER)
        self.table.pack(fill=tk.BOTH, expand=True)




    def importa(self):
        self.chiediInfo(self.elabConInfo)

    def elabConInfo(self, nome_pa, trasportatore):
        file_path = filedialog.askopenfilename(
            title="Seleziona il file da importare",
            filetypes=[("File CSV", "*.csv"), ("Tutti i file", "*.*")]
        )
        if not file_path:
            messagebox.showwarning("Attenzione", "Nessun file selezionato.")
            return

        try:
            # Chiama il metodo di elaborazione passando il file selezionato
            df = self.AppController.elaborazione(nome_pa, trasportatore, self.scelta, file_path)
            # Svuota la tabella
            for row in self.table.get_children():
                self.table.delete(row)
            # Inserisci nuovi dati (assumendo df è un DataFrame)
            if df is not None:
                for _, riga in df.iterrows():
                    values = [riga.get(col, "") if hasattr(riga, 'get') else riga[col] for col in self.columns]
                    self.table.insert("", tk.END, values=values)
            else:
                messagebox.showwarning("Attenzione", "Nessun dato elaborato.")
        except Exception as e:
            messagebox.showerror("Errore", f"Errore durante l'elaborazione: {e}")

        def debug_stampa_colonne(self, dfOut):
            print("Colonne dfOut:", list(dfOut.columns))

    def chiediInfo(self, callback):
        nome_pa = simpledialog.askstring("Nome PA", "Inserisci il Nome PA:", parent=self.root)
        if not nome_pa:
            messagebox.showwarning("Attenzione", "Nome PA obbligatorio.")
            return

        try:
            with open("src/utils/Db/Trasportatori.json", encoding="utf-8") as f:
                trasportatori = json.load(f)
        except Exception as e:
            messagebox.showerror("Errore", f"Errore caricamento trasportatori: {e}")
            return

        selezione = tk.Toplevel(self.root)
        selezione.title("Seleziona Trasportatore")
        selezione.geometry("400x300")

        label = ttk.Label(selezione, text="Seleziona il trasportatore:")
        label.pack(pady=10)

        trasportatori_nomi = [t["nome"] for t in trasportatori]
        trasportatore_var = tk.StringVar(value=trasportatori_nomi[0] if trasportatori_nomi else "")

        combo = ttk.Combobox(selezione, values=trasportatori_nomi, textvariable=trasportatore_var, state="readonly")
        combo.pack(pady=10)

        def conferma():
            selezionato_nome = combo.get()
            if not selezionato_nome:
                messagebox.showwarning("Attenzione", "Seleziona un trasportatore.")
                return
            selezionato = next((t for t in trasportatori if t["nome"] == selezionato_nome), None)
            selezione.destroy()
            if selezionato:
                callback(nome_pa, selezionato)
            else:
                messagebox.showerror("Errore", "Trasportatore non trovato.")

        btn = ttk.Button(selezione, text="Conferma", command=conferma)
        btn.pack(pady=20)

    def esporta(self):
        CSVController.esporta(self.table)




    
        



