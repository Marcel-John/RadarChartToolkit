import customtkinter as ctk
from tkinter import filedialog, messagebox, colorchooser
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import random  # NEU: Um zufällige Farben für neue Datensätze zu generieren

from models import RadarChart, RadarData, RadarDataset, RadarStyle
from radar_plot import create_figure, export_chart_image
from excel_handler import load_chart

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class DataEditorWindow(ctk.CTkToplevel):
    """Pop-up Fenster zum Bearbeiten, Hinzufügen und Löschen von Diagramm-Werten."""
    def __init__(self, parent, chart: RadarChart, update_callback):
        super().__init__(parent)
        self.title("Daten & Werte bearbeiten")
        self.geometry("850x550") # Etwas breiter gemacht, damit alles gut reinpasst
        
        self.transient(parent)
        self.grab_set()

        self.chart = chart
        self.update_callback = update_callback

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.scroll_frame = ctk.CTkScrollableFrame(self)
        self.scroll_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        # Unterer Bereich für das Hinzufügen
        self.bottom_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.bottom_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=(0, 10))
        self.bottom_frame.grid_columnconfigure(2, weight=1) # Schiebt den "Übernehmen" Button nach rechts

        # Zeile 1: Kategorie hinzufügen
        self.new_cat_entry = ctk.CTkEntry(self.bottom_frame, placeholder_text="Neue Kategorie (z.B. Magie)")
        self.new_cat_entry.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        
        self.btn_add_cat = ctk.CTkButton(self.bottom_frame, text="Kategorie hinzufügen", command=self.add_category)
        self.btn_add_cat.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        # Zeile 2: Datensatz hinzufügen (NEU)
        self.new_ds_entry = ctk.CTkEntry(self.bottom_frame, placeholder_text="Neuer Datensatz (z.B. Paladin)")
        self.new_ds_entry.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        
        self.btn_add_ds = ctk.CTkButton(self.bottom_frame, text="Datensatz hinzufügen", command=self.add_dataset)
        self.btn_add_ds.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        # Button zum Speichern rechts anordnen
        self.btn_apply = ctk.CTkButton(
            self.bottom_frame, text="Werte übernehmen", 
            command=self.apply_values, fg_color="#2b8256", hover_color="#1e5c3d"
        )
        self.btn_apply.grid(row=0, column=3, rowspan=2, padx=5, pady=5, sticky="e")

        self.entries = {}
        self.header_entries = [] 
        self.build_grid()

    def build_grid(self):
        """Baut die Tabelle mit Kategorien, Datensatz-Namen und Werten auf."""
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()
        
        self.entries.clear()
        self.header_entries.clear()

        # Tabellenkopf (Header)
        ctk.CTkLabel(self.scroll_frame, text="Kategorie", font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, padx=10, pady=5, sticky="w")
        
        for c, ds in enumerate(self.chart.data.datasets):
            # Frame für das Eingabefeld UND den Löschen-Button des Datensatzes
            header_frame = ctk.CTkFrame(self.scroll_frame, fg_color="transparent")
            header_frame.grid(row=0, column=c+1, padx=10, pady=5)

            entry_name = ctk.CTkEntry(header_frame, font=ctk.CTkFont(weight="bold"), width=100)
            entry_name.insert(0, ds.name)
            entry_name.pack(side="left", padx=(0, 5))
            self.header_entries.append(entry_name)

            # Löschen-Button für den ganzen Datensatz
            btn_del_ds = ctk.CTkButton(
                header_frame, text="X", width=25, height=25,
                fg_color="#a83232", hover_color="#7a2424", 
                command=lambda idx=c: self.delete_dataset(idx)
            )
            btn_del_ds.pack(side="left")

        # Tabellen-Zeilen (Daten)
        for r, label in enumerate(self.chart.data.labels):
            ctk.CTkLabel(self.scroll_frame, text=label).grid(row=r+1, column=0, padx=10, pady=5, sticky="w")

            for c, ds in enumerate(self.chart.data.datasets):
                val = ds.values[r]
                entry = ctk.CTkEntry(self.scroll_frame, width=130)
                entry.insert(0, str(val))
                entry.grid(row=r+1, column=c+1, padx=10, pady=5)
                self.entries[(r, c)] = entry

            # Löschen-Button für die ganze Kategorie (Zeile)
            btn_del_cat = ctk.CTkButton(
                self.scroll_frame, text="X", width=30, 
                fg_color="#a83232", hover_color="#7a2424", 
                command=lambda idx=r: self.delete_category(idx)
            )
            btn_del_cat.grid(row=r+1, column=len(self.chart.data.datasets)+1, padx=20, pady=5)

    def _save_current_state(self):
        """Speichert alle aktuellen Eingaben aus den Textfeldern ins Modell."""
        for c, entry_name in enumerate(self.header_entries):
            new_name = entry_name.get().strip()
            if new_name:
                self.chart.data.datasets[c].name = new_name
                
        for (r, c), entry in self.entries.items():
            val = float(entry.get())
            self.chart.data.datasets[c].values[r] = val

    def add_category(self):
        """Fügt eine neue Achse/Zeile hinzu."""
        new_cat = self.new_cat_entry.get().strip()
        if not new_cat: return

        try:
            self._save_current_state()
        except ValueError:
            messagebox.showerror("Fehler", "Bitte erst ungültige Zahlen korrigieren.")
            return

        self.chart.data.labels.append(new_cat)
        for ds in self.chart.data.datasets:
            ds.values.append(0.0)

        self.new_cat_entry.delete(0, 'end')
        self.build_grid()
        self.update_callback()
        
    def add_dataset(self):
        """Fügt einen neuen Datensatz (Spalte) hinzu."""
        new_ds_name = self.new_ds_entry.get().strip()
        if not new_ds_name: return

        try:
            self._save_current_state()
        except ValueError:
            messagebox.showerror("Fehler", "Bitte erst ungültige Zahlen korrigieren.")
            return

        # Zufällige Farbe generieren (Hex)
        random_color = f"#{random.randint(0, 0xFFFFFF):06x}"
        
        # Leere Werte (0.0) für alle existierenden Kategorien anlegen
        new_values = [0.0] * len(self.chart.data.labels)
        
        new_ds = RadarDataset(name=new_ds_name, values=new_values, color=random_color, marker="o", line_width=2.0)
        self.chart.data.datasets.append(new_ds)

        self.new_ds_entry.delete(0, 'end')
        self.build_grid()
        self.update_callback()

    def delete_category(self, idx):
        if len(self.chart.data.labels) <= 3:
            messagebox.showwarning("Achtung", "Ein Radar-Chart benötigt mindestens 3 Kategorien!")
            return

        try:
            self._save_current_state()
        except ValueError:
            messagebox.showerror("Fehler", "Bitte erst ungültige Zahlen korrigieren.")
            return

        del self.chart.data.labels[idx]
        for ds in self.chart.data.datasets:
            del ds.values[idx]

        self.build_grid()
        self.update_callback()
        
    def delete_dataset(self, idx):
        """Löscht einen kompletten Datensatz (Spalte)."""
        if len(self.chart.data.datasets) <= 1:
            messagebox.showwarning("Achtung", "Es muss mindestens ein Datensatz im Diagramm bleiben!")
            return

        try:
            self._save_current_state()
        except ValueError:
            messagebox.showerror("Fehler", "Bitte erst ungültige Zahlen korrigieren.")
            return

        del self.chart.data.datasets[idx]

        self.build_grid()
        self.update_callback()

    def apply_values(self):
        try:
            self._save_current_state()
            self.update_callback()
            
            self.btn_apply.configure(text="✓ Gespeichert")
            self.after(1500, lambda: self.btn_apply.configure(text="Werte übernehmen"))
        except ValueError:
            messagebox.showerror("Fehler", "Bitte nur gültige Zahlen eingeben (z.B. 10 oder 5.5).")


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

        self.btn_edit = ctk.CTkButton(self.sidebar_frame, text="Daten bearbeiten", command=self.open_data_editor, fg_color="#1f538d")
        self.btn_edit.pack(pady=5, padx=20, fill="x")

        self.btn_save = ctk.CTkButton(self.sidebar_frame, text="Als Bild exportieren", command=self.export_image)
        self.btn_save.pack(pady=5, padx=20, fill="x")

        ctk.CTkFrame(self.sidebar_frame, height=2, fg_color="gray30").pack(fill="x", pady=15, padx=20)

        # --- EINSTELLUNGEN ---
        ctk.CTkLabel(self.sidebar_frame, text="Diagramm-Titel:", font=ctk.CTkFont(weight="bold")).pack(anchor="w", padx=20)
        
        self.title_frame = ctk.CTkFrame(self.sidebar_frame, fg_color="transparent")
        self.title_frame.pack(pady=(2, 10), padx=20, fill="x")

        self.entry_title = ctk.CTkEntry(self.title_frame)
        self.entry_title.pack(side="left", fill="x", expand=True, padx=(0, 5))
        self.entry_title.bind("<Return>", lambda e: self.apply_changes())

        self.lbl_alpha = ctk.CTkLabel(self.sidebar_frame, text="Transparenz (0.20):", font=ctk.CTkFont(weight="bold"))
        self.lbl_alpha.pack(anchor="w", padx=20, pady=(10, 0))
        
        self.slider_alpha = ctk.CTkSlider(self.sidebar_frame, from_=0.0, to=1.0, number_of_steps=20, command=self._update_slider_labels)
        self.slider_alpha.pack(pady=(2, 10), padx=20, fill="x")

        self.lbl_rings = ctk.CTkLabel(self.sidebar_frame, text="Gitter-Ringe (5):", font=ctk.CTkFont(weight="bold"))
        self.lbl_rings.pack(anchor="w", padx=20, pady=(10, 0))

        self.slider_rings = ctk.CTkSlider(self.sidebar_frame, from_=2, to=10, number_of_steps=8, command=self._update_slider_labels)
        self.slider_rings.pack(pady=(2, 10), padx=20, fill="x")
        
        ctk.CTkFrame(self.sidebar_frame, height=2, fg_color="gray30").pack(fill="x", pady=15, padx=20)

        # --- DATENSÄTZE & FARBEN ---
        ctk.CTkLabel(self.sidebar_frame, text="Farben der Datensätze:", font=ctk.CTkFont(weight="bold")).pack(anchor="w", padx=20)
        
        self.datasets_frame = ctk.CTkFrame(self.sidebar_frame, fg_color="transparent")
        self.datasets_frame.pack(fill="x", padx=20, pady=(5, 10))

        self.btn_apply = ctk.CTkButton(self.sidebar_frame, text="Ansicht aktualisieren", command=self.apply_changes, fg_color="#2b8256", hover_color="#1e5c3d")
        self.btn_apply.pack(pady=20, padx=20, fill="x")

        # --- RECHTES PANEL: LIVE VORSCHAU ---
        self.preview_frame = ctk.CTkFrame(self)
        self.preview_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        
        self.canvas = None
        self.current_chart = self._create_dummy_chart()
        
        self._sync_sidebar_from_chart()
        self.update_preview()

    def _on_data_edited(self):
        self._sync_sidebar_from_chart() 
        self.update_preview()           

    def open_data_editor(self):
        DataEditorWindow(self, self.current_chart, self._on_data_edited)

    def _create_dummy_chart(self) -> RadarChart:
        ds = RadarDataset(name="Beispiel", values=[50, 75, 60, 90, 80], color="#007ACC", marker="o", line_width=2.0)
        data = RadarData(title="Live Vorschau", labels=["Angriff", "Verteidigung", "Tempo", "Technik", "Ausdauer"], datasets=[ds])
        style = RadarStyle(frame="polygon", line_color="#000", fill_color="#000", fill=True, alpha=0.2, ring_count=5)
        return RadarChart(data=data, style=style)

    def _sync_sidebar_from_chart(self):
        self._is_updating_ui = True

        self.entry_title.delete(0, "end")
        self.entry_title.insert(0, self.current_chart.data.title)
        self.slider_alpha.set(self.current_chart.style.alpha)
        self.slider_rings.set(self.current_chart.style.ring_count)
        self._update_slider_labels()

        for widget in self.datasets_frame.winfo_children():
            widget.destroy()

        for ds in self.current_chart.data.datasets:
            row_frame = ctk.CTkFrame(self.datasets_frame, fg_color="transparent")
            row_frame.pack(fill="x", pady=5)
            
            lbl = ctk.CTkLabel(row_frame, text=ds.name)
            lbl.pack(side="left")
            
            btn_color = ctk.CTkButton(
                row_frame, text="", width=40, height=20, corner_radius=4,
                border_width=1, border_color="gray50", fg_color=ds.color, 
                hover_color=ds.color, command=lambda dataset=ds: self._change_dataset_color(dataset)
            )
            btn_color.pack(side="right")

        self._is_updating_ui = False

    def _change_dataset_color(self, dataset):
        color_result = colorchooser.askcolor(title=f"Farbe für {dataset.name}", initialcolor=dataset.color)
        hex_color = color_result[1]
        if hex_color:
            dataset.color = hex_color
            self._sync_sidebar_from_chart()
            self.update_preview()

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