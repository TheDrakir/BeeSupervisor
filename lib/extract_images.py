import cv2
import lib.settings as se


def get_images(video, frame_dist):
	'''
	gibt jedes k-te Videoeinzelbild zurück
	
	:param video: Video der Bilder
	:param frame-dist: Abstand zwischen zwei zurückgegebenen Bildern
	'''
	images = []

	capture = cv2.VideoCapture(se.INPUT_DIR + "/" + video)
	frame = 0

	while True:
		capture.set(cv2.CV_CAP_PROP_POS_FRAMES, frame - 1)
		success, image = capture.read()
		if not success:
			return images

		cropped = image[se.Y0_ANALYSIS : se.Y1_ANALYSIS, se.X0_ANALYSIS : se.X1_ANALYSIS]
		
		images.append(cropped)
		
		frame += frame_dist