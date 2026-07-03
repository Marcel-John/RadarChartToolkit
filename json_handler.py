import json
from models import RadarChart, RadarData, RadarDataset, RadarStyle

# converts Object -> json
def to_dict(chart: RadarChart) -> dict:
    return {
        "data": {
            "title": chart.data.title,
            "labels": chart.data.labels,
            "datasets": [
                {
                    "name": ds.name,
                    "values": ds.values
                }
                for ds in chart.data.datasets
            ]
        },
        "style": {
            "frame": chart.style.frame,
            "line_color": chart.style.line_color,
            "fill_color": chart.style.fill_color,
            "fill": chart.style.fill,
            "alpha": chart.style.alpha
        }
    }

# json->Object
def from_dict(data: dict) -> RadarChart:
    datasets = [
        RadarDataset(
            name=ds["name"],
            values=ds["values"]
        )
        for ds in data["data"]["datasets"]
    ]

    radar_data = RadarData(
        title=data["data"]["title"],
        labels=data["data"]["labels"],
        datasets=datasets
    )

    radar_style = RadarStyle(
        frame=data["style"]["frame"],
        line_color=data["style"]["line_color"],
        fill_color=data["style"]["fill_color"],
        fill=data["style"]["fill"],
        alpha=data["style"]["alpha"]
    )

    return RadarChart(
        data=radar_data,
        style=radar_style
    )


# saving data
def save_chart(chart: RadarChart, filepath: str):
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(to_dict(chart), f, indent=4)

# loading saved data
def load_chart(filepath: str) -> RadarChart:
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)

    return from_dict(data)