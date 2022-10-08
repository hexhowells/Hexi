import cv2
import numpy as np


class Floor:
	def __init__(self, threshold=20, img_step=10, img_size=(640, 480), rescale_factor=5, smoothing_samples=5):
		self.threshold = threshold
		self.step = img_step

		self.img_size = img_size
		self.width = self.img_size[0]
		self.height = self.img_size[1]

		self.new_img_size = tuple([x // rescale_factor for x in self.img_size])

		self.smoothing_samples = smoothing_samples


	def downsample(self, img):
		out = cv2.resize(img, self.new_img_size, interpolation=cv2.INTER_AREA)
		out = cv2.resize(out, self.img_size, interpolation=cv2.INTER_NEAREST)

		return out


	def segment_floor(self, img):
		coords = self._get_segment_columns(img)

		for _ in range(self.smoothing_samples):
			coords = self._smooth_coords(coords)

		return coords


	def _get_segment_columns(self, img):
		coords = []


		for col in range(0, self.width, self.step):
			prev = img[-1][col]  # reset prev
			floor_found = False

			for row in range(self.height-1, 0, -5):
				pixel = img[row][col]

				if self._diff(pixel, prev) > self.threshold:
					coords.append([(col, row+1), (col+self.step, self.height)])
					floor_found = True
					break
				prev = pixel

			if not floor_found:
				coords.append([(col, self.height), (col+self.step, self.height)])

		return coords


	def _diff(self, rgb1, rgb2, debug=False):
		a = np.array(rgb1, dtype=np.int16)
		b = np.array(rgb2, dtype=np.int16)

		return sum(abs(a - b)) // 3


	def _smooth_coords(self, coords):
		heights = [a[1] for a, b in coords]
		heights = [heights[2]] + heights + [heights[-2]]
		
		for i in range(1, (len(heights) - 1)):
			avg_h = sum([heights[i-1], heights[i], heights[i+1]]) // 3

			new_c = list(coords[i-1][0])
			new_c[1] = avg_h
			coords[i-1][0] = tuple(new_c)
			

		return coords
