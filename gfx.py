import math

import numpy as np

def array(v):
	return np.array(v, dtype=np.float32)

def asarray(v):
	return np.asarray(v, dtype=np.float32)

def norm(v):
	return math.sqrt(dot(v, v))

def normalize(v):
	return v / norm(v)

def dot(v0, v1):
	return v0[0]*v1[0] + v0[1]*v1[1] + v0[2]*v1[2]

def cross(v0, v1):
	return array([v0[1]*v1[2] - v0[2]*v1[1], v0[2]*v1[0] - v0[0]*v1[2], v0[0]*v1[1] - v0[1]*v1[0]])

def identityM():
	return array([
		[1, 0, 0, 0],
		[0, 1, 0, 0],
		[0, 0, 1, 0],
		[0, 0, 0, 1]
	])

def translateM(v):
	return array([
		[1, 0, 0, v[0]],
		[0, 1, 0, v[1]],
		[0, 0, 1, v[2]],
		[0, 0, 0,   1 ]
	])

def scaleM(s):
	return array([
		[s, 0, 0, 0],
		[0, s, 0, 0],
		[0, 0, s, 0],
		[0, 0, 0, 1]
	])

# https://en.wikipedia.org/wiki/Euler%E2%80%93Rodrigues_formula
def rotateM(axis, theta):
	a = math.cos(theta / 2)
	b, c, d = normalize(axis) * -math.sin(theta / 2)
	aa, bb, cc, dd = a * a, b * b, c * c, d * d
	bc, ad, ac, ab, bd, cd = b * c, a * d, a * c, a * b, b * d, c * d
	return array([
		[aa + bb - cc - dd,   2 * (bc + ad),     2 * (bd - ac)  ],
		[  2 * (bc - ad),   aa + cc - bb - dd,   2 * (cd + ab)  ],
		[  2 * (bd + ac),     2 * (cd - ab),   aa + dd - bb - cc],
	])

def perspectiveM(fovy, aspect, zNear, zFar):
	f = 1 / math.tan(fovy / 2)
	M = array([
		[f/aspect, 0,                0,                                   0               ],
		[    0,    f,                0,                                   0               ],
		[    0,    0, (zFar + zNear) / (zNear - zFar), (2 * zFar * zNear) / (zNear - zFar)],
		[    0,    0,               -1,                                   0               ]
	])
	return M

def lookatM(eye, center, up):
	eye, center, up = asarray(eye), asarray(center), asarray(up)
	f = normalize(center - eye)
	s = normalize(cross(f, up))
	u = cross(s, f)
	M = array([
		[ s[0],  s[1],  s[2], 0],
		[ u[0],  u[1],  u[2], 0],
		[-f[0], -f[1], -f[2], 0],
		[  0,     0,     0,   1]
	])
	return M @ translateM(-eye)
