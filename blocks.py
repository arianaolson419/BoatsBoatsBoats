def torque1(blocks, position):
	max_side = 10
	min_side = -10
	mass_total = 3
	torques_dict = {'a':4*(-8-position), 'b':10*(-4-position), 'c':10*(-3-position), 'd':4*(2-position), 'e':7*(5-position), 'f':8*(8-position)}
	torque_total = 0
	for block in blocks:
		torque_total+=torques_dict[block]
	torque_total += mass_total*(-position)
	return torque_total

blocks = ['a', 'b', 'c', 'd', 'e', 'f']
print torque1(blocks, -1.5), 'should be positive'
print torque1(blocks, 1.5), 'should be negative'