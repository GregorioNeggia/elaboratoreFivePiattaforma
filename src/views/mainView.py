import tkinter as tk
from tkinter import ttk
import os

class MainView:
    def __init__(self, root, AppController):
        self.root = root
        self.AppController = AppController
        self.root.title("Elaboratore Five - Seleziona Modalità")
        self.root.geometry("1400x900")
        self.root.configure(bg="#1A1A2E")  # Sfondo generale scuro

        # === Caricamento logo ===
        logo_path = "src/utils/five_consulting_logo.png"
        self.logo = None
        if os.path.exists(logo_path):
            try:
                self.logo = tk.PhotoImage(file=logo_path)
                print("Logo caricato con successo.")
            except Exception as e:
                print(f"Errore caricamento logo: {e}")
        else:
            print(f"File logo non trovato: {logo_path}")

        # === Stile bottoni personalizzato ===
        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "BigOrange.TButton",
            font=("Arial", 18, "bold"),
            background="#FF8C00",
            foreground="#16213E",
            relief="raised",
            borderwidth=3,
            padding=12
        )
        style.map(
            "BigOrange.TButton",
            background=[("active", "#FF6B35")],
            foreground=[("active", "#16213E")]
        )

        # === Layout principale ===
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        self.main_frame = tk.Frame(self.root, bg="#16213E", padx=40, pady=40)
        self.main_frame.grid(sticky="nsew")

        # ===== 1. HEADER (logo) =====
        self.header_frame = tk.Frame(self.main_frame, bg="#FFFFFF", pady=15)
        self.header_frame.pack(fill="x", pady=(0, 20))

        if self.logo:
            tk.Label(self.header_frame, image=self.logo, bg="#FFFFFF").pack(pady=(5, 10))
        tk.Frame(self.header_frame, bg="#16213E", height=4).pack(fill="x")

        # ===== 2. INFO (titolo + sottotitolo) =====
        self.info_frame = tk.Frame(self.main_frame, bg="#16213E")
        self.info_frame.pack(pady=(20, 40))

        tk.Label(
            self.info_frame,
            text="Elaboratore Five",
            font=("Arial", 36, "bold"),
            fg="#FF8C00",
            bg="#16213E"
        ).pack(pady=(0, 10))

        tk.Label(
            self.info_frame,
            text="Seleziona la modalità di elaborazione",
            font=("Arial", 20),
            fg="#E0E0E0",
            bg="#16213E"
        ).pack()

        # ===== 3. BOTTONI PRINCIPALI =====
        self.buttons_frame = tk.Frame(self.main_frame, bg="#16213E")
        self.buttons_frame.pack(pady=(20, 40))

        # Griglia 2x2
        self.buttons_frame.columnconfigure((0, 1), weight=1, uniform="col")
        self.buttons_frame.rowconfigure((0, 1), weight=1, uniform="row")

        # Riga 1
        self._add_button("ALTRO", 0, 0)
        self._add_button("APRICA", 0, 1)
        # Riga 2
        self._add_button("GECO", 1, 0)
        self._add_button("VALCAVALLINA", 1, 1)

        # ===== 4. BOTTONI EXTRA =====
        self.extra_frame = tk.Frame(self.main_frame, bg="#16213E")
        self.extra_frame.pack(pady=(20, 20))

        ttk.Button(
            self.extra_frame,
            text="INFO",
            command=self.apriInfo,
            style="BigOrange.TButton"
        ).pack(fill="x", ipadx=20, ipady=5)

        # ===== 5. FOOTER =====
        self.footer_label = tk.Label(
            self.main_frame,
            text="SVILUPPATO DA GREGORIO NEGGIA",
            font=("Arial", 14, "bold"),
            fg="#FF8C00",
            bg="#16213E"
        )
        self.footer_label.pack(side="bottom", pady=(30, 10))

    # --- Funzioni di supporto ---
    def _add_button(self, text, row, col):
        btn = ttk.Button(
            self.buttons_frame,
            text=text,
            command=lambda s=text: self.apri_elaboratore(s),
            style="BigOrange.TButton"
        )
        btn.grid(row=row, column=col, padx=30, pady=20, sticky="nsew")

    def apriInfo(self):
        self.AppController.apriInfo()

    def apri_elaboratore(self, scelta):
        self.AppController.apri_elaboratore(scelta)


        