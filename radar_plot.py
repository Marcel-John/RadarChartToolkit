import numpy as np
import matplotlib.pyplot as plt

from models import RadarChart


def plot_chart(chart: RadarChart):
    labels = chart.data.labels
    datasets = chart.data.datasets

    num_vars = len(labels)

    # compute angles
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
    angles += angles[:1]  # closing the circle

    # prepare the plots
    fig, ax = plt.subplots(subplot_kw=dict(polar=True))

    # Polar settings
    ax.set_theta_offset(np.pi / 2)  # type: ignore
    ax.set_theta_direction(-1)      # type: ignore

    ax.set_thetagrids(np.degrees(angles[:-1]), labels) # type: ignore

    ax.set_rlabel_position(0)       # type: ignore
    ax.set_ylim(0, 10)

    # Daten plotten
    for ds in datasets:
        values = ds.values + ds.values[:1]

        ax.plot(angles, values, label=ds.name)
        ax.fill(angles, values, alpha=chart.style.alpha)

    ax.set_title(chart.data.title, pad=20)
    ax.legend(loc="upper right", bbox_to_anchor=(1.3, 1.1))

    plt.show()