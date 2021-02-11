import ctypes
import math
import re
import time

import numpy as np
from OpenGL import GL
from OpenGL import GLES3

import gfx
import gllib
import particles_cs as particles

class Scene:
	def __init__(self, size):
		self.size = size
		self.particles = 50000

		self.program = gllib.shader.Program()

		with open('swarm.comp', 'r') as f:
			src = f.read()

		while True:
			res = re.search(r'#!include "([^"]+)"\n', src)
			if res is None:
				break
			with open(res.group(1), 'r') as f:
				included_src = f.read()
			src = src[:res.span()[0]] + included_src + src[res.span()[1]:]

			self.program.add_shader(GL.GL_COMPUTE_SHADER, src)
		self.program.link()

		self.pprogram = particles.PProgram(
			gfx.perspectiveM(math.tau/8, self.size[0] / self.size[1], 0.1, 100),
			gfx.lookatM([5, 2, 5], [0, 0, 0], [0, 1, 0])
		)

		self.original = gllib.vbo.VBO(GL.GL_SHADER_STORAGE_BUFFER, GL.GL_STATIC_DRAW)
		self.swarm = gllib.vbo.VBO(GL.GL_SHADER_STORAGE_BUFFER, GL.GL_DYNAMIC_COPY)

		self.fbo = gllib.framebuffer.Framebuffer(size)
		self.fsquad = gllib.fsquad.FSQuad()

		with self.original as vb:
			vb.set_data(np.zeros((self.particles, 2, 4), dtype=np.float32))
			vb.bind_base(1)

		with self.swarm as vb:
			vb.set_data(np.zeros((self.particles, 2, 4), dtype=np.float32))
			vb.bind_base(2)

		GL.glClearColor(0., 0., 0., 1.)
		GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)

		self.elapsed = 0
		self.last_update_time = time.monotonic()

	def update(self):
		now = time.monotonic()
		dt = now - self.last_update_time
		self.elapsed += dt
		self.last_update_time = now

		with self.program:
			GL.glUniform1f(self.program.get_uniform_location('dt'), dt)
			GLES3.glDispatchCompute(self.particles, 1, 1)
		GLES3.glMemoryBarrier(GL.GL_SHADER_STORAGE_BARRIER_BIT | GL.GL_VERTEX_ATTRIB_ARRAY_BARRIER_BIT)

		self.pprogram.particle_count = self.particles

		with self.swarm.bind_as(GL.GL_ARRAY_BUFFER) as vb:
			with self.pprogram.vao as va:
				va.set_vertex_attrib(vb, 0, 3, GL.GL_FLOAT, 32, 0)
				va.set_vertex_attrib(vb, 1, 1, GL.GL_FLOAT, 32, 28)

		self.pprogram.update_view_matrix(gfx.lookatM([5*math.sin(self.elapsed/5), 2, 5*math.cos(self.elapsed/5)], [0, 0, 0], [0, 1, 0]))

	def render(self):
		"""
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
		"""
		GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)
		self.pprogram.render()

	def shutdown(self):
		pass

def get_ssb_array(shape):
#	mapped_ptr = GL.glMapBuffer(GL.GL_SHADER_STORAGE_BUFFER, GL.GL_READ_ONLY)
	mapped_ptr = GL.glMapBufferRange(GL.GL_SHADER_STORAGE_BUFFER, 0, shape[0]*shape[1]*shape[2]*4, GL.GL_MAP_READ_BIT)
	mapped_fptr = ctypes.cast(mapped_ptr, ctypes.POINTER(ctypes.c_float))
	arr = np.ctypeslib.as_array(mapped_fptr, shape=shape)
#	arr = [mapped_fptr[i] for i in range(10)]
	GL.glUnmapBuffer(GL.GL_SHADER_STORAGE_BUFFER)
	return arr
