from Point import Point
import math

def translation(initial_object, translation_vector):
	matrix = [
        [1, 0, 0, translation_vector.x],
        [0, 1, 0, translation_vector.y],
        [0, 0, 1, translation_vector.z],
    ]

	return Point(
		matrix[0][3] + initial_object.x,
		matrix[1][3] + initial_object.y,
		matrix[2][3] + initial_object.z
	)

def rotation(initial_object, angle, rotated_axis):
	angle = math.radians(angle)

	if rotated_axis == 'x':
		rotation_matrix = \
			[[1, 0, 0],
			[0, math.cos(angle), -math.sin(angle)],
			[0, math.sin(angle), math.cos(angle)]]

	elif rotated_axis == 'y':
		rotation_matrix = \
			[[math.cos(angle), 0, math.sin(angle)],
            [0, 1, 0],
			[-math.sin(angle), 0, math.cos(angle)]]

	else:
		rotation_matrix = \
			[[math.cos(angle), -math.sin(angle), 0],
			[math.sin(angle), math.cos(angle), 0],
			[0, 0, 1]]

	x, y, z = (initial_object.x, initial_object.y, initial_object.z)

	rx = rotation_matrix[0][0] * x + rotation_matrix[0][1] * y + rotation_matrix[0][2] * z
	ry = rotation_matrix[1][0] * x + rotation_matrix[1][1] * y + rotation_matrix[1][2] * z
	rz = rotation_matrix[2][0] * x + rotation_matrix[2][1] * y + rotation_matrix[2][2] * z

	return Point(rx, ry, rz)

