from random import gauss
from math import sqrt

from lin_alg import *

def get_plane_vectors_from_normal_3d(normal):
	vec1 = [normal[1], normal[0], 0.0]
	vec2 = cross(vec1, normal)

	vec1 = normalize(vec1)
	vec2 = normalize(vec2)

	return (vec1, vec2)

def find_t_by_optimization(n, ear_p, x0):
	# Create plane-vectors
	(p1, p2) = get_plane_vectors_from_normal_3d(n)

	print("Here!", dot(p1, p2), dot(p1, n), dot(p2, n))

	def error_func(pos, n, ear_p, x0, p1, p2):
		assert False # The pos_3d is not actually on the plane. Big nono.
		pos_3d = [pos[0]*p1[i] + pos[1]*p2[i]+x0[i] for i in range(3)]

		dist_pow2 = sum((pos_3d[i]-ear_p[i])**2 for i in range(3))
		violation = sum(n[i]*(pos_3d[i]-x0[i]) for i in range(3)) - 1.0
		penalty = 1.0
		violation = penalty * violation*violation

		return violation
		return dist_pow2 + violation

	best_pos = [0.0, 0.0]
	best_error = error_func(best_pos, n, ear_p, x0, p1, p2)

	for _ in range(1000):
		pos = [x+gauss(0,1.0e-3) for x in best_pos]
		err = error_func(pos, n, ear_p, x0, p1, p2)

		if err < best_error:
			best_error = err
			best_pos = pos
			print(err, pos)

			if err < 1.0e-4:
				break

	return [pos[0]*p1[i] + pos[1]*p2[i]+x0[i] for i in range(3)]

def get_3d_pos_on_ellipse_path_from_parameter(start_p, end_p, par, ear_p, x0, A_diag):
	pos_uncorrected = [start_p[i]*(1-par) + end_p[i]*par for i in range(3)]

	# Find a length that puts it on the ellipse using binary search!
	r_min = 0.0
	r_max = 1.0 # TODO: Fix!

	ellipse_root_func = lambda r: sum(A_diag[i] * (r*pos_uncorrected[i]+ear_p[i]-x0[i]) for i in range(3)) - 1.0

	min_val = ellipse_root_func(r_min)
	assert min_val <= 0
	max_val = ellipse_root_func(r_max)

	for _ in range(100):
		r_mid = 0.5*(r_min+r_max)
		mid_val = ellipse_root_func(r_mid)

		if mid_val < 0:
			r_min = r_mid
		elif mid_val >0:
			r_max = r_mid
		else:
			break
	r = r_mid

	"""
	# Find a length that puts it on the ellipse using Newton-Raphson
	r = 1.0
	for _ in range(100):
		f = sum(((r*pos_uncorrected[i]-x0[i]+ear_p[i])/A_diag[i])**2 for i in range(3)) - 1.0
		f_d = 2.0 * sum((r*pos_uncorrected[i]-x0[i]+ear_p[i])*pos_uncorrected[i]/A_diag[i] for i in range(3))

		r -= f/f_d

		if fabs(f) < 1.0e-8:
			break
	"""
	return [pos_uncorrected[i]*r+ear_p[i] for i in range(3)]
	

def ellipse_dist(start_p, end_p, par_1, par_2, ear_p, x0, A_diag):
	pos1 = get_3d_pos_on_ellipse_path_from_parameter(start_p, end_p, par_1, ear_p, x0, A_diag)
	pos2 = get_3d_pos_on_ellipse_path_from_parameter(start_p, end_p, par_2, ear_p, x0, A_diag)

	return sqrt(sum((pos1[i]-pos2[i])**2 for i in range(3)))

def arc_length_ellipse(ear_p, t, ear, x0, A_diag):
	plane_vec_1 = [t[i]-ear_p[i] for i in range(3)]
	plane_vec_2 = [ear[i]-ear_p[i] for i in range(3)]

	res = 1000
	h = 1.0/(res)
	return sum(ellipse_dist(plane_vec_1, plane_vec_2, i*h, (i+1)*h, ear_p, x0, A_diag) for i in range(res))
	

def elliptical_time(source, a1, a2, a3, ear_back, ear_down, right_ear=True, c=343.0):
	A_diag = [1.0/(a1*a1), 1.0/(a2*a2), 1.0/(a3*a3)]

	x0 = [0.0, ear_back, ear_down]
	n = [A_diag[i]*(source[i]-x0[i]) for i in range(3)]

	if right_ear:
		ear = [a1*sqrt(1.0-(ear_back/a2)**2 - (ear_down/a3)**2), 0.0, 0.0] # +- depending on the ear
	else:
		ear = [-a1*sqrt(1.0-(ear_back/a2)**2 - (ear_down/a3)**2), 0.0, 0.0] # +- depending on the ear


	tmp = sum( n[i]*(source[i]-ear[i]) for i in range(3) )
	lambd = (1.0-sum(n[i]*(ear[i]-x0[i]) for i in range(3)))*tmp

	ear_p = [ear[i] - lambd*(source[i] - ear[i]) for i in range(3)]

	# TODO: Check if the ear is on the "front" or the "back" of 
	# the head from the point of the source

	t = find_t_by_optimization(n, ear_p, x0)

	d2 = arc_length_ellipse(ear_p, t, ear, x0, A_diag)

	d1 = sqrt( sum((source[i]-t[i])**2 for i in range(3)) )

	return (d1+d2)/c

if __name__ == '__main__':
	source = [0.0, 1.0, 0.0]
	a1 = 0.08
	a2 = 0.08
	a3 = 0.08
	ear_back = 0.01
	ear_down = 0.01
	time = elliptical_time(source, a1, a2, a3, ear_back, ear_down)
	print(time)
