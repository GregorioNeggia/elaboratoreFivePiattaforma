
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
        # Palette coerente con ElaboratoreView
        BG_ROOT = "#1A1A2E"
        BG_FRAME = "#16213E"
        FG_TEXT = "#E0E0E0"
        ACCENT = "#FF8C00"
        ACCENT_ACTIVE = "#FF6B35"
        INPUT_BG = "#0F1A2E"
        INPUT_FG = "#EAEAEA"
        PRIMARY = "#1F6FB2"

        # === DIALOG NOME PA ===
        nome_pa_result = [None]  # lista per catturare il valore nel closure

        dialog_pa = tk.Toplevel(self.root)
        dialog_pa.title("Nome PA")
        dialog_pa.geometry("420x200")
        dialog_pa.configure(bg=BG_FRAME)
        dialog_pa.transient(self.root)
        dialog_pa.grab_set()

        frame_pa = tk.Frame(dialog_pa, bg=BG_FRAME)
        frame_pa.pack(fill="both", expand=True, padx=20, pady=20)

        tk.Label(frame_pa, text="Inserisci il Nome PA:", font=("Arial", 11), fg=FG_TEXT, bg=BG_FRAME).pack(anchor="w", pady=(0, 10))

        entry_pa = tk.Entry(frame_pa, font=("Arial", 11), bg=INPUT_BG, fg=INPUT_FG, insertbackground=INPUT_FG, relief="flat", borderwidth=2)
        entry_pa.pack(fill="x", ipady=6)
        entry_pa.focus_set()

        footer_pa = tk.Frame(frame_pa, bg=BG_FRAME)
        footer_pa.pack(fill="x", pady=(20, 0))
        spacer_pa = tk.Frame(footer_pa, bg=BG_FRAME)
        spacer_pa.pack(side="left", expand=True)

        def conferma_pa():
            val = entry_pa.get().strip()
            if not val:
                messagebox.showwarning("Attenzione", "Nome PA obbligatorio.", parent=dialog_pa)
                return
            nome_pa_result[0] = val
            dialog_pa.destroy()

        def annulla_pa():
            dialog_pa.destroy()

        btn_annulla_pa = tk.Button(footer_pa, text="Annulla", font=("Arial", 10, "bold"), bg=BG_FRAME, fg=FG_TEXT, activebackground=BG_FRAME, activeforeground=ACCENT, relief="flat", command=annulla_pa)
        btn_annulla_pa.pack(side="right", padx=(0, 10))

        btn_ok_pa = tk.Button(footer_pa, text="Conferma", font=("Arial", 10, "bold"), bg=ACCENT, fg="#16213E", activebackground=ACCENT_ACTIVE, activeforeground="#16213E", relief="raised", borderwidth=2, command=conferma_pa)
        btn_ok_pa.pack(side="right", ipadx=10, ipady=4)

        entry_pa.bind("<Return>", lambda e: conferma_pa())
        dialog_pa.wait_window()

        nome_pa = nome_pa_result[0]
        if not nome_pa:
            return

        # === CARICA TRASPORTATORI ===
        try:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            trasportatori_path = os.path.normpath(os.path.join(base_dir, "..", "utils", "Db", "Trasportatori.json"))
            with open(trasportatori_path, encoding="utf-8") as f:
                trasportatori = json.load(f)
        except Exception as e:
            messagebox.showerror("Errore", f"Errore caricamento trasportatori: {e}", parent=self.root)
            return

        # === DIALOG TRASPORTATORE ===
        selezione = tk.Toplevel(self.root)
        selezione.title("Seleziona Trasportatore")
        selezione.geometry("500x400")
        selezione.configure(bg=BG_FRAME)
        selezione.transient(self.root)
        selezione.grab_set()

        style = ttk.Style(selezione)
        try:
            style.theme_use("clam")
        except:
            pass

        # Stili ttk
        style.configure("Dark.TCombobox", fieldbackground=INPUT_BG, background=INPUT_BG, foreground=INPUT_FG, arrowcolor=INPUT_FG, bordercolor=PRIMARY, lightcolor=PRIMARY, darkcolor=BG_FRAME)
        style.map("Dark.TCombobox", fieldbackground=[("readonly", INPUT_BG)], foreground=[("readonly", INPUT_FG)], bordercolor=[("focus", PRIMARY)])
        
        selezione.option_add("*TCombobox*Listbox*Background", BG_FRAME)
        selezione.option_add("*TCombobox*Listbox*Foreground", FG_TEXT)
        selezione.option_add("*TCombobox*Listbox*selectBackground", ACCENT)
        selezione.option_add("*TCombobox*Listbox*selectForeground", "#16213E")

        container = tk.Frame(selezione, bg=BG_FRAME)
        container.pack(fill="both", expand=True, padx=20, pady=20)

        tk.Label(container, text="Seleziona il trasportatore", font=("Arial", 13, "bold"), fg=ACCENT, bg=BG_FRAME).pack(anchor="w")

        tk.Label(container, text="Trasportatore", font=("Arial", 10), fg=FG_TEXT, bg=BG_FRAME).pack(anchor="w", pady=(16, 6))
        trasportatori_nomi = [t.get("nome", "") for t in trasportatori]
        trasportatore_var = tk.StringVar(value=trasportatori_nomi[0] if trasportatori_nomi else "")
        combo = ttk.Combobox(container, values=trasportatori_nomi, textvariable=trasportatore_var, state="readonly", style="Dark.TCombobox")
        combo.pack(fill="x")

        # Campo percentuale solo per GECO
        percent_var = tk.StringVar(value="")
        percent_entry = None

        def validate_percent(newval):
            if newval.strip() == "":
                return True
            try:
                v = float(newval.replace(",", "."))
                return 0 <= v <= 100
            except:
                return False

        if scelta == "GECO":
            tk.Label(container, text="Percentuale (0–100)", font=("Arial", 10), fg=FG_TEXT, bg=BG_FRAME).pack(anchor="w", pady=(16, 6))
            vcmd = (selezione.register(validate_percent), "%P")
            percent_entry = tk.Entry(container, textvariable=percent_var, font=("Arial", 11), bg=INPUT_BG, fg=INPUT_FG, insertbackground=INPUT_FG, relief="flat", validate="key", validatecommand=vcmd)
            percent_entry.insert(0, "10")
            percent_entry.pack(fill="x", ipady=6)
            tk.Label(container, text="Lascia vuoto per 1 (nessuna variazione)", font=("Arial", 9), fg="#999", bg=BG_FRAME).pack(anchor="w", pady=(6, 0))

        footer = tk.Frame(container, bg=BG_FRAME)
        footer.pack(fill="x", pady=(20, 0))
        spacer = tk.Frame(footer, bg=BG_FRAME)
        spacer.pack(side="left", expand=True)

        def conferma():
            selezionato_nome = combo.get().strip()
            if not selezionato_nome:
                messagebox.showwarning("Attenzione", "Seleziona un trasportatore.", parent=selezione)
                return
            selezionato = next((t for t in trasportatori if t.get("nome", "") == selezionato_nome), None)
            if not selezionato:
                messagebox.showerror("Errore", "Trasportatore non trovato.", parent=selezione)
                return

            percentuale = 1
            if scelta == "GECO":
                txt = percent_var.get().strip()
                if txt:
                    try:
                        val = float(txt.replace(",", "."))
                        if not (0 <= val <= 100):
                            raise ValueError
                        percentuale = val
                    except:
                        messagebox.showerror("Errore", "Percentuale non valida (0-100).", parent=selezione)
                        return

            selezione.destroy()
            try:
                callback(nome_pa, selezionato, percentuale)
            except TypeError:
                callback(nome_pa, selezionato)

        def annulla():
            selezione.destroy()

        btn_annulla = tk.Button(footer, text="Annulla", font=("Arial", 10, "bold"), bg=BG_FRAME, fg=FG_TEXT, activebackground=BG_FRAME, activeforeground=ACCENT, relief="flat", command=annulla)
        btn_annulla.pack(side="right", padx=(0, 10))

        btn_ok = tk.Button(footer, text="Conferma", font=("Arial", 10, "bold"), bg=ACCENT, fg="#16213E", activebackground=ACCENT_ACTIVE, activeforeground="#16213E", relief="raised", borderwidth=2, command=conferma)
        btn_ok.pack(side="right", ipadx=10, ipady=4)

        if scelta == "GECO" and percent_entry:
            percent_entry.focus_set()
        else:
            combo.focus_set()

    def esporta(self):
        CSVController.esporta(self.table)




    
        



