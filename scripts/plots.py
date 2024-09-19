"""Random plots for presentations."""
import matplotlib.pyplot as plt

def plot_points():
    """Make a point plot."""
    fig, ax = plt.subplots(figsize=(6.4, 3.6), dpi=300)
    ax.plot([0.0, 1.0], [0.5, 0.6])
    fig.tight_layout()
    plt.savefig("plot.png")

def main():
    """Main."""
    plot_points()

if __name__ == "__main__":
    main()
