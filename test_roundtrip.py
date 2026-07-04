import os  # <-- Neu hinzugefügt
from models import RadarChart, RadarData, RadarDataset, RadarStyle
from excel_handler import save_chart, load_chart

def run_roundtrip_test():
    original_datasets = [
        RadarDataset(name="Spieler A", values=[80.0, 90.0, 70.0, 85.0]),
        RadarDataset(name="Spieler B", values=[60.0, 75.0, 85.0, 70.0])
    ]
    
    original_data = RadarData(
        title="Roundtrip Test Chart",
        labels=["Angriff", "Verteidigung", "Tempo", "Ausdauer"],
        datasets=original_datasets
    )
    
    original_style = RadarStyle(
        frame="polygon",
        line_color="#FF0000",
        fill_color="#FF0000",
        fill=True,
        alpha=0.4,
        ring_count=5
    )
    
    original_chart = RadarChart(data=original_data, style=original_style)
    
    test_filepath = "data/excel/roundtrip_test.xlsx"
    
    print("Starte Excel Roundtrip Test...")
    
    try:
        # NEU: Erstellt den Ordner 'data/excel/', falls er noch nicht existiert
        os.makedirs(os.path.dirname(test_filepath), exist_ok=True)
        
        # Speichern
        save_chart(original_chart, test_filepath)
        print("-> Chart erfolgreich gespeichert.")
        
        # Laden
        loaded_chart = load_chart(test_filepath)
        print("-> Chart erfolgreich geladen.")
        
        # Überprüfung (Asserts)
        assert loaded_chart.data.title == original_chart.data.title, "Titel ungleich!"
        assert loaded_chart.data.labels == original_chart.data.labels, "Labels ungleich!"
        assert len(loaded_chart.data.datasets) == len(original_chart.data.datasets), "Anzahl Datensätze ungleich!"
        
        for orig_ds, load_ds in zip(original_chart.data.datasets, loaded_chart.data.datasets):
            assert orig_ds.name == load_ds.name, f"Dataset-Name ungleich: {orig_ds.name} vs {load_ds.name}"
            assert orig_ds.values == load_ds.values, f"Dataset-Werte ungleich für {orig_ds.name}"
            
        assert loaded_chart.style.frame == original_chart.style.frame, "Style: frame ungleich!"
        assert loaded_chart.style.ring_count == original_chart.style.ring_count, "Style: ring_count ungleich!"
        assert float(loaded_chart.style.alpha) == original_chart.style.alpha, "Style: alpha ungleich!"
        
        print("\n🎉 JUCHHU! Der Roundtrip-Test war zu 100% erfolgreich. Die Daten sind identisch.")
        
    except AssertionError as e:
        print(f"\n❌ Test fehlgeschlagen: {e}")
    except Exception as e:
        print(f"\n❌ Unerwarteter Fehler beim Roundtrip: {e}")

if __name__ == "__main__":
    run_roundtrip_test()