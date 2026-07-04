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
                    "values": ds.values,
                    "color": ds.color,
                    "marker": ds.marker,
                    "line_width": ds.line_width
                }
                for ds in chart.data.datasets
            ]
        },
        "style": {
            "frame": chart.style.frame,
            "line_color": chart.style.line_color,
            "fill_color": chart.style.fill_color,
            "fill": chart.style.fill,
            "alpha": chart.style.alpha,

            "ring_count": chart.style.ring_count,

            "frame_width": chart.style.frame_width,
            "grid_width": chart.style.grid_width,

            "label_distance": chart.style.label_distance,
            "scale_label_offset": chart.style.scale_label_offset,

            "grid_alpha": chart.style.grid_alpha,
            "dpi": chart.style.dpi
        }
    }

# json->Object
def from_dict(data: dict) -> RadarChart:
    datasets = [
        RadarDataset(
            name=ds["name"],
            values=ds["values"],
            color=ds.get("color", "#007ACC"),
            marker=ds.get("marker", "o"),
            line_width=ds.get("line_width", 2.0)
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
        alpha=data["style"]["alpha"],
        ring_count=data["style"]["ring_count"],

        frame_width=data["style"]["frame_width"],
        grid_width=data["style"]["grid_width"],

        label_distance=data["style"]["label_distance"],
        scale_label_offset=data["style"]["scale_label_offset"],

        grid_alpha=data["style"]["grid_alpha"],
        dpi=data["style"].get("dpi", 300)
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