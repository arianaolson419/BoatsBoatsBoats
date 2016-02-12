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
			return integrate(integrate(argument, (z, hull[0], L)), (y, y_int[0], 0))+integrate(integrate(argument, (z, hull[1], L)), (y, 0, water_int[0]))+integrate(integrate(argument, (z, hull[1], L)), (y, water_int[0], hull_int[1]))
	else:
		return integrate(integrate(argument, (z, hull[0], L)), (y, y_int[0], water_int[0]))+integrate(integrate(argument, (z, hull[0], 0)), (y, water_int[0], 0))+integrate(integrate(argument, (z, hull[1], 0)), (y, 0, hull_int[1]))
def vertical(hull, L, argument):                       #returns integral of hull to waterline L when the boat is perfectly on its side
	pass

def heeled_over(hull, L, argument):					   #returns integral of hull to waterline L when the boat is flipped partly over, ie theta > 90 degrees
	pass

def integrate_boat(argument):                                  
	""" Returns integral of some argument over the submerged part of a boat.
	Assumes that at least some of the boat is underwater, the boat is not completely submerged and that theta (angle of hull top to waterline) is positive
	"""
	n = 3
	theta = 0
	d = .5
	
	hull = [boat_hull(-y, n), boat_hull(y, n)]
	water = water_line(y, theta, d)

	y_int_temp = []
	y_int = []
	water_int = []
	hull_int = []

	y_int_temp = solve(hull[0]-water)
	for intercept in y_int_temp:
		if type(intercept)!=Add and intercept<0:
			y_int.append(intercept)
	y_int_temp = solve(hull[1]-water)
	for intercept in y_int_temp:
		if type(intercept)!=Add and intercept>=0:
			y_int.append(intercept)
	print y_int
	water_int = solve(water)
	hull_int = [solve(hull[0])[0], -solve(hull[0])[0]]
	print water_int
	if theta < 90:
		if water_int == [] or water_int[0]>=hull_int[1]:
			return above_water(hull, water, y_int, argument)
		else:
			return hull_part_submerged(hull, water, y_int, water_int, hull_int, argument)
	elif theta == 90:
		pass
	else:
		pass
	minus = [i*.01 for i in range(-100, 0)]
	plus = [i*.01 for i in range(0, 100)]
	a = []
	for i in minus:
		a.append(hull[0].subs(y, i))
	for i in plus:
		a.append(hull[1].subs(y, i))
	plt.plot(minus+plus, a)
	plt.show()

print integrate_boat(z)