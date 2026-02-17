import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(0.0, 2.0*np.pi)
y = np.sin(x)

fig, ax = plt.subplots()
ax.plot(x, y)
ax.annotate(
    "UPPER RIGHT",
    xy=(1.0, 1.0),
    xycoords="figure fraction",
    horizontalalignment="right",
    verticalalignment="top"
    )
ax.annotate(
    "LOWER RIGHT",
    xy=(1.0, 0.0),
    xycoords="figure fraction",
    horizontalalignment="right",
    verticalalignment="bottom"
    )
ax.annotate(
    "UPPER LEFT",
    xy=(0.0, 1.0),
    xycoords="figure fraction",
    horizontalalignment="left",
    verticalalignment="top"
    )
ax.annotate(
    "LOWER LEFT",
    xy=(0.0, 0.0),
    xycoords="figure fraction",
    horizontalalignment="left",
    verticalalignment="bottom"
    )
fig.savefig("annotated_plot.png")
