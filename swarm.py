import numpy as np

import npnoise

class Swarm:
	class Params:
		def __init__(self):
			self.size = 10000
			self.life_mean = 5
			self.life_variance = 2
			self.dampening = .01
			self.field_strength = 5

	def __init__(self, params):
		self.params = params

		self.noise = npnoise.NPNoise()
		self.noiseX = npnoise.NPNoise()
		self.noiseY = npnoise.NPNoise()
		self.noiseZ = npnoise.NPNoise()

		self.original_pos = np.concatenate((
			((np.arange(self.params.size, dtype=np.float32) - (self.params.size/2)) / (self.params.size/2)).reshape((self.params.size, 1)),
			np.zeros((self.params.size, 2), dtype=np.float32)
		), axis=1)
		self.life_func = lambda: self.params.life_mean + self.params.life_variance * np.random.randn(self.params.size)
		self.vel_func = lambda pos: np.random.randn(*pos.shape) * .1

		self.original_pos = np.random.rand(self.params.size, 3).astype(np.float32) * 2 - 1 #################################
#		self.original_pos = np.zeros((self.params.size, 3)).astype(np.float32)#######################################33
		self.particle_pos = np.copy(self.original_pos)
#		self.particle_vel = np.zeros((self.params.size, 3), dtype=np.float32)
		self.particle_vel = np.copy(self.vel_func(self.original_pos))
		self.particle_age = np.zeros((self.params.size,), dtype=np.float32)
		self.particle_life = np.zeros((self.params.size,), dtype=np.float32)
		self.particle_color = np.zeros((self.params.size, 3), dtype=np.float32)

	def update(self, dt):
		field_val = self.field(self.particle_pos * 2)
		self.particle_color = (field_val / 2) + .5
		dv = field_val * self.params.field_strength
		dp = (self.particle_vel + dv/2) * dt

		self.particle_vel += (-self.particle_vel * self.params.dampening) + dv * dt
		self.particle_pos += dp
		self.particle_age += dt

		dead_particles = self.particle_age >= self.particle_life
		self._rebirth(dead_particles)

	def _rebirth(self, dead_particles):
		self.particle_pos[dead_particles] = np.copy(self.original_pos)[dead_particles]
		self.particle_vel[dead_particles] = np.copy(self.vel_func(self.original_pos))[dead_particles]
		self.particle_life[dead_particles] = self.life_func()[dead_particles]
		self.particle_age[dead_particles] = 0

	def field(self, coord):
#		theta = self.noiseX.noise3(coord) * np.pi
#		phi = self.noiseY.noise3(coord) * 2*np.pi
#		r = self.noiseZ.noise3(coord)
#		return np.stack((r*np.sin(theta)*np.cos(phi), r*np.sin(theta)*np.sin(phi), r*np.cos(theta)), axis=-1)
#		return np.stack((self.noiseX.noise3(coord), self.noiseY.noise3(coord), self.noiseZ.noise3(coord)), axis=-1) * 2. - 1.
#		return np.repeat(self.noiseX.noise3(coord), 3).reshape(-1, 3)
		return self.noise.noise3x3(coord) * 2. - 1.
