import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import griddata
from scipy.spatial import Delaunay
from scipy.interpolate import Rbf

# Read data
fileread = open('avg_cei_combo.csv','r')

nlines = 320

conc = np.zeros(nlines,dtype=float)
grad = np.zeros(nlines,dtype=float)
cei = np.zeros(nlines,dtype=float)

rocc = np.zeros(nlines,dtype=float)
rodfb = np.zeros(nlines,dtype=float)
rdfb = np.zeros(nlines,dtype=float)

Kd = 1000.0

for i in range(nlines):
    
    s = fileread.readline()
    split = s.split(",")
    conc[i] = float(split[0])
    grad[i] = float(split[1])  # nano molar per mm
    cei[i] = float(split[2])
    
    if cei[i] < 0.0:
        cei[i] = 0.0
    
    rocc[i] = conc[i] / (conc[i] + Kd)

    grad_rocc = grad[i] * Kd / ((conc[i] + Kd)**2)    
    
    rocf = rocc[i] + grad_rocc * 0.005
    rocb = rocc[i] - grad_rocc * 0.005 
    
    rf = rocf*25000
    rb = rocb*25000
    
    
    rdfb[i] = np.log10(rf - rb)

fileread.close()

# Your computed arrays: rodfb, rocc, cei
x = rdfb
y = rocc
z = cei

# Define grid range
xi = np.linspace(min(x), max(x), 300)   # log-spaced for x
yi = np.linspace(min(y), max(y), 300)

# Build grid
XI, YI = np.meshgrid(xi, yi)

# Linear interpolation (unchanged)
rbf = Rbf(x, y, z, function='multiquadric', smooth=0.25)
ZI = rbf(XI, YI)

# -----------------------------------------------------------
# Add convex-hull shading for regions with no data
# -----------------------------------------------------------

# Build Delaunay triangulation of original data
hull = Delaunay(np.column_stack([x, y]))

# Determine which grid points lie OUTSIDE hull
pts = np.column_stack([XI.ravel(), YI.ravel()])
mask = hull.find_simplex(pts) < 0
mask = mask.reshape(XI.shape)

# -----------------------------------------------------------
# Plot
# -----------------------------------------------------------

plt.figure(figsize=(7,5))

# Main contour plot
cs = plt.contourf(XI, YI, ZI, levels=[-0.0, 0.15, 0.25, 0.35, 0.45, 0.55, 0.65], cmap='inferno')

# Overlay original scatter points
plt.scatter(x, y, c=z, s=20, cmap='inferno', edgecolor='gray', alpha=0.8)
ax = plt.gca()


# Shade outside-data region

plt.contourf(
    XI, YI, mask,
    levels=[0.5, 1],            # triggers shading of True mask
    colors=["#BBBBBB"],         # light grey
    alpha=0.6
)

#plt.xscale('log')
plt.xlabel('Difference in number of receptors between front and back',fontsize=12)
plt.ylabel('Background receptor occupancy',fontsize=12)
vals = np.array([0.1, 1.0, 3, 5, 10, 25, 60, 150, 400])
log_positions = np.log10(vals)

plt.xticks(log_positions, vals)

custom_ticks = [0.1, 0.3, 0.5, 0.7, 0.9, 0.95]
plt.yticks(custom_ticks)


cbar = plt.colorbar(cs)
cbar.set_label('Chemotactic Efficiency Index (CEI)',fontsize=12)


plt.savefig('combined_plot_rn.svg')

plt.show()
