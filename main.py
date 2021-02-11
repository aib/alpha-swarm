import time
import logging

from OpenGL import GL
import sdl2

import scene
#import scene_cs as scene
import gllib.framebuffer

TITLE = "ComputeSH"
FPS_PRINT_TIME = 1

def main():
	########################
	class Opts(object): pass
	opts = Opts()
	opts.verbose = True
	opts.windowed = True
	opts.vsync = False
	########################

	if opts.verbose:
		logging.basicConfig(level=logging.DEBUG)
	else:
		logging.basicConfig(level=logging.INFO)

	logger = logging.getLogger(__name__)

	logger.info("Initializing")
	sdl2.SDL_Init(sdl2.SDL_INIT_VIDEO)

	dm = sdl2.SDL_DisplayMode()
	sdl2.SDL_GetDesktopDisplayMode(0, dm)
	if not opts.windowed:
		width = dm.w
		height = dm.h
	else:
		width = round(dm.w * .8)
		height = round(dm.h * .8)


	sdl2.SDL_GL_SetAttribute(sdl2.SDL_GL_CONTEXT_PROFILE_MASK, sdl2.SDL_GL_CONTEXT_PROFILE_ES);
	sdl2.SDL_GL_SetAttribute(sdl2.SDL_GL_CONTEXT_MAJOR_VERSION, 3)
	sdl2.SDL_GL_SetAttribute(sdl2.SDL_GL_CONTEXT_MINOR_VERSION, 0)

	window_flags = sdl2.SDL_WINDOW_OPENGL | (sdl2.SDL_WINDOW_FULLSCREEN if not opts.windowed else 0)
	window = sdl2.SDL_CreateWindow(TITLE.encode('utf-8'), sdl2.SDL_WINDOWPOS_UNDEFINED, sdl2.SDL_WINDOWPOS_UNDEFINED, width, height, window_flags)
	context = sdl2.SDL_GL_CreateContext(window)

	fbo = None
#	fbo = gllib.framebuffer.MultisampledFramebuffer(8, (width, height))

	if opts.vsync:
		if sdl2.SDL_GL_SetSwapInterval(-1) == -1:
			logger.warning("Adaptive vsync not available")
			sdl2.SDL_GL_SetSwapInterval(1)
	else:
		sdl2.SDL_GL_SetSwapInterval(0)

	main_scene = scene.Scene((width, height))

	frames = 0
	frame_count_time = time.monotonic()

	ev = sdl2.SDL_Event()
	running = True
	while running:
		while True:
			if (sdl2.SDL_PollEvent(ev) == 0):
				break
			if ev.type == sdl2.SDL_QUIT:
				running = False
			elif ev.type == sdl2.SDL_KEYUP and ev.key.keysym.sym == sdl2.SDLK_ESCAPE:
				running = False

		main_scene.update()

		if fbo is not None:
			with fbo:
				main_scene.render()
			fbo.activate_for_read()
			fbo.blit()
		else:
			main_scene.render()

		sdl2.SDL_GL_SwapWindow(window)

		frames += 1
		now = time.monotonic()
		if now - frame_count_time > FPS_PRINT_TIME:
			fps = frames / (now - frame_count_time)
			frames = 0
			frame_count_time = now
			logger.debug("%.3f FPS", fps)

	main_scene.shutdown()

	sdl2.SDL_GL_DeleteContext(context)
	sdl2.SDL_DestroyWindow(window)
	sdl2.SDL_Quit()

if __name__ == '__main__':
	main()
