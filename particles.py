from OpenGL import GL

import gllib

VERTEX_SHADER = """\
#version 310 es

uniform mat4 u_view;
uniform mat4 u_projection;

in vec3 position;
in float age;

out float vf_age;

void main() {
	gl_Position = u_projection * u_view * vec4(position, 1);
	vf_age = age;
}

"""
FRAGMENT_SHADER = """\
#version 310 es

in highp float vf_age;

out highp vec4 fragColor;

void main() {
	fragColor = vec4(1., vf_age, 0., 1.);
}
"""

class PProgram:
	def __init__(self, projection_matrix, view_matrix):
		self.program = gllib.shader.VertexFragmentProgram(VERTEX_SHADER, FRAGMENT_SHADER)
		self.vao = gllib.vao.VAO()
		self.pos = gllib.vbo.VBO(GL.GL_ARRAY_BUFFER, GL.GL_DYNAMIC_DRAW)
		self.age = gllib.vbo.VBO(GL.GL_ARRAY_BUFFER, GL.GL_DYNAMIC_DRAW)
		self.particle_count = 0

		with self.program:
			GL.glUniformMatrix4fv(self.program.get_uniform_location('u_projection'), 1, GL.GL_TRUE, projection_matrix)
		self.update_view_matrix(view_matrix)

		with self.vao as va:
			with self.pos as vb:
				va.set_vertex_attrib(vb, 0, 3, GL.GL_FLOAT)
			with self.age as vb:
				va.set_vertex_attrib(vb, 1, 1, GL.GL_FLOAT)

	def update_view_matrix(self, view_matrix):
		with self.program:
			GL.glUniformMatrix4fv(self.program.get_uniform_location('u_view'), 1, GL.GL_TRUE, view_matrix)

	def update_data(self, pos, age):
		pos_reshape = pos.reshape(-1, 3)
		self.particle_count = pos_reshape.shape[0]

		with self.pos as vb:
			vb.set_data(pos_reshape)

		with self.age as vb:
			vb.set_data(age.reshape(-1, 1))

	def render(self):
		with self.program:
			with self.vao:
				GL.glDrawArrays(GL.GL_POINTS, 0, self.particle_count)
