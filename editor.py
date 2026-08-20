import customtkinter as ctk
from tkinter import filedialog, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

from models import RadarChart, RadarData, RadarDataset, RadarStyle
from radar_plot import create_figure, export_chart_image
from excel_handler import load_chart

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

        # Buttons mit 'command' verknüpft!
        self.btn_load = ctk.CTkButton(self.sidebar_frame, text="Excel Laden", command=self.load_from_excel)
        self.btn_load.pack(pady=10, padx=20, fill="x")

        self.btn_save = ctk.CTkButton(self.sidebar_frame, text="Als Bild exportieren", command=self.export_image)
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

    def load_from_excel(self):
        """Öffnet einen Dialog, lädt die Excel-Datei und aktualisiert die Vorschau."""
        filepath = filedialog.askopenfilename(
            title="Excel-Datei auswählen",
            filetypes=[("Excel Files", "*.xlsx")]
        )
        
        if filepath:
            try:
                # Hier kommt dein mächtiger excel_handler und validator ins Spiel!
                self.current_chart = load_chart(filepath)
                self.update_preview()
            except Exception as e:
                # Fängt Fehler ab (z.B. wenn der Validator anschlägt)
                messagebox.showerror("Fehler beim Laden", f"Die Datei konnte nicht geladen werden:\n\n{str(e)}")

    def export_image(self):
        """Öffnet einen Speichern-Dialog und exportiert das aktuelle Chart."""
        filepath = filedialog.asksaveasfilename(
            title="Bild exportieren",
            defaultextension=".png",
            filetypes=[("PNG Image", "*.png"), ("SVG Vector", "*.svg")]
        )
        
        if filepath:
            try:
                export_chart_image(self.current_chart, filepath)
                messagebox.showinfo("Erfolg", f"Bild erfolgreich gespeichert unter:\n{filepath}")
            except Exception as e:
                messagebox.showerror("Fehler beim Export", f"Das Bild konnte nicht gespeichert werden:\n\n{str(e)}")

if __name__ == "__main__":
    app = StarChartEditor()
    app.mainloop()