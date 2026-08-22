import customtkinter as ctk
from tkinter import filedialog, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

from models import RadarChart, RadarData, RadarDataset, RadarStyle
from radar_plot import create_figure, export_chart_image
from excel_handler import load_chart

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class StarChartEditor(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Star Chart Editor")
        self.geometry("1100x750")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Flag gegen ungewollte Mehrfach-Aufrufe beim Initialisieren der Regler
        self._is_updating_ui = False

        # --- LINKES PANEL: SIDEBAR ---
        self.sidebar_frame = ctk.CTkScrollableFrame(self, width=320, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")

        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="Chart Editor", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.pack(pady=(20, 15))

        # Dateipfad-Aktionen
        self.btn_load = ctk.CTkButton(self.sidebar_frame, text="Excel Laden", command=self.load_from_excel)
        self.btn_load.pack(pady=5, padx=20, fill="x")

        self.btn_save = ctk.CTkButton(self.sidebar_frame, text="Als Bild exportieren", command=self.export_image)
        self.btn_save.pack(pady=5, padx=20, fill="x")

        # Trennlinie
        ctk.CTkFrame(self.sidebar_frame, height=2, fg_color="gray30").pack(fill="x", pady=15, padx=20)

        # --- EINSTELLUNGEN ---
        
        # 1. Titel
        ctk.CTkLabel(self.sidebar_frame, text="Diagramm-Titel:", font=ctk.CTkFont(weight="bold")).pack(anchor="w", padx=20)
        
        self.title_frame = ctk.CTkFrame(self.sidebar_frame, fg_color="transparent")
        self.title_frame.pack(pady=(2, 10), padx=20, fill="x")

        self.entry_title = ctk.CTkEntry(self.title_frame)
        self.entry_title.pack(side="left", fill="x", expand=True, padx=(0, 5))
        self.entry_title.bind("<Return>", lambda e: self.apply_changes()) # Enter wendet alle Änderungen an

        # 2. Transparenz (Alpha Slider)
        self.lbl_alpha = ctk.CTkLabel(self.sidebar_frame, text="Transparenz (0.20):", font=ctk.CTkFont(weight="bold"))
        self.lbl_alpha.pack(anchor="w", padx=20, pady=(10, 0))
        
        # command-Parameter aktualisiert nur noch das Label, nicht das Diagramm!
        self.slider_alpha = ctk.CTkSlider(self.sidebar_frame, from_=0.0, to=1.0, number_of_steps=20, command=self._update_slider_labels)
        self.slider_alpha.pack(pady=(2, 10), padx=20, fill="x")

        # 3. Ring-Anzahl Slider
        self.lbl_rings = ctk.CTkLabel(self.sidebar_frame, text="Gitter-Ringe (5):", font=ctk.CTkFont(weight="bold"))
        self.lbl_rings.pack(anchor="w", padx=20, pady=(10, 0))

        # command-Parameter aktualisiert nur noch das Label, nicht das Diagramm!
        self.slider_rings = ctk.CTkSlider(self.sidebar_frame, from_=2, to=10, number_of_steps=8, command=self._update_slider_labels)
        self.slider_rings.pack(pady=(2, 10), padx=20, fill="x")

        # --- BUTTON ZUM ANWENDEN DER ÄNDERUNGEN ---
        self.btn_apply = ctk.CTkButton(self.sidebar_frame, text="Ansicht aktualisieren", command=self.apply_changes, fg_color="#2b8256", hover_color="#1e5c3d")
        self.btn_apply.pack(pady=20, padx=20, fill="x")


        # --- RECHTES PANEL: LIVE VORSCHAU ---
        self.preview_frame = ctk.CTkFrame(self)
        self.preview_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        
        self.canvas = None
        self.current_chart = self._create_dummy_chart()
        
        # GUI mit Modell-Daten füllen und Zeichnen
        self._sync_sidebar_from_chart()
        self.update_preview()

    def _create_dummy_chart(self) -> RadarChart:
        """Erstellt ein einfaches Chart für den Start."""
        ds = RadarDataset(name="Beispiel", values=[50, 75, 60, 90, 80], color="#007ACC", marker="o", line_width=2.0)
        data = RadarData(title="Live Vorschau", labels=["Angriff", "Verteidigung", "Tempo", "Technik", "Ausdauer"], datasets=[ds])
        style = RadarStyle(frame="polygon", line_color="#000", fill_color="#000", fill=True, alpha=0.2, ring_count=5)
        return RadarChart(data=data, style=style)

    def _sync_sidebar_from_chart(self):
        """Aktualisiert alle Sidebar-Regler basierend auf dem aktuellen Chart."""
        self._is_updating_ui = True

        self.entry_title.delete(0, "end")
        self.entry_title.insert(0, self.current_chart.data.title)

        self.slider_alpha.set(self.current_chart.style.alpha)
        self.slider_rings.set(self.current_chart.style.ring_count)
        
        self._update_slider_labels()

        self._is_updating_ui = False

    def _update_slider_labels(self, value=None):
        """Aktualisiert nur den Text über den Slidern, während man schiebt."""
        if self._is_updating_ui:
            return
            
        alpha_val = self.slider_alpha.get()
        rings_val = int(self.slider_rings.get())
        
        self.lbl_alpha.configure(text=f"Transparenz ({alpha_val:.2f}):")
        self.lbl_rings.configure(text=f"Gitter-Ringe ({rings_val}):")

    def apply_changes(self):
        """Liest alle Werte aus der GUI aus, wendet sie auf das Modell an und zeichnet das Chart neu."""
        if self._is_updating_ui:
            return

        # 1. Werte auslesen
        new_title = self.entry_title.get()
        alpha_val = round(self.slider_alpha.get(), 2)
        rings_val = int(self.slider_rings.get())

        # 2. Modell aktualisieren
        self.current_chart.data.title = new_title
        self.current_chart.style.alpha = alpha_val
        self.current_chart.style.ring_count = rings_val
        
        # 'fill' automatisch basierend auf Transparenz setzen
        self.current_chart.style.fill = alpha_val > 0.0

        # 3. Neu zeichnen
        self.update_preview()

    def update_preview(self):
        """Zeichnet das Chart neu und bettet es ein."""
        if self.canvas:
            self.canvas.get_tk_widget().destroy()

        fig, _ = create_figure(self.current_chart)

        self.canvas = FigureCanvasTkAgg(fig, master=self.preview_frame)
        self.canvas.draw()
        
        widget = self.canvas.get_tk_widget()
        widget.pack(fill="both", expand=True)
        
        plt.close(fig)

    def load_from_excel(self):
        """Öffnet einen Dialog, lädt die Excel-Datei und aktualisiert die Vorschau."""
        filepath = filedialog.askopenfilename(
            title="Excel-Datei auswählen",
            filetypes=[("Excel Files", "*.xlsx")]
        )
        
        if filepath:
            try:
                self.current_chart = load_chart(filepath)
                self._sync_sidebar_from_chart()
                self.update_preview()
            except Exception as e:
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