#encoding=utf-8

import numpy as np
#import matplotlib
#matplotlib.use('Agg')
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


fig = plt.figure(figsize=(6,6), facecolor='white')
ax = fig.add_axes([0,0,1,1], frameon=False, aspect=1)

#number of drip
n = 50
size_min = 50
size_max = 50*50

#drip position 
p = np.random.uniform(0, 1, (n, 2)) # low,high,size(=n*2)
# colors 
c = np.ones((n, 4)) * (0,0,0,1)
c[:,3] = np.linspace(0,1,n)
#size 
s = np.linspace(size_min, size_max, n)
#scatter plot
scat = ax.scatter(p[:,0], p[:,1], s=s, lw=0.5,
	edgecolors=c, facecolor='None')

ax.set_xlim(0, 1), ax.set_xticks([])
ax.set_ylim(0, 1), ax.set_yticks([])	

def update(frame):
	global p, c, s
	c[:,3] = np.maximum(0, c[:,3]-1.0/n)
	s += (size_max-size_min)/n

	i = frame % 50
	p[i] = np.random.uniform(0,1,2)
	s[i] = size_min
	c[i, 3] = 1

	scat.set_edgecolors(c)
	#scat.set_sizes(s)
	scat.set_offsets(p)

	return scat

#animation = FuncAnimation(fig, update, interval=10, blit=True, frames=200)
#animation.save('rain.gif', writer='imagemagick', fps=30, dpi=40)

plt.show()