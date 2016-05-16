#encoding=utf-8

import numpy as np
import matplotlib.pyplot as plt
import pylab as pl

# character color
# b blue
# g green
# r red
# c cyan
# m magenta
# y yellow
# k black
# w white

def test2():
	x = [1, 2, 3, 4, 5]
	y = [1, 4, 9, 16, 25]

	#pl.plot(x, y)
	pl.plot(x, y, 'c*')
	pl.show()

def test1():
	plt.figure(1)
	ax1 = plt.subplot(211)

	x = np.linspace(0, 3, 100)
	for i in xrange(5):
		plt.figure(1)
		plt.plot(x, np.exp(i*x/3))
		plt.sca(ax1)
		plt.plot(x, np.sin(i*x))

	plt.show()

if __name__ == '__main__':
	test2()
