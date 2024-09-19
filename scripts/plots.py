"""Random plots for presentations."""
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy.typing as npt

def plot_points(
        ax: mpl.axes.Axes,
        x: npt.ArrayLike,
        y: npt.ArrayLike,
        yerr: npt.ArrayLike,
        xtick_labels: npt.ArrayLike,
        yticks: npt.ArrayLike,
        ylabel: str,
        title: str
) -> mpl.axes.Axes:
    """Make a point plot."""
    ax.errorbar(
        x,
        y,
        yerr,
        fmt=".",
        capsize=2.0,
        )
    ax.set_xlim(min(x)-0.5, max(x)+0.5)
    ax.set_ylim(-0.1, 1.1)
    ax.set_xticks(x, labels=xtick_labels)
    ax.set_yticks(yticks)
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    return ax

def main():
    """Main."""
    # Plot minimal figure
    fig, ax = plt.subplots(figsize=(6.4, 3.6), dpi=300)
    plot_points(
        ax=ax,
        x=[0.0, 1.0],
        y=[0.4, 0.6],
        yerr=[0.0, 0.0],
        xtick_labels=["Model A", "Model B"],
        yticks=[0.0, 0.2, 0.4, 0.6, 0.8, 1.0],
        ylabel="Nash-Sutcliffe Model Efficiency",
        title="Which model is better?"
    )
    fig.tight_layout()
    plt.savefig("figures/nse_01.png")
    plt.close()

    # Plot minimal figure w/ error bars
    fig, ax = plt.subplots(figsize=(6.4, 3.6), dpi=300)
    plot_points(
        ax=ax,
        x=[0.0, 1.0],
        y=[0.4, 0.6],
        yerr=[0.2, 0.3],
        xtick_labels=["Model A", "Model B"],
        yticks=[0.0, 0.2, 0.4, 0.6, 0.8, 1.0],
        ylabel="Nash-Sutcliffe Model Efficiency",
        title="Which model is better?"
    )
    fig.tight_layout()
    plt.savefig("figures/nse_02.png")
    plt.close()

    # Plot full figure
    fig, ax = plt.subplots(figsize=(6.4, 3.6), dpi=300)
    plot_points(
        ax=ax,
        x=[0.0, 1.0, 2.0],
        y=[0.4, 0.6, 0.45],
        yerr=[0.2, 0.3, 0.1],
        xtick_labels=["Model A", "Model B", "Baseline"],
        yticks=[0.0, 0.2, 0.4, 0.6, 0.8, 1.0],
        ylabel="Nash-Sutcliffe Model Efficiency",
        title="Which model is better?"
    )
    fig.tight_layout()
    plt.savefig("figures/nse_05.png")
    plt.close()

if __name__ == "__main__":
    main()
