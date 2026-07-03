from dataclasses import dataclass

@dataclass
class RadarDataset:
    name: str
    values: list[float]

@dataclass
class RadarData:
    title: str
    labels: list[str]
    values: list[float]
    datasets: list[RadarDataset]

@dataclass
class RadarStyle:
    frame: str
    line_color: str
    fill_color: str
    fill: bool
    alpha: float

@dataclass
class RadarChart:
    data: RadarData
    style: RadarStyle