import numpy as np
import matplotlib.pyplot as plt
import math

from models import RadarChart

def _get_max_value(datasets):
    """Ermittelt den größten Wert aller Datensätze."""

    return max(
        max(dataset.values)
        for dataset in datasets
    )

def _calculate_scale(max_value: float, ring_count: int):
    """Berechnet eine sinnvolle Obergrenze und Skalenwerte."""

    upper = math.ceil(max_value / ring_count) * ring_count

    levels = np.linspace(
        upper / ring_count,
        upper,
        ring_count
    )

    return upper, levels

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

def _draw_frame(ax, unit, style):
    """Zeichnet den äußeren Polygonrahmen."""

    closed = np.vstack([unit, unit[0]])
    ax.plot(
    closed[:, 0],
    closed[:, 1],
    color="black",
    linewidth=style.frame_width
    )

def _draw_grid(ax, unit, levels, max_value, style):
    """Zeichnet die Radiallinien und Polygonringe."""

    for x, y in unit:
        ax.plot([0, x], [0, y], color="gray", linewidth=style.grid_width, alpha=style.grid_alpha)
    
    if max_value == 0:
        max_value = 1

    for r in levels:
        radius = r / max_value

        ring = unit * radius
        ring = np.vstack([ring, ring[0]])

        ax.plot(ring[:, 0], ring[:, 1], color="gray", linewidth=style.grid_width, alpha=style.grid_alpha)

        ax.text(
            -style.scale_label_offset,
            radius,
            str(r),
            ha="right",
            va="center",
            fontsize=8
        )

def _draw_labels(ax, unit, labels, style):
    """Zeichnet die Achsenbeschriftungen."""

    for label, (x, y) in zip(labels, unit):
        ax.text(
            x * style.label_distance,
            y * style.label_distance,
            label,
            ha="center",
            va="center"
        )

def _draw_datasets(ax, unit, datasets, style, max_value):
    """Zeichnet alle Datensätze."""

    for ds in datasets:
        values = np.array(ds.values) / max_value

        points = unit * values[:, None]
        points = np.vstack([points, points[0]])

        ax.plot(points[:, 0], points[:, 1], label=ds.name, color=style.line_color)
        if style.fill:
            ax.fill(points[:, 0], points[:, 1], color=style.fill_color, alpha=style.alpha)

def plot_chart(chart: RadarChart):
    labels = chart.data.labels

    _, ax = _setup_axes()

    _, unit = _compute_geometry(len(labels))

    max_value = _get_max_value(chart.data.datasets)

    max_value, levels = _calculate_scale(
        max_value,
        chart.style.ring_count
    )

    _draw_frame(ax, unit, chart.style)
    _draw_grid(ax, unit, levels, max_value, chart.style)
    _draw_labels(ax, unit, labels, chart.style)
    _draw_datasets(ax, unit, chart.data.datasets, chart.style, max_value)

    ax.set_title(chart.data.title)
    ax.legend()

    plt.show()