from json_handler import load_chart
from radar_plot import plot_chart


def main():
    # Pfad zur Testdatei
    filepath = "data/json/test.json"

    try:
        chart = load_chart(filepath)
        print(f"Loaded chart: {chart.data.title}")

        plot_chart(chart)

    except FileNotFoundError:
        print(f"File not found: {filepath}")
    except Exception as e:
        print(f"Error while running chart system: {e}")


if __name__ == "__main__":
    main()