import numpy as np
import cv2



def img_filter(x):
	return 1 * (x > 25)


def new_object(img1, img2):
	diff = cv2.absdiff(img1, img2)
	diff = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
	diff = img_filter(diff)

	score = np.average(diff)
	window_score = np.average(diff[200:,80:-80])
	score_distribution = abs(score - window_score)

	if 0.05 < score < 0.4 and score_distribution > 0.1:
		return True
	else:
		return False

