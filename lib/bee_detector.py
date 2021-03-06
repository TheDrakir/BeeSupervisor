import cv2

import lib.settings as se
from lib.bee import Bee


class Bee_Detector:
    '''Klasse zum Erkennen von Bienen'''

    # die Score-Grenze, ab der eine Bounding Box eine Biene ist
    confidence_thresh = .9

    def __init__(self, weights, config):
        # lade das yolov4-tiny Netzwerk
        self.network = cv2.dnn.readNet(str(se.NETWORK_PATH / weights), str(se.NETWORK_PATH / config))

        # definiere den Index der zu erkennenden Klassen des Netzwerks
        self.bee_ind = 0

        # Liste der Ausgabeschichten
        self.output_layers = self.network.getUnconnectedOutLayersNames()

    def get_bees(self, image):
        '''
        get_bees gibt die Bounding Boxes aller Bienen zurück.
        
        :param image: untersuchtes Bild
        '''
        # definiere die Höhe, Breite von image
        h, w, _ = image.shape

        # skaliere die Helligkeit auf das Intervall 0 <= x <= 1
        channel_scalar = 1 / 255
        channel_subtrahend = (0, 0, 0)
        # Dimensionen des Eingabebilds des neuronalen Netzes
        new_size = (256, 256)
        
        # ermittle aus dem blob über network den output, die Liste aller Bounding Boxes und der dazugehörigen Scores mit self.network
        blob = cv2.dnn.blobFromImage(image, channel_scalar, new_size, channel_subtrahend, swapRB=True, crop=False)
        self.network.setInput(blob)
        outputs = self.network.forward(self.output_layers)

        # erstelle bees, die Liste aller Bienen mit Scores über dem Threshhold
        bees = []
        for output in outputs:
            for detection in output:
                confidence = detection[5 + self.bee_ind]
                if confidence > Bee_Detector.confidence_thresh:
                    ctr = int(detection[0] * w), int(detection[1] * h)
                    dim = int(detection[2] * w), int(detection[3] * h)
                    
                    bees.append(Bee(ctr, dim))
        return bees
