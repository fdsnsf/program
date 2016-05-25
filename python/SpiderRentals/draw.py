#encoding=utf-8

import numpy as np
#import matplotlib
#matplotlib.use('Agg')
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


def scatterplot(x, y, name):
	pl.plot(x, y, 'oc')
	#pl.show()
	pl.savefig(name+'.jpg')


def test2():
	x = [1, 2, 3, 4, 5]
	y = [1, 4, 9, 16, 25]

	#pl.plot(x, y)
	#pl.title('坐标系')
	pl.title('title')
	pl.plot(x, y, 'c*')

	pl.xlabel('x axis')
	pl.ylabel('y axis')
	pl.xlim(0.0, 9.0)
	pl.ylim(0.0, 30)

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

def test3():
	scatterplot([1,3,1,2,3],[2,5,4,4,3])

def test4():

	plt.figure(figsize=(8,6), dpi=80)
	plt.subplot(111)

	x = np.linspace(-np.pi, np.pi, 256, endpoint=True)
	c,s = np.cos(x), np.sin(x)

	plt.plot(x, c, color='blue', linewidth=1.0, linestyle='-')
	plt.plot(x, s, color='green', linewidth=1.0, linestyle='-')

	plt.xlim(-4.0, 4.0)
	

	plt.show()

if __name__ == '__main__':
	try:
		test4()
	except Exception, e:
		print e
	
