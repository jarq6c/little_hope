import numpy as np
import matplotlib.pyplot as plt
plt.style.use("tableau-colorblind10")

def plot_association(x, y, size, ofile):
    fig, ax = plt.subplots(figsize=(size, size), dpi=300)
    ax.plot(x, y, ".")
    ax.plot(x, x, "--")
    ax.set_xlim(0.0, 1.0)
    ax.set_xticks([0.0, 1.0], labels=["", ""])
    ax.set_yticks([0.0, 1.0], labels=["", ""])
    ax.set_ylim(0.0, 1.0)
    ax.set_aspect("equal")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.set_xlabel("Observed")
    ax.set_ylabel("Simulated")
    ax.text(0.02, 0.9, "$r^2 = 0.73$")
    fig.tight_layout()
    plt.savefig(ofile)

def plot_bias(x, y, size, ofile):
    fig, ax = plt.subplots(figsize=(size, size), dpi=300)
    ax.boxplot([x, y])
    ax.set_xticklabels(["Observed", "Simulated"])
    ax.set_yticks([0.0, 1.6], labels=["", ""])
    ax.set_ylim(0.0, 1.6)
    ax.set_aspect("equal")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.set_ylabel("Streamflow")
    ax.text(0.6, 1.4, "$MSE = 0.26$")
    fig.tight_layout()
    plt.savefig(ofile)

def main():
    rng = np.random.default_rng(seed=2024)
    x = np.linspace(0.1, 0.85, 100)
    y = x + rng.normal(0.0, 0.1, 100)
    plot_association(x, y, 2.5, "association.png")
    plot_bias(x, y+0.5, 2.5, "bias.png")

if __name__ == "__main__":
    main()
