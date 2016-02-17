from sympy import *
from math import *
from sympy.abc import x, y, z
import matplotlib.pyplot as plt

def boat_hull(y, n):
	return y**n - 1

def water_line(y, theta, d):
	return tan(theta*pi/180)*y -d

def above_water(hull, L, y_int, argument):                    #returns integral of hull to waterline L when the whole top of the hull is above water
	if y_int[0]<0:
		return integrate(integrate(argument, (z, hull[0], L)), (y, y_int[0], 0))+integrate(integrate(argument, (z, hull[1], L)), (y, 0, y_int[1]))
	else:
		return integrate(integrate(argument, (z, hull[1], L)), (y, y_int[0], y_int[1]))

def hull_part_submerged(hull, L, y_int, water_int, hull_int, argument):            #returns integral of hull to waterline L when the part of the top of the hull is submerged
	if water_int[0]>=0:
		if y_int[0]>=0:
			return integrate(integrate(argument, (z, hull[1], L)), (y, y_int[0], water_int[0]))+integrate(integrate(argument, (z, hull[1], L)), (y, water_int[0], hull_int[1]))
		else:
			return integrate(integrate(argument, (z, hull[0], L)), (y, y_int[0], 0))+integrate(integrate(argument, (z, hull[1], L)), (y, 0, water_int[0]))+integrate(integrate(argument, (z, hull[1], 0)), (y, water_int[0], hull_int[1]))
	else:
		return integrate(integrate(argument, (z, hull[0], L)), (y, y_int[0], water_int[0]))+integrate(integrate(argument, (z, hull[0], 0)), (y, water_int[0], 0))+integrate(integrate(argument, (z, hull[1], 0)), (y, 0, hull_int[1]))

def heeled_over1(hull, L, argument):					   #returns integral of hull to waterline L when the boat is flipped partly over, ie theta > 90 degrees
	pass

def intersect_solve(hull, water):
	y_int = []
	y_int_temp = solve(hull[0]-water)			       #solve for boat-water intersection

	for intercept in y_int_temp:					   #eliminate imaginary results
		if type(intercept)!=Add and intercept<0:
			y_int.append(intercept)

	y_int_temp = solve(hull[1]-water)					#repeat for other half of hull

	for intercept in y_int_temp:
		if type(intercept)!=Add and intercept>=0:
			y_int.append(intercept)
	return y_int


def integrate_water(argument, params):                                  
	""" Returns integral of some argument over the submerged part of a boat.
	Assumes that at least some of the boat is underwater, the boat is not completely submerged and that theta (angle of hull top to waterline) is positive
	"""

	n = params[0]
	theta = params[1]										   #unpack variables
	d = params[2]
	
	hull = [boat_hull(-y, n), boat_hull(y, n)]         #create equations
	water = water_line(y, theta, d)

	y_int = intersect_solve(hull, water)
	water_int = solve(water)
	hull_int = [solve(hull[0])[0], -solve(hull[0])[0]]

	if theta < 90:										#now calculate it
		if water_int == [] or water_int[0]>=hull_int[1]:
			return above_water(hull, water, y_int, argument)
		else:
			return hull_part_submerged(hull, water, y_int, water_int, hull_int, argument)
	else:
		if abs(water_int[0]) <= hull_int[1]:
			pass


def integrate_boat(argument, params):                                  
	""" Returns integral of some argument over the submerged part of a boat.
	Assumes that at least some of the boat is underwater, the boat is not completely submerged and that theta (angle of hull top to waterline) is positive
	"""
	n = params[0]
	theta = params[1]										   #unpack variables
	d = params[2]

	hull = [boat_hull(-y, n), boat_hull(y, n)]         #create equations
	water = water_line(y, 0, 0)
	
	hull_int = []

	hull_int = [solve(hull[0])[0], -solve(hull[0])[0]]

	return above_water(hull, water, hull_int, argument)

def plot_boat(com, cob, params):
	n = params[0]
	theta = params[1]										   #unpack variables
	d = params[2]
	
	hull = [boat_hull(-y, n), boat_hull(y, n)]         #create equations
	water = water_line(y, theta, d)

	minus = [i*.01 for i in range(-100, 0)] 			#now plot it
	plus = [i*.01 for i in range(0, 100)]
	hull_plot = []
	waterline_plot = []
	hull_top_plot = [0]*200
	for i in minus:
		hull_plot.append(hull[0].subs(y, i))
	for i in plus:
		hull_plot.append(hull[1].subs(y, i))
	for i in minus:
		waterline_plot.append(water.subs(y, i))
	for i in plus:
		waterline_plot.append(water.subs(y, i))

	plt.plot(minus+plus, hull_plot, 'b')
	plt.plot(minus+plus, waterline_plot, 'g')
	plt.plot(minus+plus, hull_top_plot, 'b')
	plt.plot(com[0], com[1], 'go')
	plt.plot(cob[0], cob[1], 'ro')
	plt.show()

def boat_cob(params):
	args = [y, z]
	cob = []
	for arg in args:
		vector_cob = integrate_water(arg, params)
		cob.append(vector_cob/integrate_water(1, params))
	cob.append(0)									#this part's x
	return cob

def boat_com(params):
	args = [y, z]
	com = []
	for arg in args:
		vector_com = integrate_boat(arg, params)
		com.append(vector_com/integrate_boat(1, params))
	com.append(0)									#this part's x
	return com

params = [2, 15, .5]
print integrate_boat(1, params)
print integrate_water(1, params)
cob = boat_cob(params)
com =  boat_com(params)
print com
print cob
plot_boat(com, cob, params)