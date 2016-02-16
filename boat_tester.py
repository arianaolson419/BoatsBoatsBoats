from sympy import *
from math import *
def boat_hull(y, n):
	return y**n - 1

def water_line(y, theta, d):
	return tan(theta)*y -d

def integrate_water(y, z, x, arg, params):						#the symbol being integrated, n, d, theta
	theta = params[0]
	d = params[1]
	n = params[2]

	water = water_line(y, theta, d)
	y_int = []

	if n%2 == 0:												#cases where n is even, and side doesn't matter
		#boat hull shape
		boat = boat_hull(y, n)
		#where the water intersects the boat
		y_int = solve(water-boat, y)
		#where the water intersects the x axis
		water_int = solve(water, y)
		#where the boat intersects the x axis
		hull_int = solve(boat, y)
		#if the water line does not intersect the boat deck. 
		if water_int == [] or abs(water_int[0])>=abs(hull_int[0]):
			#integral of arg (x, y, or z) for volume of displaced water in the arg unit vector direction
			return integrate(integrate(arg, (z, boat, water)),(y, y_int[0], y_int[1]))
		#if the yint of the water is positive
		elif water_int[0] > 0:
			return integrate(integrate(arg, (z, boat, water)),(y, y_int[0], water_int[0])) + integrate(integrate(arg, (z, boat, 0)),(y, water_int[0], hull_int[1]))
		#if yint water is negative
		elif water_int[0] < 0:
			return integrate(integrate(arg, (z, boat, 0)),(y, hull_int[0], water_int[0])) + integrate(integrate(arg, (z, boat, water)),(y, water_int[0], y_int[1]))
	else:									#working with two sides of the boat instead of the boat as a whole
		boat_neg = boat_hull(-y, n)
		boat_pos = boat_hull(y, n)
		y_int_neg = solve(water-boat_neg, y)
		y_int_pos = solve(water-boat_pos, y)
		water_int = solve(water, y)
		hull_int = [-1, 1]
		'''hull_int = solve(boat_neg, y)
								hull_int.append(solve(boat_pos, y))'''
		#find the positive intersection on the negative side of the boat
		for i in y_int_neg:
			if re(i) == i:
				y_int.append(i)
		#find the negative intersection on the positive side
		for k in y_int_pos:
			if re(k) == k:
				y_int.append(k)
		#if the waterline does not intersect the boat deck
		if water_int == [] or abs(water_int[0])>=abs(hull_int[0]):
			return integrate(integrate(arg, (z, boat_neg, water)),(y, y_int[0], 0)) + integrate(integrate(arg, (z, boat_pos, water)),(y, 0, y_int[1]))
		elif water_int[0] > 0:
			return integrate(integrate(arg, (z, boat_neg, water)),(y, y_int[0], 0)) + integrate(integrate(arg, (z, boat_pos, water)),(y, 0, water_int[0])) + integrate(integrate(arg, (z, boat_pos, 0)),(y, water_int[0], hull_int[1]))
		elif water_int[0] < 0:
			return integrate(integrate(arg, (z, boat_neg, 0)), (y, hull_int[0], y_int[0])) + integrate(integrate(arg, (z, boat_pos, water)),(y, y_int[0], 0)) + integrate(integrate(arg, (z, boat_neg, water)),(y, 0, y_int[1]))
	# print integrate(integrate(arg, (z, boat, water)),(y, y_int[0], y_int[1]))

def boat_cob(y, z, x, params):
	args = [y, z]
	cob = [0]
	for arg in args:
		vector_cob = integrate_water(y, z, x, arg, params)
		cob.append(vector_cob/integrate_water(y, z, x, 1, params))
	return cob


y = Symbol('y')
z = Symbol('z')
x = Symbol('x')

theta = pi/6        #radians
d = .5
n = 3

params = [theta, d, n]

print boat_cob(y, z, x, params)
# print solve(boat_hull(y, n)-water_line(y, theta, d), y)