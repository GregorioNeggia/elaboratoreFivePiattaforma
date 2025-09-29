
from utils.config.configuration import OUTPUT_COLUMNS




import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
import json
from tkinter import filedialog
from controllers.CSVController import CSVController
import os

class ElaboratoreView:
    def __init__(self, root, scelta, AppController):
        self.root = root
        self.scelta = scelta
        self.columns = OUTPUT_COLUMNS
        self.AppController = AppController
        # Window
        self.root.title(f"ELABORATORE - {self.scelta}")
        self.root.geometry("1400x900")
        self.root.configure(bg="#1A1A2E")

        # === Stili (coerenti con mainView) ===
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except Exception:
            pass
        style.configure(
            "BigOrange.TButton",
            font=("Arial", 14, "bold"),
            background="#FF8C00",
            foreground="#16213E",
            relief="raised",
            borderwidth=3,
            padding=8
        )
        style.map(
            "BigOrange.TButton",
            background=[("active", "#FF6B35")],
            foreground=[("active", "#16213E")]
        )
        # Treeview heading style
        try:
            style.configure("Treeview.Heading", font=("Arial", 10, "bold"))
            style.configure("Treeview", rowheight=24)
        except Exception:
            pass

        # Frame principale (sfondo scuro)
        self.main_frame = tk.Frame(self.root, bg="#16213E", padx=20, pady=20)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Titolo
        self.title_label = tk.Label(
            self.main_frame,
            text=f"ELABORATORE\n{self.scelta}",
            font=("Arial", 24, "bold"),
            fg="#FF8C00",
            bg="#16213E",
            justify="center"
        )
        self.title_label.pack(pady=(0, 16), fill=tk.X)

        # Frame bottoni
        self.button_frame = tk.Frame(self.main_frame, bg="#16213E")
        self.button_frame.pack(pady=(0, 16))

        self.import_btn = ttk.Button(self.button_frame, text="IMPORTA", command=self.importa, style="BigOrange.TButton")
        self.import_btn.grid(row=0, column=0, padx=10)

        self.export_btn = ttk.Button(self.button_frame, text="ESPORTA", command=self.esporta, style="BigOrange.TButton")
        self.export_btn.grid(row=0, column=1, padx=10)

        # Label tabella
        self.table_label = tk.Label(self.main_frame, text="ANTEPRIMA ESPORTAZIONE", font=("Arial", 12, "bold"), fg="#E0E0E0", bg="#16213E")
        self.table_label.pack(pady=(10, 6))

        # Tabella (Treeview)
        table_container = tk.Frame(self.main_frame, bg="#16213E")
        table_container.pack(fill=tk.BOTH, expand=True)

        self.table = ttk.Treeview(table_container, columns=self.columns, show="headings", height=12)
        for col in self.columns:
            self.table.heading(col, text=col)
            self.table.column(col, width=120, anchor=tk.CENTER)
        self.table.pack(fill=tk.BOTH, expand=True)




    def importa(self):
        self.chiediInfo(self.elabConInfo, self.scelta)

    def elabConInfo(self, nome_pa, trasportatore, percentuale):
        file_path = filedialog.askopenfilename(
            title="Seleziona il file da importare",
            filetypes=[("File CSV", "*.csv"), ("Tutti i file", "*.*")]
        )
        if not file_path:
            messagebox.showwarning("Attenzione", "Nessun file selezionato.")
            return

        try:
            # Chiama il metodo di elaborazione passando il file selezionato
            df = self.AppController.elaborazione(nome_pa, trasportatore, self.scelta, file_path, percentuale)
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

        

    def chiediInfo(self, callback, scelta):
        nome_pa = simpledialog.askstring("Nome PA", "Inserisci il Nome PA:", parent=self.root)
        if not nome_pa:
            messagebox.showwarning("Attenzione", "Nome PA obbligatorio.")
            return

        try:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            trasportatori_path = os.path.join(base_dir, "..", "utils", "Db", "Trasportatori.json")
            trasportatori_path = os.path.normpath(trasportatori_path)
            with open(trasportatori_path, encoding="utf-8") as f:
                trasportatori = json.load(f)
        except Exception as e:
            messagebox.showerror("Errore", f"Errore caricamento trasportatori: {e}")
            return

        selezione = tk.Toplevel(self.root)
        selezione.title("Seleziona Trasportatore")
        selezione.geometry("600x500")
        # rendi la finestra modale per evitare interazioni con la root
        try:
            selezione.transient(self.root)
            selezione.grab_set()
        except Exception:
            pass

        label = ttk.Label(selezione, text="Seleziona il trasportatore:")
        label.pack(pady=10)

        trasportatori_nomi = [t["nome"] for t in trasportatori]
        trasportatore_var = tk.StringVar(value=trasportatori_nomi[0] if trasportatori_nomi else "")

        combo = ttk.Combobox(selezione, values=trasportatori_nomi, textvariable=trasportatore_var, state="readonly")
        combo.pack(pady=10)
        print(scelta)

        def conferma():
            selezionato_nome = combo.get()
            if not selezionato_nome:
                messagebox.showwarning("Attenzione", "Seleziona un trasportatore.")
                return
            selezionato = next((t for t in trasportatori if t["nome"] == selezionato_nome), None)

            # Se la scelta richiede una percentuale, chiedila ora
            percentuale = 1
            if scelta == "GECO":
                try:
                    needs_percentuale = messagebox.askyesno("Percentuale", "Hai bisogno di inserire la percentuale?", parent=selezione)
                    if needs_percentuale:
                        percentuale = simpledialog.askfloat(
                            "Percentuale",
                            "Inserisci la percentuale (es. 10 per 10%):",
                            parent=selezione,
                            minvalue=0,
                            maxvalue=100
                        )
                        print(f"Percentuale inserita: {percentuale}")
                except Exception as e:
                    print(f"Errore richiesta percentuale: {e}")
            selezione.destroy()
            if selezionato:
                try:
                    callback(nome_pa, selezionato, percentuale)
                except TypeError:
                    callback(nome_pa, selezionato)
            else:
                messagebox.showerror("Errore", "Trasportatore non trovato.")

        btn = ttk.Button(selezione, text="Conferma", command=conferma)
        btn.pack(pady=20)

    def esporta(self):
        CSVController.esporta(self.table)




    
        



