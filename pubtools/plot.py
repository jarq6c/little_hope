# Requirements
import matplotlib.pyplot as plt
from pathlib import Path
from pandas.plotting import register_matplotlib_converters
import seaborn as sns
import matplotlib as mpl

# Use package style sheet
_root = Path(__file__).parent.resolve()
style_sheet = _root / 'matplotlibrc'
style_sheet = style_sheet.resolve()
plt.style.use(str(style_sheet))

# Register converters
register_matplotlib_converters()

# Plot settings
current_palette = sns.color_palette('colorblind')
sns.set_palette(current_palette)

def hist(x, bins=20, density=True, dpi=100, output_file=None, 
    legend=None, xlabel=None, ylabel=None,
    xlim=None, ylim=None, title=None):
    """Use the state-machine to plot a basic histogram."""
    # Plot
    plt.hist(x, bins=bins, density=density)
    plt.gcf().set_dpi(dpi)

    # Set legend
    if legend != None:
        plt.legend(legend)

    # Set xlabel
    if xlabel != None:
        plt.xlabel(xlabel)

    # Set ylabel
    if ylabel != None:
        plt.ylabel(ylabel)

    # Set xlim
    if xlim != None:
        plt.xlim(xlim)

    # Set ylim
    if ylim != None:
        plt.ylim(ylim)

    # Set title
    if title != None:
        plt.title(title)
    
    # Show plot
    if output_file == None:
        plt.show()
    else:
        plt.savefig(output_file)

def plot(x, y, fmt, dpi=100, output_file=None, 
    legend=None, xlabel=None, ylabel=None,
    xlim=None, ylim=None, title=None):
    """Generate a basic plot using state-machine."""
    # Plot
    plt.plot(x, y, fmt)

    # # Plot data
    # if columns == None:
    #     df.plot(ax=ax, logy=logy)
    # else:
    #     df[columns].plot(ax=ax, logy=logy)

    # # Set legend
    # if legend != None:
    #     ax.legend(legend)

    # # Set xlabel
    # if xlabel != None:
    #     ax.set_xlabel(xlabel)

    # # Set ylabel
    # if ylabel != None:
    #     ax.set_ylabel(ylabel)

    # # Set xlim
    # if xlim != None:
    #     ax.set_xlim(xlim)

    # # Set ylim
    # if ylim != None:
    #     ax.set_ylim(ylim)

    # # Set title
    # if title != None:
    #     ax.set_title(title)
    
    # Show plot
    if output_file == None:
        plt.show()
    else:
        plt.savefig(output_file)
    

def plot_dataframe(df, logy=False, dpi=100, columns=None, 
    output_file=None, legend=None, xlabel=None, ylabel=None,
    xlim=None, ylim=None, title=None):
    """Plot a pandas.DataFrame"""
    # Get blank plot
    fig, ax = plt.subplots(dpi=dpi)

    # Plot data
    if columns == None:
        df.plot(ax=ax, logy=logy)
    else:
        df[columns].plot(ax=ax, logy=logy)

    # Set legend
    if legend != None:
        ax.legend(legend)

    # Set xlabel
    if xlabel != None:
        ax.set_xlabel(xlabel)

    # Set ylabel
    if ylabel != None:
        ax.set_ylabel(ylabel)

    # Set xlim
    if xlim != None:
        ax.set_xlim(xlim)

    # Set ylim
    if ylim != None:
        ax.set_ylim(ylim)

    # Set title
    if title != None:
        ax.set_title(title)
    
    # Show plot
    if output_file == None:
        plt.show()
    else:
        fig.savefig(output_file)
    