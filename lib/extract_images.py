import cv2
import os
from settings import Settings


# gibt jedes Videoeinzelbild von video, sodass frame_dist dessen Frame-Zahl teilt, zurück
def get_images(video, frame_dist):
	images = []

	capture = cv2.VideoCapture(Settings.input_dir + "/" + video)
	frame = 0

	while True:
		capture.set(cv2.CV_CAP_PROP_POS_FRAMES, frame - 1)
		success, image = capture.read()
		if not success:
			return images

		cropped = image[Settings.y0 : Settings.y1, Settings.x0 : Settings.x1]
		
		images.append(cropped)
		
		frame += frame_dist