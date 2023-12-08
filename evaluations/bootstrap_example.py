import pandas as pd
import matplotlib.pyplot as plt
from arch.bootstrap import StationaryBootstrap, optimal_block_length
from arviz import hdi

from hydrotools.metrics.metrics import nash_sutcliffe_efficiency

def main():
    # Load the data
    df = pd.read_csv("cat-52_cfs.csv")

    # Make some fake observations
    df["observed"] = df["predicted"].ewm(span=20).mean()

    # Determine optimal "block" length
    # Note: this is the average block length for stationary bootstrap
    # Stationary bootstrap will vary the blocklengths exponentially
    block_length = optimal_block_length(df[["predicted", "observed"]].values)["stationary"].max()

    # Sample the data in blocks with replacement
    bs = StationaryBootstrap(block_length, df)

    # Generate a distribution of NSE values
    nse_distribution = bs.apply(lambda d: nash_sutcliffe_efficiency(d["observed"], d["predicted"]))

    # Get the 95% confidence interval
    confidence_interval = bs.conf_int(lambda d: nash_sutcliffe_efficiency(d["observed"], d["predicted"])).flatten()

    # Alternatively, get the 95% highest density interval
    # Generally, either option is fine
    # HDI can be a bit more reslient if your statistic has a funky or skewed distribution
    density_interval = hdi(nse_distribution.flatten(), hdi_prob=0.95)

    # Compute plain NSE
    plain_nse = nash_sutcliffe_efficiency(df["observed"], df["predicted"])

    # Print
    print(f"NSE: {plain_nse:.2f}")
    print(f"Confidence interval (95%): {confidence_interval}")
    print(f"Highest density interval (95%): {density_interval}")

    # Plot
    fig, ax = plt.subplots()
    ax.errorbar(
        x=[1],
        y=[plain_nse],
        yerr=[[plain_nse-confidence_interval[0]], [confidence_interval[1]-plain_nse]],
        fmt=".")
    ax.errorbar(
        x=[2],
        y=[plain_nse],
        yerr=[[plain_nse-density_interval[0]], [density_interval[1]-plain_nse]],
        fmt=".")
    ax.set_ylabel("NSE")
    ax.set_xticks([1, 2])
    ax.set_xticklabels(["CI", "HDI"])
    ax.set_xlim(0, 3)
    ax.set_title("NSE with error bars")
    fig.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
