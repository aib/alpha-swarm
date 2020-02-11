import numpy as np

class NPNoise:
	def __init__(self):
		self.cube_bias = 100
		self.noise_cube = np.random.random((200, 200, 200, 3)).astype(np.float32)

	def noise3x3(self, coord):
		lerp = lambda a, b, x: a + (b-a)*x

		mins = np.floor(coord).astype(np.int8)
		maxs = np.ceil(coord).astype(np.int8)
		ts = coord - mins
		ts = np.repeat(ts, 3).reshape(-1, 3, 3)

		mins += self.cube_bias
		maxs += self.cube_bias

		xyz = self.noise_cube[mins[:,0],mins[:,1],mins[:,2]]
		Xyz = self.noise_cube[maxs[:,0],mins[:,1],mins[:,2]]
		xYz = self.noise_cube[mins[:,0],maxs[:,1],mins[:,2]]
		XYz = self.noise_cube[maxs[:,0],maxs[:,1],mins[:,2]]
		xyZ = self.noise_cube[mins[:,0],mins[:,1],maxs[:,2]]
		XyZ = self.noise_cube[maxs[:,0],mins[:,1],maxs[:,2]]
		xYZ = self.noise_cube[mins[:,0],maxs[:,1],maxs[:,2]]
		XYZ = self.noise_cube[maxs[:,0],maxs[:,1],maxs[:,2]]

		lyz = lerp(xyz, Xyz, ts[:,0,:])
		lYz = lerp(xYz, XYz, ts[:,0,:])
		lyZ = lerp(xyZ, XyZ, ts[:,0,:])
		lYZ = lerp(xYZ, XYZ, ts[:,0,:])

		llz = lerp(lyz, lYz, ts[:,1,:])
		llZ = lerp(lyZ, lYZ, ts[:,1,:])

		lll = lerp(llz, llZ, ts[:,2,:])

		return lll
