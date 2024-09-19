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
        xlim: tuple[float, float],
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
    ax.set_xlim(xlim)
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
        xlim=(-0.5, 2.5),
        ylabel="Nash-Sutcliffe Model Efficiency",
        title="Which model is better?"
    )
    fig.tight_layout()
    plt.savefig("figures/nse_01.png")
    plt.close()

    # Add error bars
    fig, ax = plt.subplots(figsize=(6.4, 3.6), dpi=300)
    plot_points(
        ax=ax,
        x=[0.0, 1.0],
        y=[0.4, 0.6],
        yerr=[0.2, 0.4],
        xtick_labels=["Model A", "Model B"],
        yticks=[0.0, 0.2, 0.4, 0.6, 0.8, 1.0],
        xlim=(-0.5, 2.5),
        ylabel="Nash-Sutcliffe Model Efficiency",
        title="Which model is better?"
    )
    ax.text(2.45, -0.05, "(95% Confidence)", ha="right")
    fig.tight_layout()
    plt.savefig("figures/nse_02.png")
    plt.close()

    # Add baseline
    fig, ax = plt.subplots(figsize=(6.4, 3.6), dpi=300)
    plot_points(
        ax=ax,
        x=[0.0, 1.0, 2.0],
        y=[0.4, 0.6, 0.45],
        yerr=[0.2, 0.4, 0.1],
        xtick_labels=["Model A", "Model B", "Baseline"],
        yticks=[0.0, 0.2, 0.4, 0.6, 0.8, 1.0],
        xlim=(-0.5, 2.5),
        ylabel="Nash-Sutcliffe Model Efficiency",
        title="Which model is better?"
    )
    ax.text(2.45, -0.05, "(95% Confidence)", ha="right")
    fig.tight_layout()
    plt.savefig("figures/nse_03.png")
    plt.close()

    # Add floods
    fig, ax = plt.subplots(figsize=(6.4, 3.6), dpi=300)
    plot_points(
        ax=ax,
        x=[0.0, 1.0, 2.0],
        y=[0.4, 0.6, 0.45],
        yerr=[0.2, 0.4, 0.1],
        xtick_labels=["Model A", "Model B", "Baseline"],
        yticks=[0.0, 0.2, 0.4, 0.6, 0.8, 1.0],
        xlim=(-0.5, 2.5),
        ylabel="Nash-Sutcliffe Model Efficiency",
        title="Which model is better?"
    )
    ax.text(2.45, -0.05, "(95% Confidence)", ha="right")
    ax.text(-0.48, 1.03, "High-flow Events: 47")
    fig.tight_layout()
    plt.savefig("figures/nse_04.png")
    plt.close()

    # Add droughts
    fig, ax = plt.subplots(figsize=(6.4, 3.6), dpi=300)
    plot_points(
        ax=ax,
        x=[0.0, 1.0, 2.0],
        y=[0.4, 0.6, 0.45],
        yerr=[0.2, 0.4, 0.1],
        xtick_labels=["Model A", "Model B", "Baseline"],
        yticks=[0.0, 0.2, 0.4, 0.6, 0.8, 1.0],
        xlim=(-0.5, 2.5),
        ylabel="Nash-Sutcliffe Model Efficiency",
        title="Which model is better?"
    )
    ax.text(2.45, -0.05, "(95% Confidence)", ha="right")
    ax.text(-0.48, 1.03, "High-flow Events: 47")
    ax.text(-0.48, 0.95, "Low-flow Events: 13")
    fig.tight_layout()
    plt.savefig("figures/nse_05.png")
    plt.close()

    # Add period of record
    fig, ax = plt.subplots(figsize=(6.4, 3.6), dpi=300)
    plot_points(
        ax=ax,
        x=[0.0, 1.0, 2.0],
        y=[0.4, 0.6, 0.45],
        yerr=[0.2, 0.4, 0.1],
        xtick_labels=["Model A", "Model B", "Baseline"],
        yticks=[0.0, 0.2, 0.4, 0.6, 0.8, 1.0],
        xlim=(-0.5, 2.5),
        ylabel="Nash-Sutcliffe Model Efficiency",
        title="Which model is better?"
    )
    ax.hlines(0.38, -0.5, 2.5, color="C1", linestyles="dashed", label="Risk Tolerance")
    ax.text(2.45, -0.05, "(95% Confidence)", ha="right")
    ax.text(-0.48, 1.03, "High-flow Events: 47")
    ax.text(-0.48, 0.95, "Low-flow Events: 13")
    ax.legend(edgecolor="white")
    fig.tight_layout()
    plt.savefig("figures/nse_06.png")
    plt.close()

    # Add pass criterion
    fig, ax = plt.subplots(figsize=(6.4, 3.6), dpi=300)
    plot_points(
        ax=ax,
        x=[0.0, 1.0, 2.0],
        y=[0.4, 0.6, 0.45],
        yerr=[0.2, 0.4, 0.1],
        xtick_labels=["Model A", "Model B", "Baseline"],
        yticks=[0.0, 0.2, 0.4, 0.6, 0.8, 1.0],
        xlim=(-0.5, 2.5),
        ylabel="Nash-Sutcliffe Model Efficiency",
        title="Which model is better?"
    )
    ax.text(2.45, -0.05, "(95% Confidence)", ha="right")
    ax.hlines(0.38, -0.5, 2.5, color="C1", linestyles="dashed", label="Risk Tolerance")
    ax.text(-0.48, 1.03, "High-flow Events: 47")
    ax.text(-0.48, 0.95, "Low-flow Events: 13")
    ax.text(-0.48, 0.87, "Period of Record: 2 years")
    ax.legend(edgecolor="white")
    fig.tight_layout()
    plt.savefig("figures/nse_07.png")
    plt.close()

if __name__ == "__main__":
    main()
