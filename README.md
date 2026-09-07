# RadarChartToolkit

Ein Python-Toolkit mit grafischer Benutzeroberfläche (CustomTkinter) zum Erstellen, Bearbeiten, Vergleichen und Exportieren von Radar Charts (Spinnennetz-Diagrammen).

## Schnellstart (Windows App ohne Python)

Du musst Python nicht installiert haben, um das Toolkit zu nutzen!

1. Gehe auf die [Releases-Seite](https://github.com/Marcel-John/RadarChartToolkit/releases).
2. Lade die neueste `RadarChartToolkit.exe` herunter.
3. Starte die Datei direkt per Doppelklick.

⚠️ Hinweis zur Windows-Warnung:
Da dieses Tool ein kostenloses Open-Source-Projekt ist, besitzt es kein kommerzielles Entwickler-Zertifikat. Daher zeigt Windows beim ersten Start oft das blaue Fenster "Der Computer wurde durch Windows geschützt" an.
Lösung: Klicke in dem blauen Fenster einfach auf "Weitere Informationen" und danach auf "Trotzdem ausführen". Der Quellcode ist hier auf GitHub zu 100 % offen und transparent einsehbar.

---

## Funktionen

- **Grafischer Editor (GUI):** Moderne Benutzeroberfläche auf Basis von CustomTkinter.
- **Multi-Datensatz Support:** Beliebig viele Datensätze (z.B. verschiedene Helden/Charaktere) im selben Diagramm vergleichen.
- **Dynamische Datenbearbeitung:** Hinzufügen, Bearbeiten und Löschen von Kategorien (Achsen) und Datensätzen über ein integriertes Tabellen-Pop-up.
- **Farbanpassung:** Individuelle Farbwahl für jeden Datensatz über ein integriertes Farb-Palette-Menü.
- **Live-Vorschau & Style-Regler:** Echtzeit-Anpassung von Titel, Transparenz (Alpha) und Anzahl der Gitter-Ringe.
- **Excel Import & Export:** Laden und Speichern von Diagramm-Daten inklusive Farb- und Style-Einstellungen in `.xlsx`-Dateien.
- **Bild-Export:** Exportieren der fertigen Radar Charts als hochauflösende PNG-Grafik oder SVG-Vektorgrafik.

---

## Entwicklung & Start aus dem Quellcode

Falls du den Code anpassen oder das Projekt aus den Quelldateien ausführen möchtest:

### 1. Repository klonen

```bash
git clone [https://github.com/Marcel-John/RadarChartToolkit.git](https://github.com/Marcel-John/RadarChartToolkit.git)
cd RadarChartToolkit
```

### 2. Virtuelle Umgebung erstellen (Empfohlen)

```bash
python -m venv venv
venv\Scripts\activate      # Windows
# source venv/bin/activate  # Mac/Linux
```

### 3. Abhängigkeiten installieren

```bash
pip install -r requirements.txt
```

### 4. Anwendung starten

```bash
python editor.py
```

---

## Projektstruktur

- `editor.py` – Hauptprogramm mit der grafischen CustomTkinter Benutzeroberfläche & Live-Vorschau.
- `models.py` – Datentypen und Datenmodell (`RadarChart`, `RadarDataset`, `RadarStyle`).
- `radar_plot.py` – Matplotlib-Renderlogik zum Erzeugen und Exportieren des Radar Charts.
- `excel_handler.py` – Import- und Export-Logik für Excel-Dateien (`.xlsx`).
- `excel_validator.py` – Überprüft die Struktur geladener Excel-Dateien auf Gültigkeit.
- `json_handler.py` – Import- und Export-Logik für JSON-Dateien.

---

## Contributing

This project is maintained by the author only.

Bug reports and feature requests are welcome via GitHub Issues, but pull requests are currently not accepted.