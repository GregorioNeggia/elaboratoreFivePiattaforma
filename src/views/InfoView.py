import tkinter as tk
from utils.ui.theme_colors import ThemeColors


class InfoView:
    """Finestra di guida – coerente per stile con MainView."""

    def __init__(self, parent: tk.Tk | tk.Toplevel | None = None):
        # ── Finestra ────────────────────────────────────────────────────────
        self.window = tk.Toplevel(parent) if parent else tk.Toplevel()
        self.window.title("Guida - Elaboratore Five")
        self.window.geometry("1000x800")
        self.window.configure(bg=ThemeColors.BACKGROUND)
        self.window.resizable(True, True)

        # ── Layout principale ──────────────────────────────────────────────
        main = tk.Frame(self.window, bg=ThemeColors.BACKGROUND, padx=30, pady=30)
        main.pack(fill="both", expand=True)


        # Testo guida
        guida = (
            "Benvenuto nell’Elaboratore Five!\n\n"
            "\n"
            "Con questa applicazione puoi elaborare file CSV in quattro modalità:\n"
            "  • GECO – dati per GECO\n"
            "  • APRICA – dati per APRICA\n"
            "  • VALCAVALLINA – dati per VALCAVALLINA\n"
            "  • ALTRO – elaborazioni personalizzate\n\n"
            "\n"
            "Procedura passo-passo:\n"
            "\n"
            "  1. Seleziona la modalità desiderata.\n"
            "  2. Importa il file CSV.\n"
            "  3. Inserisci il nome della PA e scegli il trasportatore.\n"
            "  4. Controlla l’anteprima dei dati.\n"
            "  5. Esporta il risultato finale.\n\n"
            "\n"
            "Per assistenza: gregorio@fiveconsulting.it"
        )
        # Titolo
        tk.Label(
            main,
            text="Guida all'Elaboratore Five",
            font=("Helvetica", 24, "bold"),
            fg=ThemeColors.ORANGE,
            bg=ThemeColors.BACKGROUND,
        ).pack(pady=(0, 30))

        


        

        tk.Label(
            main,
            text=guida,
            font=("Helvetica", 20),
            fg=ThemeColors.WHITE,
            bg=ThemeColors.BACKGROUND,
            justify="left",
            wraplength=700,
        ).pack(pady=(0, 30))

        # Pulsante Chiudi
        tk.Button(
            main,
            text="Chiudi",
            font=("Arial", 18, "bold"),
            bg=ThemeColors.ORANGE,
            fg=ThemeColors.MAIN_BG,
            relief="raised",
            borderwidth=3,
            command=self.window.destroy,
        ).pack(pady=(0, 20))
