import ctypes
import math
import time

import numpy as np
from OpenGL import GL

import gllib
import gllib.fsquad
import gllib.framebuffer
import gfx
import particles
import swarm

class Scene:
	def __init__(self, size):
		self.size = size

		self.elapsed = 0
		self.swarm = swarm.Swarm(swarm.Swarm.Params())
		self.last_update_time = time.monotonic()
		self.poses = np.zeros((1,self.swarm.params.size,3), dtype=np.float32)
		self.ages = np.zeros((1,self.swarm.params.size), dtype=np.float32)

		self.pprogram = particles.PProgram(
			gfx.perspectiveM(math.tau/8, self.size[0] / self.size[1], 0.1, 100),
			gfx.lookatM([5, 2, 5], [0, 0, 0], [0, 1, 0])
		)

		self.fbo = gllib.framebuffer.Framebuffer(size)
		self.fsquad = gllib.fsquad.FSQuad()

#		GL.glPointSize(1)
		GL.glClearColor(0., 0., 0., 1.)
		GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)

	def update(self):
		now = time.monotonic()
		dt = now - self.last_update_time
		self.elapsed += dt
		self.last_update_time = now

		self.swarm.update(dt)
		for n in range(self.poses.shape[0]-1,0,-1):
			self.poses[n] = self.poses[n-1]
			self.ages[n] = self.ages[n-1]
		self.poses[0] = self.swarm.particle_pos
		self.ages[0] = self.swarm.particle_age / self.swarm.particle_life

		self.pprogram.update_view_matrix(gfx.lookatM([5*math.sin(self.elapsed/5), 2, 5*math.cos(self.elapsed/5)], [0, 0, 0], [0, 1, 0]))
		self.pprogram.update_data(self.poses, self.ages)

	def render(self):
		with self.fbo:
			GL.glClearColor(0., 0., 0., 0.)
			GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)
			self.pprogram.render()

		GL.glDisable(GL.GL_DEPTH_TEST)
		GL.glEnable(GL.GL_BLEND)

		GL.glBlendColor(1, 1, 1, .95)
		GL.glBlendFunc(GL.GL_SRC_ALPHA, GL.GL_CONSTANT_ALPHA)

		with self.fbo.texture:
			self.fsquad.draw()

		GL.glDisable(GL.GL_BLEND)
		GL.glEnable(GL.GL_DEPTH_TEST)

	def shutdown(self):
		pass
