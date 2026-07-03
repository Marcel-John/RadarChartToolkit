import numpy as np
import matplotlib.pyplot as plt

from models import RadarChart

def _compute_geometry(num_vars: int):
    """Berechnet Winkel und Einheitsvektoren für das Radar Chart."""

    angles = np.linspace(
        np.pi / 2,
        2 * np.pi + np.pi / 2,
        num_vars,
        endpoint=False
    )

    unit = np.c_[np.cos(angles), np.sin(angles)]

    return angles, unit

def _setup_axes():
    """Erstellt Figure und Axes."""

    fig, ax = plt.subplots()

    ax.set_aspect("equal")
    ax.axis("off")

    return fig, ax

def _draw_frame(ax, unit):
    """Zeichnet den äußeren Polygonrahmen."""

    closed = np.vstack([unit, unit[0]])
    ax.plot(closed[:, 0], closed[:, 1], color="black")

def _draw_grid(ax, unit):
    """Zeichnet die Radiallinien und Polygonringe."""

    for x, y in unit:
        ax.plot([0, x], [0, y], color="gray", alpha=0.4)

    levels = [2, 4, 6, 8, 10]

    for r in levels:
        radius = r / 10.0

        ring = unit * radius
        ring = np.vstack([ring, ring[0]])

        ax.plot(ring[:, 0], ring[:, 1], color="gray", alpha=0.2)

        ax.text(
            -0.03,
            radius,
            str(r),
            ha="right",
            va="center",
            fontsize=8
        )

def _draw_labels(ax, unit, labels):
    """Zeichnet die Achsenbeschriftungen."""

    for label, (x, y) in zip(labels, unit):
        ax.text(
            x * 1.1,
            y * 1.1,
            label,
            ha="center",
            va="center"
        )

def _draw_datasets(ax, unit, datasets, style):
    """Zeichnet alle Datensätze."""

    for ds in datasets:
        values = np.array(ds.values) / 10.0

        points = unit * values[:, None]
        points = np.vstack([points, points[0]])

        ax.plot(points[:, 0], points[:, 1], label=ds.name)
        ax.fill(points[:, 0], points[:, 1], alpha=style.alpha)

def plot_chart(chart: RadarChart):
    labels = chart.data.labels

    _, ax = _setup_axes()

    _, unit = _compute_geometry(len(labels))

    _draw_frame(ax, unit)
    _draw_grid(ax, unit)
    _draw_labels(ax, unit, labels)
    _draw_datasets(ax, unit, chart.data.datasets, chart.style)

    ax.set_title(chart.data.title)
    ax.legend()

    plt.show()