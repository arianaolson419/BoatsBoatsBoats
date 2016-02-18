from sympy import *
from math import *
from sympy.abc import x, y, z
import matplotlib.pyplot as plt

def boat_hull(y, n):
	return y**n - 1

def water_line(y, theta, d):
	return tan(theta*pi/180)*y - d

def another_line(y, theta, d):
	return (-1/tan(theta*pi/180))*y - d

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

def heeled_over1(hull, L, y_int, water_int, hull_int, argument):					   #returns integral of hull to waterline L when the boat is flipped partly over, ie theta > 90 degrees
	return integrate(integrate(argument, (z, L, 0)), (y, water_int[0], y_int[len(y_int)-1])) + integrate(integrate(argument, (z, hull[1], 0)), (y, y_int[len(y_int)-1], hull_int[1]))

def heeled_over2(hull, L, y_int, water_int, hull_int, argument):					   #returns integral of hull to waterline L when the boat is flipped partly over, ie theta > 90 degrees
	return integrate(integrate(argument, (z, L, 0)), (y, water_int[0], y_int[len(y_int)-1])) + integrate(integrate(argument, (z, hull[0], 0)), (y, y_int[len(y_int)-1], 0)) + integrate(integrate(argument, (z, hull[1], 0)), (y, 0, hull_int[1]))

def heeled_over3(hull, L, y_int, water_int, hull_int, argument):					   #returns integral of hull to waterline L when the boat is flipped partly over, ie theta > 90 degrees
	return integrate(integrate(argument, (z, L, 0)), (y, water_int[0], y_int[len(y_int)-1])) + integrate(integrate(argument, (z, hull[1], 0)), (y, y_int[len(y_int)-1], hull_int[1]))

def heeled_over4(hull, L, y_int, water_int, hull_int, argument):					   #returns integral of hull to waterline L when the boat is flipped partly over, ie theta > 90 degrees
	return integrate(integrate(argument, (z, hull[0], L)), (y, y_int[0], 0)) + integrate(integrate(argument, (z, hull[1], L)), (y, 0, y_int[1]))

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
	# print y_int
	water_int = solve(water)
	hull_int = [solve(hull[0])[0], -solve(hull[0])[0]]

	if theta < 90:										#now calculate it
		if water_int == [] or water_int[0]>=hull_int[1]:
			return above_water(hull, water, y_int, argument)
		else:
			return hull_part_submerged(hull, water, y_int, water_int, hull_int, argument)
	else:
		if abs(water_int[0]) <= hull_int[1]:
			if water_int[0] >= 0:
				return heeled_over1(hull, water, y_int, water_int, hull_int, argument)
			elif d >= 1:
				return heeled_over2(hull, water, y_int, water_int, hull_int, argument)
			else:
				return heeled_over3(hull, water, y_int, water_int, hull_int, argument)
		else:
			return integrate_boat(argument, params) - heeled_over4(hull, water, y_int, water_int, hull_int, argument)
	if theta == 180:
		print 'yer flipped matey'


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

def plot_boat(com, cob, vector_cob_com, vector_buoyancy, params):
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
	another_line1 = another_line(y, theta, -com[1])
	plot_another_line = []
	for i in minus:
		hull_plot.append(hull[0].subs(y, i)) #negative boat hull
	for i in plus:
		hull_plot.append(hull[1].subs(y, i)) #positive boat hull
	for i in minus:
		waterline_plot.append(water.subs(y, i)) #negative waterline
	for i in plus:
		waterline_plot.append(water.subs(y, i)) #positive waterline
	for i in minus:
		plot_another_line.append(another_line1.subs(y, i))
	for i in plus:
		plot_another_line.append(another_line1.subs(y, i))
	plt.title(str(theta))
	plt.plot(minus+plus, hull_plot, 'b') # hull
	plt.plot(minus+plus, waterline_plot, 'g') #waterline
	plt.plot(minus+plus, plot_another_line, 'y')
	plt.plot(minus+plus, hull_top_plot, 'b')
	plt.plot(com[0], com[1], 'go')
	plt.plot(cob[0], cob[1], 'ro')
	plt.plot([com[0], com[0]+vector_cob_com[0]], [com[1], com[1]+vector_cob_com[1]], 'r')
	plt.plot([0, vector_buoyancy[0]], [0, vector_buoyancy[1]], 'r')
	plt.plot([0,0], [0, -1], 'b')
	axes = plt.gca()
	axes.set_xlim([-1,1])
	axes.set_ylim([-1,1])
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

for k in range(0, 20):
	theta = 170-10*k
	print theta
	params = [1, theta, .6]
	cob = boat_cob(params)
	com =  boat_com(params)
	print cob
	print com
	difference_cob_com = [0]*3
	for i in range(3):
		difference_cob_com[i] = cob[i]-com[i]
	vector_cob_com = Matrix((difference_cob_com))
	if theta <= 90:
		vector_buoyancy = Matrix(([cos(pi/4-theta*pi/180), sin(pi/4-theta*pi/180), 0]))
	else:
		vector_buoyancy = Matrix(([cos(-pi/4+theta*pi/180), sin(-pi/4+theta*pi/180), 0]))
	cross_result = vector_cob_com.cross(vector_buoyancy)[2]
	print cross_result
	if cross_result<0:
		print 'rights'
	if cross_result>0:
		print 'tips'
	if cross_result==0:
		print 'sits'
	# if theta > 90:	
	# 	if cross_result>0:
	# 		print 'rights'
	# 	if cross_result<0:
	# 		print 'tips'
	# 	if cross_result==0:
	# 		print 'sits'
	plot_boat(com, cob, vector_cob_com, vector_buoyancy, params)