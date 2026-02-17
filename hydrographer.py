import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# plt.rcParams.update({
#     "text.usetex": True,
#     "font.family": "sans-serif",
#     "font.sans-serif": "Helvetica",
# })
# plt.rcParams["text.latex.preamble"] += r"\usepackage{sfmath}"

CFS_TO_CMS: float = 0.3048 ** 3.0

df = pd.read_csv(
    "streamflow_data.tsv", sep="\t", comment="#", dtype=str
    ).iloc[1:, :][["datetime", "90085_00065"]].rename(
        columns={"90085_00065": "streamflow"}
    )

df["converted"] = df["streamflow"].astype(float) * CFS_TO_CMS
df["datetime"] = pd.to_datetime(df["datetime"])

fig, ax = plt.subplots(figsize=(6.4, 3.6))

locator = mdates.AutoDateLocator(minticks=3, maxticks=7)
formatter = mdates.ConciseDateFormatter(locator)
ax.xaxis.set_major_locator(locator)
ax.xaxis.set_major_formatter(formatter)

ax.plot(df["datetime"], df["converted"])
ax.set_xlabel("DateTime [UTC]")
ax.set_ylabel("Streamflow ($m^{3} s^{-1}$)")

fig.tight_layout()
fig.savefig("hydrograph.png", dpi=300)
