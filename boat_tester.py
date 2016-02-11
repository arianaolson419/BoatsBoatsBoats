from sympy import *
from math import *
def boat_hull(y, n):
	return y**n - 1

def water_line(y, theta, d):
	return tan(theta)*y -d

def integrate_water(y, z, x, arg, params):						#right now i'm assuming d is within the boat.
	theta = params[0]
	d = params[1]
	n = params[2]

	water = water_line(y, theta, d)
	y_int = []

	if n%2 == 0:												#cases where n is even, and side doesn't matter
		boat = boat_hull(y, n)
		y_int = solve(water-boat, y)
		water_int = solve(water, y)
		hull_int = solve(boat, y)
		if water_int == [] or abs(water_int[0])>=abs(hull_int[0]):
			return integrate(integrate(arg, (z, boat, water)),(y, y_int[0], y_int[1]))
		elif water_int[0] > 0:
			return integrate(integrate(arg, (z, boat, water)),(y, y_int[0], water_int[0])) + integrate(integrate(arg, (z, boat, 0)),(y, water_int[0], hull_int[1]))
		elif water_int[0] < 0:
			return integrate(integrate(arg, (z, boat, 0)),(y, hull_int[0], water_int[0])) + integrate(integrate(arg, (z, boat, water)),(y, water_int[0], y_int[1]))
	else:
		boat_neg = boat_hull(-y, n)
		boat_pos = boat_hull(y, n)
		y_int_neg = solve(water-boat_neg, y)
		y_int_pos = solve(water-boat_pos, y)
		water_int = solve(water, y)
		hull_int = solve(boat_neg, y)
		hull_int.append(solve(boat_pos, y))
		for i in y_int_neg:
			if i < 0:
				y_int.append(i)
		for k in y_int_pos:
			if k > 0:
				y_int.append(k)
		if water_int == [] or abs(water_int[0])>=abs(hull_int[0]):
			return integrate(integrate(arg, (z, boat_neg, water)),(y, y_int[0], 0)) + integrate(integrate(arg, (z, boat_pos, water)),(y, 0, y_int[1]))
		elif water_int[0] > 0:
			return integrate(integrate(arg, (z, boat_neg, water)),(y, y_int[0], 0)) + integrate(integrate(arg, (z, boat_pos, water)),(y, 0, water_int[0])) + integrate(integrate(arg, (z, boat, 0)),(y, water_int[0], hull_int[1]))
		elif water_int[0] < 0:
			return integrate(integrate(arg, (z, boat, 0)), (y, hull_int[0], y_int[0])) + integrate(integrate(arg, (z, boat_pos, water)),(y, y_int[0], 0)) + integrate(integrate(arg, (z, boat_neg, water)),(y, 0, y_int[1]))
	# print integrate(integrate(arg, (z, boat, water)),(y, y_int[0], y_int[1]))


y = Symbol('y')
z = Symbol('z')
x = Symbol('x')

theta = pi/6              #radians
d = .5
n = 2

params = [theta, d, n]

print integrate_water(y, z, x, 1, params)
# print solve(boat_hull(y, n)-water_line(y, theta, d), y)