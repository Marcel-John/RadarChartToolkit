import os
from models import RadarChart, RadarData, RadarDataset, RadarStyle
from radar_plot import plot_chart, export_chart_image


def test_plotter_and_export():
    print("=== Starte Plotter & Export Test ===")

    # 1. Test-Daten mit unterschiedlichen Farben, Markern und Linienstärken erstellen
    dataset_a = RadarDataset(
        name="Held A (Offensiv)",
        values=[85.0, 50.0, 90.0, 65.0, 75.0],
        color="#E63946",   # Rot
        marker="o",        # Kreis-Punkte
        line_width=2.5
    )

    dataset_b = RadarDataset(
        name="Held B (Defensiv)",
        values=[45.0, 95.0, 40.0, 80.0, 90.0],
        color="#1D3557",   # Dunkelblau
        marker="s",        # Quadrat-Punkte ("s" für square)
        line_width=1.5
    )

    chart_data = RadarData(
        title="Helden-Vergleich",
        labels=["Angriff", "Verteidigung", "Tempo", "Technik", "Ausdauer"],
        datasets=[dataset_a, dataset_b]
    )

    chart_style = RadarStyle(
        frame="polygon",
        line_color="#000000",
        fill_color="#000000",
        fill=True,
        alpha=0.2,
        ring_count=5,
        dpi=300
    )

    chart = RadarChart(data=chart_data, style=chart_style)

    # 2. Ordner für Test-Exporte anlegen
    output_dir = "data/export"
    os.makedirs(output_dir, exist_ok=True)

    png_path = os.path.join(output_dir, "test_chart.png")
    svg_path = os.path.join(output_dir, "test_chart.svg")

    # 3. PNG-Export testen
    print(f"-> Exportiere PNG nach '{png_path}'...")
    export_chart_image(chart, png_path)
    
    if os.path.exists(png_path) and os.path.getsize(png_path) > 0:
        print("✅ PNG-Export erfolgreich!")
    else:
        print("❌ PNG-Export fehlgeschlagen!")

    # 4. SVG-Export testen
    print(f"-> Exportiere SVG nach '{svg_path}'...")
    export_chart_image(chart, svg_path)

    if os.path.exists(svg_path) and os.path.getsize(svg_path) > 0:
        print("✅ SVG-Export erfolgreich!")
    else:
        print("❌ SVG-Export fehlgeschlagen!")

    # 5. Interaktives Fenster testen (Matplotlib GUI)
    print("\n-> Öffne interaktives Diagramm-Fenster (Schließe das Fenster, um den Test zu beenden)...")
    plot_chart(chart)

    print("\n=== Test abgeschlossen ===")


if __name__ == "__main__":
    test_plotter_and_export()