import cv2

import lib.settings as se
from lib.animal import Animal


class Vra_Detector:
    '''Klasse zur Untersuchung von Bienen auf eine Varroa-Infektion'''

    confidence_thresh = .8

    def __init__(self, weights, config):

        # lade das yolov4-tiny Netzwerk
        self.network = cv2.dnn.readNet(str(se.NETWORK_PATH / weights), str(se.NETWORK_PATH / config))

        # definiere den Index der zu erkennenden Klassen des Netzwerks
        self.vra_ind = 0

        # die Namen der Schichten des Netzwerks
        layer_names = self.network.getLayerNames()

        # List der Ausgabeschichten
        self.output_layers = [layer_names[i[0] - 1] for i in self.network.getUnconnectedOutLayers()]


    def get_vra(self, image):
        cv2.waitKey(0)
        h, w, _ = image.shape

        # Milbenerkennung
        channel_scalar = 1 / 255
        new_size = (416, 416)
        channel_subtrahend = (0, 0, 0)
        
        blob = cv2.dnn.blobFromImage(image, channel_scalar, new_size, channel_subtrahend, swapRB=True, crop=False)

        self.network.setInput(blob)
        outputs = self.network.forward(self.output_layers)

        for output in outputs:
            for detection in output:
                confidence = detection[5 + self.vra_ind]
                if confidence > Vra_Detector.confidence_thresh:
                    ctr = int(detection[0] * w), int(detection[1] * h)
                    dim = int(detection[2] * w), int(detection[3] * h)
                    return Animal(ctr, dim)
        return None
