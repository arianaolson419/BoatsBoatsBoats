from sympy import *
from math import *
from sympy.abc import x, y, z
def boat_hull(y, n):
	return y**n - 1

def water_line(y, theta, d):
	return tan(theta*pi/180)*y -d

def above_water(hull, L, y_int, argument):                    #returns integral of hull to waterline L when the whole top of the hull is above water
	pass

def hull_part_submerged(hull, L, y_int, water_int, argument):            #returns integral of hull to waterline L when the part of the top of the hull is submerged
	pass

def vertical(hull, L, argument):                       #returns integral of hull to waterline L when the boat is perfectly on its side
	pass

def heeled_over(hull, L, argument):					   #returns integral of hull to waterline L when the boat is flipped partly over, ie theta > 90 degrees
	pass

def integrate_boat():                                  
	""" Returns integral of some argument over the submerged part of a boat.
	Assumes that at least some of the boat is underwater, and that theta (angle of hull top to waterline) is positive
	"""
	n = 3
	theta = 15
	d = .5
	argument = 1
	
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

	water_int = solve(water)
	hull_int = [solve(hull[0])[0], -solve(hull[0])[0]]
	
	# if theta <

integrate_boat()