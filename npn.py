import numpy as np
#import opensimplex
import PIL.Image

import npnoise

def gen2(shape):
	npn = npnoise.NPNoise()

	xys = np.mgrid[0:shape[0], 0:shape[1]].reshape(2, shape[1], -1).T.astype(np.float32)
	xys = xys / 512
	zs = np.zeros((shape[0],shape[1],1), dtype=np.float32)
	coords = np.concatenate((xys, zs), axis=2).reshape(shape[0], shape[1], 3)

	pix = npn.noise3((coords * 15).reshape(-1,3)).reshape(shape[0], shape[1])
	PIL.Image.fromarray((pix * 255).astype(np.uint8)).save("/tmp/sn2.png")

#	pix = npn.noise3x3((coords * 15).reshape(-1,3)).reshape(shape[0], shape[1], 3)
#	PIL.Image.fromarray((pix[...,0] * 255).astype(np.uint8)).save("/tmp/sn2-1.png")
#	PIL.Image.fromarray((pix[...,1] * 255).astype(np.uint8)).save("/tmp/sn2-2.png")
#	PIL.Image.fromarray((pix[...,2] * 255).astype(np.uint8)).save("/tmp/sn2-3.png")

def gen1(shape):
	sn = opensimplex.OpenSimplex()
	pix = np.zeros(shape, dtype=np.float32)
	for y in range(shape[1]):
		yy = y / shape[1]
		for x in range(shape[0]):
			xx = x / shape[0]
			pix[y][x] = sn.noise2d(xx * 10., yy * 10.)

	PIL.Image.fromarray((-128 + (pix * 127)).astype(np.uint8)).save("/tmp/sn1.png")

def main():
#	gen1((512,512))
	gen2((512,512))

if __name__ == '__main__':
	main()
