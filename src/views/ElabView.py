# views/elaboratore_view.py
import json
import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

from utils.ui.theme_colors import ThemeColors
from utils.config.configuration import OUTPUT_COLUMNS
from controllers.CSVController import CSVController


class ElaboratoreView:
    """Schermata di elaborazione CSV con dialog moderni."""

    def __init__(self, root, scelta, app_controller):
        self.root           = root
        self.scelta         = scelta
        self.app_controller = app_controller
        self.columns        = OUTPUT_COLUMNS

        self._init_window()
        self._setup_style()
        self._build_layout()

    def _init_window(self):
        self.root.title(f"ELABORATORE – {self.scelta}")
        self.root.geometry("1400x900")
        self.root.configure(bg=ThemeColors.BACKGROUND)

    def _setup_style(self):
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except Exception:
            pass

        # ═══ CONFIGURAZIONE GLOBALE COMBOBOX PER LEGGIBILITÀ ═══
        # Imposta le opzioni globali per tutti i Combobox dropdown
        self.root.tk.call("option", "add", "*TCombobox*Listbox.background", "#0F1A2E")
        self.root.tk.call("option", "add", "*TCombobox*Listbox.foreground", ThemeColors.WHITE)
        self.root.tk.call("option", "add", "*TCombobox*Listbox.selectBackground", ThemeColors.ORANGE)
        self.root.tk.call("option", "add", "*TCombobox*Listbox.selectForeground", ThemeColors.MAIN_BG)
        self.root.tk.call("option", "add", "*TCombobox*Listbox.font", "Arial 12 normal")

        style.configure(
            "BigOrange.TButton",
            font=("Arial", 14, "bold"),
            background=ThemeColors.ORANGE,
            foreground=ThemeColors.MAIN_BG,
            relief="raised",
            borderwidth=3,
            padding=8,
        )
        style.map(
            "BigOrange.TButton",
            background=[("active", ThemeColors.ORANGE_ACTIVE)],
            foreground=[("active", ThemeColors.MAIN_BG)],
        )

        style.configure("Treeview.Heading", font=("Arial", 10, "bold"))
        style.configure("Treeview", rowheight=24)

    def _build_layout(self):
        main = tk.Frame(self.root, bg=ThemeColors.MAIN_BG, padx=20, pady=20)
        main.pack(fill=tk.BOTH, expand=True)

        tk.Label(
            main,
            text=f"ELABORATORE\n{self.scelta}",
            font=("Arial", 24, "bold"),
            fg=ThemeColors.ORANGE,
            bg=ThemeColors.MAIN_BG,
            justify="center",
        ).pack(pady=(0, 16), fill=tk.X)

        btn_frame = tk.Frame(main, bg=ThemeColors.MAIN_BG)
        btn_frame.pack(pady=(0, 16))

        ttk.Button(btn_frame, text="IMPORTA", style="BigOrange.TButton",
                   command=self.importa).grid(row=0, column=0, padx=10)
        ttk.Button(btn_frame, text="ESPORTA", style="BigOrange.TButton",
                   command=self.esporta).grid(row=0, column=1, padx=10)
        ttk.Button(btn_frame, text="REFRESH", style="BigOrange.TButton",
                   command=self.refresh).grid(row=0, column=2, padx=10)

        tk.Label(
            main,
            text="ANTEPRIMA ESPORTAZIONE",
            font=("Arial", 12, "bold"),
            fg=ThemeColors.LIGHT_GRAY,
            bg=ThemeColors.MAIN_BG,
        ).pack(pady=(10, 6))

        container = tk.Frame(main, bg=ThemeColors.MAIN_BG)
        container.pack(fill=tk.BOTH, expand=True)

        self.table = ttk.Treeview(
            container, columns=self.columns, show="headings", height=12
        )
        for col in self.columns:
            self.table.heading(col, text=col)
            self.table.column(col, width=120, anchor=tk.CENTER)
        self.table.pack(fill=tk.BOTH, expand=True)

    def importa(self):
        self._dialog_flow(self._esegui_elaborazione, self.scelta)

    def esporta(self):
        CSVController.esporta(self.table)

    def refresh(self):
        """Svuota tabella e rilancia importazione."""
        self.table.delete(*self.table.get_children())
        self.importa()

    def _esegui_elaborazione(self, nome_pa, trasportatore, percentuale):
        file_path = filedialog.askopenfilename(
            title="Seleziona il file da importare",
            filetypes=[("File CSV", "*.csv"), ("Tutti i file", "*.*")],
        )
        if not file_path:
            messagebox.showwarning("Attenzione", "Nessun file selezionato.")
            return

        try:
            df = self.app_controller.elaborazione(
                nome_pa, trasportatore, self.scelta, file_path, percentuale
            )
            self.table.delete(*self.table.get_children())
            if df is not None:
                for _, row in df.iterrows():
                    self.table.insert(
                        "", tk.END, values=[row.get(col, "") for col in self.columns]
                    )
            else:
                messagebox.showwarning("Attenzione", "Nessun dato elaborato.")
        except Exception as exc:
            messagebox.showerror("Errore", f"Errore durante l'elaborazione:\n{exc}")

    def _dialog_flow(self, callback, scelta):
        nome_pa = self._dialog_nome_pa()
        if not nome_pa:
            return

        try:
            trasportatori = self._carica_trasportatori()
        except Exception as exc:
            messagebox.showerror("Errore", f"Errore caricamento trasportatori:\n{exc}")
            return

        result = self._dialog_trasportatore(scelta, trasportatori)
        if not result:
            return
        trasportatore, percentuale = result
        callback(nome_pa, trasportatore, percentuale)

    def _dialog_nome_pa(self):
        dlg = tk.Toplevel(self.root)
        dlg.title("Nome PA")
        dlg.geometry("480x220")
        dlg.configure(bg=ThemeColors.MAIN_BG)
        dlg.transient(self.root)
        dlg.grab_set()
        dlg.resizable(False, False)

        # Centra finestra
        dlg.update_idletasks()
        x = self.root.winfo_x() + (self.root.winfo_width() // 2) - (dlg.winfo_width() // 2)
        y = self.root.winfo_y() + (self.root.winfo_height() // 2) - (dlg.winfo_height() // 2)
        dlg.geometry(f"+{x}+{y}")

        main = tk.Frame(dlg, bg=ThemeColors.MAIN_BG)
        main.pack(fill="both", expand=True, padx=30, pady=30)

        tk.Label(
            main,
            text="Inserisci Nome PA",
            font=("Arial", 16, "bold"),
            fg=ThemeColors.ORANGE,
            bg=ThemeColors.MAIN_BG,
        ).pack(anchor="w", pady=(0, 20))

        entry_var = tk.StringVar()
        entry = tk.Entry(
            main,
            textvariable=entry_var,
            font=("Arial", 13),
            bg="#0F1A2E",
            fg=ThemeColors.WHITE,
            insertbackground=ThemeColors.ORANGE,
            relief="flat",
            borderwidth=0,
        )
        entry.pack(fill="x", ipady=10)
        entry.focus_set()

        footer = tk.Frame(main, bg=ThemeColors.MAIN_BG)
        footer.pack(fill="x", pady=(30, 0))

        def conferma():
            val = entry_var.get().strip()
            if not val:
                messagebox.showwarning("Attenzione", "Nome PA obbligatorio.", parent=dlg)
                return
            dlg.result = val
            dlg.destroy()

        def annulla():
            dlg.result = None
            dlg.destroy()

        tk.Button(
            footer,
            text="Annulla",
            font=("Arial", 11, "bold"),
            bg=ThemeColors.ORANGE,
            fg=ThemeColors.MAIN_BG,
            activebackground=ThemeColors.ORANGE_ACTIVE,
            activeforeground=ThemeColors.MAIN_BG,
            relief="flat",
            borderwidth=0,
            command=annulla,
        ).pack(side="right", padx=(10, 0), ipadx=12, ipady=6)

        tk.Button(
            footer,
            text="Conferma",
            font=("Arial", 11, "bold"),
            bg=ThemeColors.ORANGE,
            fg=ThemeColors.MAIN_BG,
            activebackground=ThemeColors.ORANGE_ACTIVE,
            activeforeground=ThemeColors.MAIN_BG,
            relief="flat",
            borderwidth=0,
            command=conferma,
        ).pack(side="right", ipadx=16, ipady=6)

        entry.bind("<Return>", lambda e: conferma())
        entry.bind("<Escape>", lambda e: annulla())

        dlg.wait_window()
        return getattr(dlg, "result", None)

    def _dialog_trasportatore(self, scelta, trasportatori):
        dlg = tk.Toplevel(self.root)
        dlg.title("Seleziona Trasportatore")
        dlg.geometry("560x480")
        dlg.configure(bg=ThemeColors.MAIN_BG)
        dlg.transient(self.root)
        dlg.grab_set()
        dlg.resizable(False, False)

        dlg.update_idletasks()
        x = self.root.winfo_x() + (self.root.winfo_width() // 2) - (dlg.winfo_width() // 2)
        y = self.root.winfo_y() + (self.root.winfo_height() // 2) - (dlg.winfo_height() // 2)
        dlg.geometry(f"+{x}+{y}")

        # ═══ CONFIGURAZIONE MIGLIORATA PER LEGGIBILITÀ DROPDOWN ═══
        # Configurazione globale per tutti i dropdown Combobox
        dlg.tk.call("option", "add", "*TCombobox*Listbox.background", "#0F1A2E")
        dlg.tk.call("option", "add", "*TCombobox*Listbox.foreground", ThemeColors.WHITE)
        dlg.tk.call("option", "add", "*TCombobox*Listbox.selectBackground", ThemeColors.ORANGE)
        dlg.tk.call("option", "add", "*TCombobox*Listbox.selectForeground", ThemeColors.MAIN_BG)
        dlg.tk.call("option", "add", "*TCombobox*Listbox.font", "Arial 12")
        dlg.tk.call("option", "add", "*TCombobox*Listbox.borderWidth", "0")
        dlg.tk.call("option", "add", "*TCombobox*Listbox.highlightThickness", "0")
        
        # Configurazione aggiuntiva per migliorare il contrasto
        self.root.tk.call("option", "add", "*TCombobox*Listbox.background", "#0F1A2E")
        self.root.tk.call("option", "add", "*TCombobox*Listbox.foreground", ThemeColors.WHITE)
        self.root.tk.call("option", "add", "*TCombobox*Listbox.selectBackground", ThemeColors.ORANGE)
        self.root.tk.call("option", "add", "*TCombobox*Listbox.selectForeground", ThemeColors.MAIN_BG)

        main = tk.Frame(dlg, bg=ThemeColors.MAIN_BG)
        main.pack(fill="both", expand=True, padx=30, pady=30)

        tk.Label(
            main,
            text="Configurazione Trasportatore",
            font=("Arial", 16, "bold"),
            fg=ThemeColors.ORANGE,
            bg=ThemeColors.MAIN_BG,
        ).pack(anchor="w", pady=(0, 24))

        tk.Label(
            main,
            text="Trasportatore",
            font=("Arial", 11),
            fg=ThemeColors.LIGHT_GRAY,
            bg=ThemeColors.MAIN_BG,
        ).pack(anchor="w", pady=(0, 8))

        nomi = [t["nome"] for t in trasportatori]
        var_trasp = tk.StringVar(value=nomi[0] if nomi else "")

        combo_style = ttk.Style(dlg)
        combo_style.configure(
            "Custom.TCombobox",
            fieldbackground="#0F1A2E",
            background="#0F1A2E",
            foreground=ThemeColors.WHITE,
            arrowcolor=ThemeColors.ORANGE,
            bordercolor=ThemeColors.ORANGE,
            relief="flat",
            insertcolor=ThemeColors.WHITE,
            lightcolor="#1A1A2E",
            darkcolor="#1A1A2E",
        )

        combo = ttk.Combobox(
            main,
            values=nomi,
            textvariable=var_trasp,
            state="readonly",
            style="Custom.TCombobox",
            font=("Arial", 12),
            height=10,
        )
        combo.pack(fill="x", ipady=8)

        # ═══ CONFIGURAZIONE AVANZATA LISTBOX DROPDOWN ═══
        def configure_dropdown():
            try:
                # Trova la finestra dropdown della combobox
                popdown = combo.tk.eval(f'ttk::combobox::PopdownWindow {combo}')
                listbox = f'{popdown}.f.l'
                
                # Configurazione completa per massima leggibilità
                combo.tk.call(listbox, 'configure', '-background', '#0F1A2E')
                combo.tk.call(listbox, 'configure', '-foreground', ThemeColors.WHITE)
                combo.tk.call(listbox, 'configure', '-selectbackground', ThemeColors.ORANGE)
                combo.tk.call(listbox, 'configure', '-selectforeground', ThemeColors.MAIN_BG)
                combo.tk.call(listbox, 'configure', '-font', 'Arial 12')
                combo.tk.call(listbox, 'configure', '-borderwidth', '0')
                combo.tk.call(listbox, 'configure', '-highlightthickness', '0')
                combo.tk.call(listbox, 'configure', '-relief', 'flat')
                
                # Migliora la selezione e l'active state
                combo.tk.call(listbox, 'configure', '-activestyle', 'dotbox')
                
            except Exception as e:
                print(f"Configurazione dropdown fallita: {e}")
        
        # Configura quando viene aperto il dropdown
        def on_dropdown_open(event=None):
            dlg.after(10, configure_dropdown)
        
        # Bind all'evento di apertura
        combo.bind('<Button-1>', on_dropdown_open)
        combo.bind('<space>', on_dropdown_open)
        combo.bind('<Return>', on_dropdown_open)
        
        # Esegui anche dopo che il widget è renderizzato
        dlg.after(100, configure_dropdown)

        percent_var = tk.StringVar(value="10")
        if scelta == "GECO":
            tk.Label(
                main,
                text="Percentuale Variazione (0–100)",
                font=("Arial", 11),
                fg=ThemeColors.LIGHT_GRAY,
                bg=ThemeColors.MAIN_BG,
            ).pack(anchor="w", pady=(24, 8))

            validate_cmd = (dlg.register(self._is_valid_percent), "%P")
            percent_entry = tk.Entry(
                main,
                textvariable=percent_var,
                font=("Arial", 13),
                bg="#0F1A2E",
                fg=ThemeColors.WHITE,
                insertbackground=ThemeColors.ORANGE,
                relief="flat",
                borderwidth=0,
                validate="key",
                validatecommand=validate_cmd,
            )
            percent_entry.pack(fill="x", ipady=10)

            tk.Label(
                main,
                text="Lascia vuoto o inserisci 1 per nessuna variazione",
                font=("Arial", 9, "italic"),
                fg="#999",
                bg=ThemeColors.MAIN_BG,
            ).pack(anchor="w", pady=(6, 0))

        footer = tk.Frame(main, bg=ThemeColors.MAIN_BG)
        footer.pack(fill="x", pady=(30, 0))

        def conferma():
            nome = combo.get().strip()
            if not nome:
                messagebox.showwarning("Attenzione", "Seleziona un trasportatore.", parent=dlg)
                return
            sel = next((t for t in trasportatori if t["nome"] == nome), None)
            if not sel:
                messagebox.showerror("Errore", "Trasportatore non trovato.", parent=dlg)
                return

            perc = 1
            if scelta == "GECO" and percent_var.get().strip():
                try:
                    val = float(percent_var.get().replace(",", "."))
                    if not 0 <= val <= 100:
                        raise ValueError
                    perc = val
                except Exception:
                    messagebox.showerror("Errore", "Percentuale non valida (0-100).", parent=dlg)
                    return

            dlg.result = (sel, perc)
            dlg.destroy()

        def annulla():
            dlg.result = None
            dlg.destroy()

        tk.Button(
            footer,
            text="Annulla",
            font=("Arial", 11, "bold"),
            bg=ThemeColors.MAIN_BG,
            fg=ThemeColors.LIGHT_GRAY,
            activebackground="#1F2937",
            activeforeground=ThemeColors.ORANGE,
            relief="solid",
            borderwidth=1,
            highlightthickness=1,
            highlightbackground=ThemeColors.ORANGE,
            highlightcolor=ThemeColors.ORANGE_ACTIVE,
            command=annulla,
        ).pack(side="right", padx=(10, 0), ipadx=12, ipady=6)

        tk.Button(
            footer,
            text="Conferma",
            font=("Arial", 11, "bold"),
            bg=ThemeColors.ORANGE,
            fg=ThemeColors.MAIN_BG,
            activebackground=ThemeColors.ORANGE_ACTIVE,
            activeforeground=ThemeColors.MAIN_BG,
            relief="flat",
            borderwidth=0,
            command=conferma,
        ).pack(side="right", ipadx=16, ipady=6)

        combo.bind("<Return>", lambda e: conferma())
        dlg.bind("<Escape>", lambda e: annulla())

        dlg.wait_window()
        return getattr(dlg, "result", None)

    def _carica_trasportatori(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        path = os.path.normpath(
            os.path.join(base_dir, "..", "utils", "Db", "Trasportatori.json")
        )
        with open(path, encoding="utf-8") as f:
            return json.load(f)

    @staticmethod
    def _is_valid_percent(val):
        if not val.strip():
            return True
        try:
            return 0 <= float(val.replace(",", ".")) <= 100
        except ValueError:
            return False









    
        



