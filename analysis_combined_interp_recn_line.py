#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import Rbf

# -----------------------------------------------------------
# Read data
# -----------------------------------------------------------

# Read data
fileread = open('avg_cei_combo.csv','r')

nlines = 320

conc = np.zeros(nlines, dtype=float)
grad = np.zeros(nlines, dtype=float)
cei = np.zeros(nlines, dtype=float)

rocc = np.zeros(nlines, dtype=float)
rodfb = np.zeros(nlines, dtype=float)
rdfb = np.zeros(nlines, dtype=float)

Kd = 1000.0

for i in range(nlines):

    s = fileread.readline()
    split = s.split(",")

    conc[i] = float(split[0])
    grad[i] = float(split[1])
    cei[i] = float(split[2])

    if cei[i] < 0.0:
        cei[i] = 0.0

    rocc[i] = conc[i] / (conc[i] + Kd)

    grad_rocc = grad[i] * Kd / ((conc[i] + Kd) ** 2)

    rocf = rocc[i] + grad_rocc * 0.005
    rocb = rocc[i] - grad_rocc * 0.005

    rf = rocf * 25000
    rb = rocb * 25000

    rdfb[i] = np.log10(rf - rb)

fileread.close()

# -----------------------------------------------------------
# Coordinates for interpolation
# -----------------------------------------------------------

x = rdfb          # log10(receptor difference)
y = rocc          # receptor occupancy
z = cei

# -----------------------------------------------------------
# RBF interpolation
# -----------------------------------------------------------

rbf = Rbf(
    x,
    y,
    z,
    function='multiquadric',
    smooth=0.25
)

# -----------------------------------------------------------
# Define equal-width strips in log-space
# -----------------------------------------------------------

centers = [40, 90, 150, 230]

log_halfwidth = 0.10

colors = [
    '#2563EB',   # blue
    '#DC2626',   # red
    '#F59E0B',   # orange
    '#000000'    # black
]
# -----------------------------------------------------------
# Plot
# -----------------------------------------------------------

plt.figure(figsize=(8, 6))

yline = np.linspace(0.05, 0.98, 500)

for center, color in zip(centers, colors):

    # -------------------------------------------------------
    # Strip boundaries in log-space
    # -------------------------------------------------------

    log_center = np.log10(center)

    xmin = log_center - log_halfwidth
    xmax = log_center + log_halfwidth

    # -------------------------------------------------------
    # Raw data inside strip
    # -------------------------------------------------------

    strip_mask = (
        (rdfb >= xmin) &
        (rdfb <= xmax)
    )

    occ_raw = rocc[strip_mask]
    cei_raw = cei[strip_mask]

    # -------------------------------------------------------
    # Sample interpolation across strip
    # -------------------------------------------------------

    xstrip = np.linspace(
        xmin,
        xmax,
        101
    )

    cei_mean = np.zeros_like(yline)
    cei_std = np.zeros_like(yline)

    for i, yy in enumerate(yline):

        vals = rbf(
            xstrip,
            np.full_like(xstrip, yy)
        )

        cei_mean[i] = np.mean(vals)
        cei_std[i] = np.std(vals)

    # -------------------------------------------------------
    # Legend label
    # -------------------------------------------------------

    rmin = 10**xmin
    rmax = 10**xmax

    label = (
        f'{rmin:.0f}-{rmax:.0f}'
    )

    # -------------------------------------------------------
    # Raw points
    # -------------------------------------------------------

    plt.scatter(
        occ_raw,
        cei_raw,
        s=40,
        color=color,
        alpha=0.35,
        zorder=3
    )

    # -------------------------------------------------------
    # Mean curve
    # -------------------------------------------------------

    plt.plot(
        yline,
        cei_mean,
        color=color,
        lw=3,
        label=label,
        zorder=4
    )

    # -------------------------------------------------------
    # Standard deviation band
    # -------------------------------------------------------

    plt.fill_between(
        yline,
        cei_mean - cei_std,
        cei_mean + cei_std,
        color=color,
        alpha=0.18,
        linewidth=0,
        zorder=2
    )

# -----------------------------------------------------------
# Formatting
# -----------------------------------------------------------

plt.xlabel('Background receptor occupancy', fontsize=14)
plt.ylabel('Chemotactic Efficiency Index (CEI)', fontsize=14)

plt.xlim([0.05, 0.9])
plt.ylim([0.0,0.6])

custom_ticks = [0.1, 0.3, 0.5, 0.7, 0.9]
plt.xticks(custom_ticks)
plt.yticks(fontsize=14)
plt.xticks(fontsize=14)

leg = plt.legend(
    title='front-back difference in number of active receptors',
    title_fontsize=14,
    frameon=False,
    fontsize=14,
    loc='upper right'
)

leg._legend_box.align = "left"

plt.tight_layout()

plt.savefig('cei_vertical_sweeps_logspace.svg')

plt.show()