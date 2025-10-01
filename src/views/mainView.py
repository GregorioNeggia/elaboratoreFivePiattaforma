# views/main_view.py
import os
import tkinter as tk
from tkinter import ttk
from utils.ui.theme_colors import ThemeColors


class MainView:
    """Schermata iniziale 'Seleziona Modalità'."""

    def __init__(self, root, app_controller):
        self.root           = root
        self.app_controller = app_controller

        # ── Finestra ────────────────────────────────────────────────────────
        self.root.title("Elaboratore Five – Seleziona Modalità")
        self.root.geometry("1400x900")
        self.root.configure(bg=ThemeColors.BACKGROUND)

        # ── Risorse ────────────────────────────────────────────────────────
        self.logo = self._load_logo()

        # ── Stile globale TTK ───────────────────────────────────────────────
        self._setup_style()

        # ── Layout principale ──────────────────────────────────────────────
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0,  weight=1)

        self.main_frame = tk.Frame(
            self.root,
            bg=ThemeColors.MAIN_BG,
            padx=40,
            pady=40,
        )
        self.main_frame.grid(sticky="nsew")

        self._build_header()
        self._build_info()
        self._build_buttons()
        self._build_extra()
        self._build_footer()

    # ======================================================================
    # Helper privati
    # ======================================================================

    def _load_logo(self):
        logo_path = os.path.abspath(
            os.path.join(
                os.path.dirname(__file__),
                "..", "utils", "five_consulting_logo.png",
            )
        )
        if not os.path.exists(logo_path):
            print(f"File logo non trovato: {logo_path}")
            return None

        try:
            return tk.PhotoImage(file=logo_path)
        except Exception as exc:
            print(f"Errore caricamento logo: {exc}")
            return None

    def _setup_style(self):
        style = ttk.Style()
        style.theme_use("clam")

        style.configure(
            "BigOrange.TButton",
            font=("Arial", 18, "bold"),
            background=ThemeColors.ORANGE,
            foreground=ThemeColors.MAIN_BG,
            relief="raised",
            borderwidth=3,
            padding=12,
        )
        style.map(
            "BigOrange.TButton",
            background=[("active", ThemeColors.ORANGE_ACTIVE)],
            foreground=[("active", ThemeColors.MAIN_BG)],
        )

    # ── Costruzione sottosezioni UI ────────────────────────────────────────
    def _build_header(self):
        header = tk.Frame(self.main_frame, bg=ThemeColors.WHITE, pady=15)
        header.pack(fill="x", pady=(0, 20))

        if self.logo:
            tk.Label(header, image=self.logo, bg=ThemeColors.WHITE).pack(pady=(5, 10))
        tk.Frame(header, bg=ThemeColors.MAIN_BG, height=4).pack(fill="x")

    def _build_info(self):
        info = tk.Frame(self.main_frame, bg=ThemeColors.MAIN_BG)
        info.pack(pady=(20, 40))

        tk.Label(
            info,
            text="Elaboratore Five",
            font=("Arial", 36, "bold"),
            fg=ThemeColors.ORANGE,
            bg=ThemeColors.MAIN_BG,
        ).pack(pady=(0, 10))

        tk.Label(
            info,
            text="Seleziona la modalità di elaborazione",
            font=("Arial", 20),
            fg=ThemeColors.LIGHT_GRAY,
            bg=ThemeColors.MAIN_BG,
        ).pack()

    def _build_buttons(self):
        grid = tk.Frame(self.main_frame, bg=ThemeColors.MAIN_BG)
        grid.pack(pady=(20, 40))

        # Configura griglia 2×2
        for idx in (0, 1):
            grid.columnconfigure(idx, weight=1, uniform="col")
            grid.rowconfigure(idx,    weight=1, uniform="row")

        modes = [
            ("ALTRO",         0, 0),
            ("APRICA",        0, 1),
            ("GECO",          1, 0),
            ("VALCAVALLINA",  1, 1),
        ]
        for text, r, c in modes:
            ttk.Button(
                grid,
                text=text,
                style="BigOrange.TButton",
                command=lambda s=text: self.app_controller.apri_elaboratore(s, self.root),
            ).grid(row=r, column=c, padx=30, pady=20, sticky="nsew")

    def _build_extra(self):
        extra = tk.Frame(self.main_frame, bg=ThemeColors.MAIN_BG)
        extra.pack(pady=(20, 20))

        ttk.Button(
            extra,
            text="INFO",
            style="BigOrange.TButton",
            command=self.app_controller.apriInfo,
        ).pack(fill="x", ipadx=20, ipady=5)

    def _build_footer(self):
        tk.Label(
            self.main_frame,
            text="SVILUPPATO DA GREGORIO NEGGIA",
            font=("Arial", 14, "bold"),
            fg=ThemeColors.ORANGE,
            bg=ThemeColors.MAIN_BG,
        ).pack(side="bottom", pady=(30, 10))
