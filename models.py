from dataclasses import dataclass

# allowing for multiple datasets allows comparison
@dataclass
class RadarDataset:
    name: str
    values: list[float]

# datastructure for storing the data
@dataclass
class RadarData:
    title: str
    labels: list[str]
    datasets: list[RadarDataset]

# storing of the style for the chart
@dataclass
class RadarStyle:
    frame: str
    line_color: str
    fill_color: str
    fill: bool
    alpha: float
    ring_count: int = 5

    frame_width: float = 2.0
    grid_width: float = 0.8

    label_distance: float = 1.1
    scale_label_offset: float = 0.03

    grid_alpha: float = 0.3

# combining RadarData and RadarStyle for easy acces
@dataclass
class RadarChart:
    data: RadarData
    style: RadarStyle