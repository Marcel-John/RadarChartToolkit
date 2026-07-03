from openpyxl import Workbook, load_workbook
from openpyxl.worksheet.worksheet import Worksheet

from models import (
    RadarChart,
    RadarData,
    RadarDataset,
    RadarStyle,
)


def _load_meta(sheet: Worksheet) -> str:
    """Liest den Titel aus dem Meta-Sheet."""
    title = sheet["B2"].value
    
    if title is None:
        raise ValueError("Missing chart title.")
    
    return str(title)


def _load_data(sheet: Worksheet) -> tuple[list[str], list[RadarDataset]]:
    """Liest Labels und Datensätze aus dem Data-Sheet."""
    labels = []

    dataset_names = [
        str(cell.value)
        for cell in sheet[1][1:]
    ]

    datasets = [
        RadarDataset(
            name=name,
            values=[]
        )
        for name in dataset_names
    ]

    for row in sheet.iter_rows(min_row=2, values_only=True):
        if row[0] is None:
            raise ValueError("Missing label in Data sheet.")

        labels.append(str(row[0]))

        for i, dataset in enumerate(datasets):
            value = row[i + 1]
            if value is None:
                raise ValueError("Found empty cell in dataset.")

            if not isinstance(value, (int, float)):
                raise TypeError(
                    f"Expected numeric value, got {type(value).__name__}: {value}"
                    )

            dataset.values.append(float(value))

    return labels, datasets


def _load_style(sheet: Worksheet) -> RadarStyle:
    """Liest alle Style-Einstellungen."""
    values = {}

    for key, value in sheet.iter_rows(min_row=2, values_only=True):
        if key is None:
            continue
        values[str(key)] = value

    return RadarStyle(
        frame=values["frame"],
        line_color=values["line_color"],
        fill_color=values["fill_color"],
        fill=values["fill"],
        alpha=values["alpha"],
        ring_count=values["ring_count"],
        frame_width=values["frame_width"],
        grid_width=values["grid_width"],
        label_distance=values["label_distance"],
        scale_label_offset=values["scale_label_offset"],
        grid_alpha=values["grid_alpha"],
    )


def load_chart(filepath: str) -> RadarChart:
    """Lädt ein RadarChart aus einer Excel-Datei."""

    workbook = load_workbook(filepath)

    meta_sheet = workbook["Meta"]
    data_sheet = workbook["Data"]
    style_sheet = workbook["Style"]

    title = _load_meta(meta_sheet)

    labels, datasets = _load_data(data_sheet)

    style = _load_style(style_sheet)

    data = RadarData(
        title=title,
        labels=labels,
        datasets=datasets
    )

    return RadarChart(
        data=data,
        style=style
    )

def save_chart(chart: RadarChart, filepath: str):
    """Speichert ein RadarChart als Excel-Datei."""
    pass