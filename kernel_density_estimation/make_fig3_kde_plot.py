# This script reproduces Figure 3.

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import gaussian_kde
from matplotlib import gridspec
import matplotlib.colors as mcolors
from matplotlib import cm
import matplotlib.ticker as ticker


df = pd.read_csv("Fig_3.csv")
x = df.iloc[:, 0].values
y1 = df.iloc[:, 1].values
y2 = df.iloc[:, 2].values
y3 = df.iloc[:, 3].values


# Function with optional label and simplified grid (only at powers of 10)
def plot_density_for_composite(ax, x, y, title, show_ylabel=False):
    mask = (x > 0) & (y > 0)
    x_log, y_log = x[mask], y[mask]
    xy = np.vstack([x_log, y_log])
    z = gaussian_kde(xy)(xy)
    idx = z.argsort()
    x_log, y_log, z = x_log[idx], y_log[idx], z[idx]

    norm = mcolors.Normalize(vmin=np.min(z[z > 0]), vmax=np.max(z))

    # background before scatters
    x_fill = np.logspace(-2, 2, 500)
    y_lower_03 = x_fill - 0.4
    y_upper_03 = x_fill + 0.4
    y_lower_3 = x_fill - 4
    y_upper_3 = x_fill + 4
    #ax.fill_between(x_fill, y_lower_3, y_upper_3, color='royalblue', alpha=0.2, zorder=0, linestyle='--', linewidth=1.0)
    #color filled b/w y=x-3 and y=x+3
    
    sc = ax.scatter(x_log, y_log, c=z, s=5, cmap='viridis', norm=norm)
    
    ax.plot(x_fill, y_lower_3, color='royalblue', linestyle='--', linewidth=1)
    ax.plot(x_fill, y_upper_3, color='royalblue', linestyle='--', linewidth=1)
    ax.plot(x_fill, y_lower_03, color='lightcoral', linestyle='--', linewidth=1)
    ax.plot(x_fill, y_upper_03, color='lightcoral', linestyle='--', linewidth=1)
    #not color fill, dashed line only

    #ax.plot([0.01, 100], [0.01, 100], 'k--', linewidth=1)
    x_line = np.logspace(-2, 2, 500)
    ax.plot(x_line, x_line, 'k--', linewidth=1)

    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.set_xlim(0.01, 100)
    ax.set_ylim(0.01, 100)
    ax.set_xlabel("DFT forces [eV/Å]")

    if show_ylabel:
        ax.set_ylabel("Predicted forces [eV/Å]")
    else:
        ax.tick_params(labelleft=False)

    ax.grid(True, which='major', axis='both', color='lightgray', linestyle='--', linewidth=0.5)
    ax.xaxis.set_major_locator(ticker.LogLocator(base=10.0, subs=(1.0,), numticks=10))
    ax.yaxis.set_major_locator(ticker.LogLocator(base=10.0, subs=(1.0,), numticks=10))
    ax.tick_params(which='both', direction='in', length=4)

    ax.set_title(title, fontsize=12)
    return sc



# Create figure
fig = plt.figure(figsize=(11, 3))
gs = gridspec.GridSpec(1, 4, width_ratios=[1, 1, 1, 0.05], wspace=0.3)

# Axes
ax1 = fig.add_subplot(gs[0])
ax2 = fig.add_subplot(gs[1], sharex=ax1, sharey=ax1)
ax3 = fig.add_subplot(gs[2], sharex=ax1, sharey=ax1)
cax = fig.add_subplot(gs[3])

# Plot each subplot
sc1 = plot_density_for_composite(ax1, x, y1, "Zero-shot", show_ylabel=True)
plot_density_for_composite(ax2, x, y2, "From-scratch")
plot_density_for_composite(ax3, x, y3, "Fine-tuned")

# Add simplified colorbar
cbar = fig.colorbar(sc1, cax=cax, ticks=[])
cbar.ax.set_title("High density", fontsize=10, pad=10)
cbar.ax.set_xlabel("Low density", fontsize=10, labelpad=10)
cbar.ax.xaxis.set_label_position('bottom')

fig.subplots_adjust(bottom=0.2)
plt.savefig("Fig_5.png", dpi=400)
plt.savefig("Fig_5.svg", format="svg")
plt.show()
