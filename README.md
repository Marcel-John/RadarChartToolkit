# RadarChartToolkit

Ein Python-Toolkit mit grafischer Benutzeroberfläche (CustomTkinter) zum Erstellen, Bearbeiten, Vergleichen und Exportieren von Radar Charts (Spinnennetz-Diagrammen).

## Funktionen

- **Grafischer Editor (GUI):** Moderne Benutzeroberfläche auf Basis von CustomTkinter.
- **Multi-Datensatz Support:** Beliebig viele Datensätze (z.B. verschiedene Helden/Charaktere) im selben Diagramm vergleichen.
- **Dynamische Datenbearbeitung:** Hinzufügen, Bearbeiten und Löschen von Kategorien (Achsen) und Datensätzen über ein integriertes Tabellen-Pop-up.
- **Farbanpassung:** Individuelle Farbwahl für jeden Datensatz über ein integriertes Farb-Palette-Menü.
- **Live-Vorschau & Style-Regler:** Echtzeit-Anpassung von Titel, Transparenz (Alpha) und Anzahl der Gitter-Ringe.
- **Excel Import & Export:** Laden und Speichern von Diagramm-Daten inklusive Farb- und Style-Einstellungen in `.xlsx`-Dateien.
- **Bild-Export:** Exportieren der fertigen Radar Charts als hochauflösende PNG-Grafik oder SVG-Vektorgrafik.

## Installation

Repository klonen:

```bash
git clone [https://github.com/Marcel-John/RadarChartToolkit.git](https://github.com/Marcel-John/RadarChartToolkit.git)
cd RadarChartToolkit
```

### Virtuelle Umgebung erstellen (Empfohlen)

```bash
python -m venv venv
venv\Scripts\activate      # Windows
# source venv/bin/activate  # Mac/Linux
```

### Abhängigkeiten installieren

```bash
pip install -r requirements.txt
```

## Anwendung starten

Starte den grafischen Editor einfach über:

```bash
python editor.py
```

## Projektstruktur

- `editor.py` – Hauptprogramm mit der grafischen CustomTkinter Benutzeroberfläche & Live-Vorschau.
- `models.py` – Datentypen und Datenmodell (`RadarChart`, `RadarDataset`, `RadarStyle`).
- `radar_plot.py` – Matplotlib-Renderlogik zum Erzeugen und Exportieren des Radar Charts.
- `excel_handler.py` – Import- und Export-Logik für Excel-Dateien (`.xlsx`).
- `excel_validator.py` – Überprüft die Struktur geladener Excel-Dateien auf Gültigkeit.
- `json_handler.py` – Import- und Export-Logik für JSON-Dateien.

## Contributing

This project is maintained by the author only.

Bug reports and feature requests are welcome via GitHub Issues, but pull requests are currently not accepted.