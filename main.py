import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib.offsetbox import AnchoredText
import matplotlib.lines as mlines
import numpy as np
import math
import time

# Function that update acceleration ax and ay
def update_a(theta, r, g):
	a = -g*math.sin(theta)/r
	return(a)

# Function that convert degrees in radiants
def deg2rad(theta_deg):
	return(theta_deg*math.pi/360)

# Parameters
g = 9.80665

# Initial conditions
r = float(input('Length of the wire[m]: '))
theta = math.radians(float(input('Initial angle[deg]: ')))
Tapprox = 2*math.pi*(r/g)**(1/2)
print('Approximated period for small oscillations[s]: T = ', Tapprox)
dt = float(input('Time step for integration[s]: '))
nT = float(input('Approximated number of T to compute: '))
steps = round(nT*Tapprox/dt)

# Trajectory plot-Leapfrog integration
print('Computing the trajectory...')
fig = plt.figure()
axes = fig.add_subplot(1, 1, 1)
figManager = plt.get_current_fig_manager()  # Fullscreen mode
figManager.full_screen_toggle()
exit = AnchoredText('Type ctrl+w to exit', prop = dict(size = 9), frameon = True, loc = 2) # Exit instruction
exit.patch.set_boxstyle('round,pad=0.,rounding_size=0.2')
axes.add_artist(exit)
axes.set_aspect('equal', 'box')
a = update_a(theta, r, g)
half_T_count = 0
T_est = 0
s = 0
w = 0
for i in range(steps):
	w_old = w
	w1_2 = w + a*dt/2 # Half step
	theta = theta + w1_2*dt
	a = update_a(theta, r, g)
	w = w1_2 + a*dt/2
	#print([theta, w, a])
	rx = r*math.sin(theta)
	ry = -r*math.cos(theta)
	s = s + 1
	if w_old*w < 0: # Estimation of the half period
		T_est = T_est + s*dt
		half_T_count = half_T_count + 1
		s = 0
	# Plot
	line = mlines.Line2D([0, rx], [0, ry], color = 'black')
	axes.add_line(line)
	plt.scatter(rx, ry, facecolor = 'red', s = 100)
plt.show()
T_est = 2/half_T_count*T_est
print('Estimated true period[s]: T = ', T_est)
