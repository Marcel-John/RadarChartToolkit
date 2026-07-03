import numpy as np
import matplotlib.pyplot as plt

from models import RadarChart


def plot_chart(chart: RadarChart):
    labels = chart.data.labels
    datasets = chart.data.datasets

    num_vars = len(labels)

    # angles
    angles = np.linspace(np.pi / 2, 2*np.pi + np.pi/2, num_vars, endpoint=False)

    # unit circle points
    unit = np.c_[np.cos(angles), np.sin(angles)]

    fig, ax = plt.subplots()

    ax.set_aspect('equal')
    ax.axis('off')

    # polygon frame
    closed = np.vstack([unit, unit[0]])
    ax.plot(closed[:, 0], closed[:, 1], color="black")

    # radial lines
    for x, y in unit:
        ax.plot([0, x], [0, y], color="gray", alpha=0.4)

    # labels
    for i, (x, y) in enumerate(unit):
        ax.text(x*1.1, y*1.1, labels[i], ha="center", va="center")

    # datasets
    for ds in datasets:
        vals = np.array(ds.values)
        vals = vals / 10.0  # normalize (wichtig!)
        pts = unit * vals[:, None]
        pts = np.vstack([pts, pts[0]])

        ax.plot(pts[:, 0], pts[:, 1], label=ds.name)
        ax.fill(pts[:, 0], pts[:, 1], alpha=chart.style.alpha)
    
    levels = [2, 4, 6, 8, 10]
    for r in levels:
        radius = r / 10.0
        ring = unit * (r / 10.0)
        ring = np.vstack([ring, ring[0]])
        ax.plot(ring[:, 0], ring[:, 1], color="gray", alpha=0.2)

        # Zahlen anzeigen
        ax.text(
        -0.03,
        radius,
        str(r),
        ha="right",
        va="center",
        fontsize=8
        )
    
    

    ax.set_title(chart.data.title)
    ax.legend()

    plt.show()