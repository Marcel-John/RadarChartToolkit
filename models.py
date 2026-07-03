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

# combining RadarData and RadarStyle for easy acces
@dataclass
class RadarChart:
    data: RadarData
    style: RadarStyle