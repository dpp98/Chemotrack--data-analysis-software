#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 21 02:45:14 2025

@author: devi
"""

import argparse
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde


# ----------- CLI ARGUMENTS -------------

parser = argparse.ArgumentParser(
    description="Generate half-violin plot from chemotaxis CSV data"
)

parser.add_argument(
    "input_csv",
    type=str,
    help="Input CSV file"
)

parser.add_argument(
    "--cmin",
    type=float,
    required=True,
    help="Minimum concentration (nM)"
)

parser.add_argument(
    "--cmax",
    type=float,
    required=True,
    help="Maximum concentration (nM)"
)

args = parser.parse_args()

fileread_name = args.input_csv
cmin_exp = args.cmin
cmax_exp = args.cmax


# ----------- AUTO-GENERATED OUTPUT NAMES -------------

fileout_name = f"avg_cei_{int(cmin_exp)}_{int(cmax_exp)}nM.csv"
figfilename = f"cei_vs_{int(cmin_exp)}_{int(cmax_exp)}nM.png"

fileout = open(fileout_name, 'w')


# ----------- AUTO-DETECT NUMBER OF LINES -------------

with open(fileread_name, 'r') as f:
    nlines = sum(1 for _ in f)

fileread = open(fileread_name, 'r')


# ----------- HELPERS -------------

def index_of_closest(value, array):
    differences = [abs(value - x) for x in array]
    return differences.index(min(differences))


def bounded_kde(data, low=-1, high=1, points=200):
    """
    KDE computed with reflection at boundaries.
    Prevents KDE from bending inward near ±1.
    """
    data = np.asarray(data)
    if len(data) < 2:
        y = np.linspace(low, high, points)
        pdf = np.zeros_like(y)
        return y, pdf

    reflect_low = 2 * low - data[data < (low + 0.1)]
    reflect_high = 2 * high - data[data > (high - 0.1)]
    reflected = np.concatenate([data, reflect_low, reflect_high])

    kde = gaussian_kde(reflected, bw_method='scott')
    y = np.linspace(low, high, points)
    pdf = kde(y)
    return y, pdf


def format_concentration(value_nm):
    """
    Format concentration for display:
      - 0      -> "0"
      - <1000  -> "XXX nM"
      - >=1000 -> "X.X µM"
    """
    if value_nm == 0:
        return "0"
    elif value_nm >= 1000:
        return f"{value_nm / 1000:.1f} µM"
    else:
        return f"{value_nm:.0f} nM"


# ----------- READ DATA -------------

nbins = 10
deltac_exp = (cmax_exp - cmin_exp) / 1000.0

xbins = [50,150,250,350,450,550,650,750,850,950]

cbins = np.zeros(nbins, dtype=float)
for i in range(nbins):
    cbins[i] = cmin_exp + deltac_exp * xbins[i]

cos = [[] for _ in range(nbins)]
spds = [[] for _ in range(nbins)]

chem = np.zeros(nlines, dtype=float)
costh = np.zeros(nlines, dtype=float)   # this is cei lazy enough to not change the variable name LOL!
speed = np.zeros(nlines, dtype=float)

for i in range(nlines):
    s = fileread.readline()
    if not s:
        break

    split = s.split()

    chem[i] = float(split[1])
    costh[i] = float(split[2])
    speed[i] = float(split[4])

    if abs(costh[i]) > 1.0:
        print(i, 'Nonsense', costh[i])


# ----------- BINNING -------------

# Neglect 50 nM on either side
cmin = cmin_exp + 50.0 * deltac_exp
cmax = cmax_exp - 50.0 * deltac_exp

avgcei = np.zeros(nbins)
avgspd = np.zeros(nbins)

for i in range(nlines):
    if cmin < chem[i] < cmax:
        indx = index_of_closest(chem[i], cbins)
        cos[indx].append(costh[i])
        spds[indx].append(speed[i])


# ----------- WRITE AVERAGES -------------

for i in range(nbins):
    avgcei[i] = np.mean(np.asarray(cos[i]))
    avgspd[i] = np.mean(np.asarray(spds[i]))
    fileout.write(f"{cbins[i]},{cmax_exp - cmin_exp},{avgcei[i]}\n")


# ----------- HALF-VIOLIN PLOT -------------

fig, ax = plt.subplots(figsize=(10, 6))

width = cbins[1] - cbins[0]

for i, yvals in enumerate(cos):

    ygrid, pdf = bounded_kde(yvals, low=-1, high=1, points=300)
    if pdf.max() > 0:
        pdf = pdf / pdf.max() * 0.5 * width
    else:
        pdf = np.zeros_like(pdf)

    x_center = cbins[i]
    xv = x_center - pdf

    ax.fill_betweenx(
        ygrid,
        xv,
        x_center,
        facecolor="skyblue",
        edgecolor="black",
        linewidth=1.0,
        alpha=1.0
    )

    mean_y = np.mean(yvals)
    mean_width = 0.3 * width
    ax.plot(
        [x_center - mean_width, x_center],
        [mean_y, mean_y],
        color="black",
        linewidth=3.0
    )

    jitter = (np.random.rand(len(yvals)) * 0.4 + 0.1) * 0.75 * width
    ax.scatter(
        x_center + jitter,
        yvals,
        s=10,
        alpha=0.2,
        color="purple"
    )


# ----------- LABELS & SAVE -------------

title = (
    rf"$C_{{min}}$ = {format_concentration(cmin_exp)}, "
    rf"$C_{{max}}$ = {format_concentration(cmax_exp)}"
)





#ax.set_title(title, fontsize=30)
#ax.set_xlabel('concentration (nM)', fontsize=20)
#ax.set_ylabel('chemotactic efficiency index', fontsize=20)

# Remove all x-axis ticks and labels
#ax.set_xticks([])

# Show x-ticks at the concentration bin centres
ax.set_xticks(cbins)
print(cbins)



labels = []
for x in cbins:
    if x >= 1000:
        labels.append(f"{x / 1000:.1f}")   # Convert to µM with one decimal place
    else:
        labels.append(f"{x:g}")            # Keep nM values

ax.set_xticklabels(labels, fontsize=24)

# Show only three y-axis ticks
ax.set_ylim(-1.05, 1.05)
ax.set_yticks([-1, -0.75, -0.50, -0.25, 0, 0.25, 0.50, 0.75, 1])
ax.set_yticklabels(
    ["-1.00", "-0.75", "-0.50", "-0.25", "0.00", "0.25", "0.50", "0.75", "1.00"],
    fontsize=20,
)


# Increase y-axis tick label size
ax.tick_params(axis='y', labelsize=24, width=2)
# Uniform border thickness
for spine in ax.spines.values():
    spine.set_linewidth(2)

# Fixed margins
fig.subplots_adjust(
    left=0.15,
    right=0.98,
    bottom=0.15,
    top=0.90
)
plt.tight_layout()
plt.savefig(figfilename, dpi=500)
#plt.show()

fileread.close()
fileout.close()
