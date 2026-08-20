import customtkinter as ctk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

from models import RadarChart, RadarData, RadarDataset, RadarStyle
from radar_plot import create_figure

# Modernes Design aktivieren
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class StarChartEditor(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Star Chart Editor")
        self.geometry("1100x700")

        # Layout: 1 Zeile, 2 Spalten (Sidebar links, Vorschau rechts)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # --- LINKES PANEL: SIDEBAR ---
        self.sidebar_frame = ctk.CTkFrame(self, width=300, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_propagate(False)

        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="Chart Editor", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.pack(pady=(20, 30))

        # Platzhalter-Buttons für später
        self.btn_load = ctk.CTkButton(self.sidebar_frame, text="Excel Laden")
        self.btn_load.pack(pady=10, padx=20, fill="x")

        self.btn_save = ctk.CTkButton(self.sidebar_frame, text="Als Bild exportieren")
        self.btn_save.pack(pady=10, padx=20, fill="x")

        # --- RECHTES PANEL: LIVE VORSCHAU ---
        self.preview_frame = ctk.CTkFrame(self)
        self.preview_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        
        # Variable für das Matplotlib-Canvas
        self.canvas = None

        # Erstelle ein Dummy-Chart für den Start
        self.current_chart = self._create_dummy_chart()
        self.update_preview()

    def _create_dummy_chart(self) -> RadarChart:
        """Erstellt ein einfaches Chart, damit das Fenster beim Start nicht leer ist."""
        ds = RadarDataset(name="Beispiel", values=[50, 75, 60, 90, 80], color="#1f538d")
        data = RadarData(title="Live Vorschau", labels=["A", "B", "C", "D", "E"], datasets=[ds])
        style = RadarStyle(frame="polygon", line_color="#000", fill_color="#000", fill=True, alpha=0.2)
        return RadarChart(data=data, style=style)

    def update_preview(self):
        """Zeichnet das Chart neu und bettet es in das CustomTkinter-Fenster ein."""
        # Altes Canvas löschen, falls vorhanden
        if self.canvas:
            self.canvas.get_tk_widget().destroy()

        # Neues Figure über unseren Plotter generieren
        fig, _ = create_figure(self.current_chart)

        # Figure in Tkinter einbetten
        self.canvas = FigureCanvasTkAgg(fig, master=self.preview_frame)
        self.canvas.draw()
        
        # Das Widget im Frame platzieren
        widget = self.canvas.get_tk_widget()
        widget.pack(fill="both", expand=True)
        
        # Speicher freigeben
        plt.close(fig)

if __name__ == "__main__":
    app = StarChartEditor()
    app.mainloop()