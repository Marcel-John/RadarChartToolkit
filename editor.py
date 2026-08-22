import customtkinter as ctk
from tkinter import filedialog, messagebox, colorchooser
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

        self._is_updating_ui = False

        # --- LINKES PANEL: SIDEBAR ---
        self.sidebar_frame = ctk.CTkScrollableFrame(self, width=320, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")

        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="Chart Editor", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.pack(pady=(20, 15))

        self.btn_load = ctk.CTkButton(self.sidebar_frame, text="Excel Laden", command=self.load_from_excel)
        self.btn_load.pack(pady=5, padx=20, fill="x")

        self.btn_save = ctk.CTkButton(self.sidebar_frame, text="Als Bild exportieren", command=self.export_image)
        self.btn_save.pack(pady=5, padx=20, fill="x")

        ctk.CTkFrame(self.sidebar_frame, height=2, fg_color="gray30").pack(fill="x", pady=15, padx=20)

        # --- EINSTELLUNGEN ---
        
        # 1. Titel
        ctk.CTkLabel(self.sidebar_frame, text="Diagramm-Titel:", font=ctk.CTkFont(weight="bold")).pack(anchor="w", padx=20)
        
        self.title_frame = ctk.CTkFrame(self.sidebar_frame, fg_color="transparent")
        self.title_frame.pack(pady=(2, 10), padx=20, fill="x")

        self.entry_title = ctk.CTkEntry(self.title_frame)
        self.entry_title.pack(side="left", fill="x", expand=True, padx=(0, 5))
        self.entry_title.bind("<Return>", lambda e: self.apply_changes())

        # 2. Transparenz
        self.lbl_alpha = ctk.CTkLabel(self.sidebar_frame, text="Transparenz (0.20):", font=ctk.CTkFont(weight="bold"))
        self.lbl_alpha.pack(anchor="w", padx=20, pady=(10, 0))
        
        self.slider_alpha = ctk.CTkSlider(self.sidebar_frame, from_=0.0, to=1.0, number_of_steps=20, command=self._update_slider_labels)
        self.slider_alpha.pack(pady=(2, 10), padx=20, fill="x")

        # 3. Ring-Anzahl
        self.lbl_rings = ctk.CTkLabel(self.sidebar_frame, text="Gitter-Ringe (5):", font=ctk.CTkFont(weight="bold"))
        self.lbl_rings.pack(anchor="w", padx=20, pady=(10, 0))

        self.slider_rings = ctk.CTkSlider(self.sidebar_frame, from_=2, to=10, number_of_steps=8, command=self._update_slider_labels)
        self.slider_rings.pack(pady=(2, 10), padx=20, fill="x")
        
        ctk.CTkFrame(self.sidebar_frame, height=2, fg_color="gray30").pack(fill="x", pady=15, padx=20)

        # --- DATENSÄTZE & FARBEN ---
        ctk.CTkLabel(self.sidebar_frame, text="Farben der Datensätze:", font=ctk.CTkFont(weight="bold")).pack(anchor="w", padx=20)
        
        # Leerer Frame, der später dynamisch mit Buttons gefüllt wird
        self.datasets_frame = ctk.CTkFrame(self.sidebar_frame, fg_color="transparent")
        self.datasets_frame.pack(fill="x", padx=20, pady=(5, 10))

        # --- BUTTON ZUM ANWENDEN DER ÄNDERUNGEN ---
        self.btn_apply = ctk.CTkButton(self.sidebar_frame, text="Ansicht aktualisieren", command=self.apply_changes, fg_color="#2b8256", hover_color="#1e5c3d")
        self.btn_apply.pack(pady=20, padx=20, fill="x")

        # --- RECHTES PANEL: LIVE VORSCHAU ---
        self.preview_frame = ctk.CTkFrame(self)
        self.preview_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        
        self.canvas = None
        self.current_chart = self._create_dummy_chart()
        
        self._sync_sidebar_from_chart()
        self.update_preview()

    def _create_dummy_chart(self) -> RadarChart:
        ds = RadarDataset(name="Beispiel", values=[50, 75, 60, 90, 80], color="#007ACC", marker="o", line_width=2.0)
        data = RadarData(title="Live Vorschau", labels=["Angriff", "Verteidigung", "Tempo", "Technik", "Ausdauer"], datasets=[ds])
        style = RadarStyle(frame="polygon", line_color="#000", fill_color="#000", fill=True, alpha=0.2, ring_count=5)
        return RadarChart(data=data, style=style)

    def _sync_sidebar_from_chart(self):
        """Aktualisiert alle Sidebar-Regler basierend auf dem aktuellen Chart."""
        self._is_updating_ui = True

        # Textfeld und Slider
        self.entry_title.delete(0, "end")
        self.entry_title.insert(0, self.current_chart.data.title)
        self.slider_alpha.set(self.current_chart.style.alpha)
        self.slider_rings.set(self.current_chart.style.ring_count)
        self._update_slider_labels()

        # Farb-Buttons für jeden Datensatz neu generieren
        for widget in self.datasets_frame.winfo_children():
            widget.destroy()

        for ds in self.current_chart.data.datasets:
            row_frame = ctk.CTkFrame(self.datasets_frame, fg_color="transparent")
            row_frame.pack(fill="x", pady=5)
            
            lbl = ctk.CTkLabel(row_frame, text=ds.name)
            lbl.pack(side="left")
            
            # Farb-Block Button
            btn_color = ctk.CTkButton(
                row_frame, 
                text="", 
                width=40, 
                height=20,
                corner_radius=4,
                border_width=1,
                border_color="gray50",
                fg_color=ds.color, 
                hover_color=ds.color,
                command=lambda dataset=ds: self._change_dataset_color(dataset)
            )
            btn_color.pack(side="right")

        self._is_updating_ui = False

    def _change_dataset_color(self, dataset):
        """Öffnet den Farbwähler und aktualisiert die Farbe für den Datensatz."""
        # colorchooser gibt ein Tupel zurück: ((r, g, b), '#hexcode')
        color_result = colorchooser.askcolor(title=f"Farbe für {dataset.name}", initialcolor=dataset.color)
        
        hex_color = color_result[1]
        if hex_color:  # Wenn der Nutzer nicht auf "Abbrechen" geklickt hat
            dataset.color = hex_color
            self._sync_sidebar_from_chart()  # Buttons aktualisieren
            self.update_preview()            # Diagramm sofort neu zeichnen

    def _update_slider_labels(self, value=None):
        if self._is_updating_ui: return
        self.lbl_alpha.configure(text=f"Transparenz ({self.slider_alpha.get():.2f}):")
        self.lbl_rings.configure(text=f"Gitter-Ringe ({int(self.slider_rings.get())}):")

    def apply_changes(self):
        if self._is_updating_ui: return
        self.current_chart.data.title = self.entry_title.get()
        self.current_chart.style.alpha = round(self.slider_alpha.get(), 2)
        self.current_chart.style.ring_count = int(self.slider_rings.get())
        self.current_chart.style.fill = self.current_chart.style.alpha > 0.0
        self.update_preview()

    def update_preview(self):
        if self.canvas: self.canvas.get_tk_widget().destroy()
        fig, _ = create_figure(self.current_chart)
        self.canvas = FigureCanvasTkAgg(fig, master=self.preview_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill="both", expand=True)
        plt.close(fig)

    def load_from_excel(self):
        filepath = filedialog.askopenfilename(title="Excel-Datei auswählen", filetypes=[("Excel Files", "*.xlsx")])
        if filepath:
            try:
                self.current_chart = load_chart(filepath)
                self._sync_sidebar_from_chart()
                self.update_preview()
            except Exception as e:
                messagebox.showerror("Fehler beim Laden", f"Die Datei konnte nicht geladen werden:\n\n{str(e)}")

    def export_image(self):
        filepath = filedialog.asksaveasfilename(title="Bild exportieren", defaultextension=".png", filetypes=[("PNG Image", "*.png"), ("SVG Vector", "*.svg")])
        if filepath:
            try:
                export_chart_image(self.current_chart, filepath)
                messagebox.showinfo("Erfolg", f"Bild erfolgreich gespeichert unter:\n{filepath}")
            except Exception as e:
                messagebox.showerror("Fehler beim Export", f"Das Bild konnte nicht gespeichert werden:\n\n{str(e)}")

if __name__ == "__main__":
    app = StarChartEditor()
    app.mainloop()