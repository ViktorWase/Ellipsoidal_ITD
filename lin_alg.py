from math import sqrt

def dot(a, b):
	assert len(a)==len(b)
	return sum(a[i]*b[i] for i in range(len(a)))

def cross(a, b):
	c = [a[1]*b[2] - a[2]*b[1],
		a[2]*b[0] - a[0]*b[2],
		a[0]*b[1] - a[1]*b[0]]
	return c

def normalize(vec):
	size = sqrt(sum(v*v for v in vec))
	return [v/size for v in vec]
