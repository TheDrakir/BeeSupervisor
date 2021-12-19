import cv2

from lib.settings import Settings
from lib.bee import Bee
from lib.timer import Timer


class Bee_Detector:
    def __init__(self, weights, config):

        # lade das yolov4-tiny Netzwerk
        self.network = cv2.dnn.readNet(str(Settings.network_path / weights), str(Settings.network_path / config))

        # definiere den Index der zu erkennenden Klassen des Netzwerks
        self.bee_ind = 0

        # die Namen der Schichten des Netzwerks
        layer_names = self.network.getLayerNames()

        # Liste der Ausgabeschichten
        self.output_layers = [layer_names[i[0] - 1] for i in self.network.getUnconnectedOutLayers()]


    def get_bees(self, image):
        # definiere die Höhe, Breite von image
        h, w, _ = image.shape

        # skaliere die Helligkeit auf das Intervall 0 <= x <= 1
        channel_scalar = 1 / 255
        channel_subtrahend = (0, 0, 0)
        # Dimensionen des Eingabebilds des neuronalen Netzes
        new_size = (256, 256)
        
        # ermittle output, die Liste aller Bounding Boxes und der dazugehörigen Scores mit self.network
        blob = cv2.dnn.blobFromImage(image, channel_scalar, new_size, channel_subtrahend, swapRB=True, crop=False)
        self.network.setInput(blob)
        outputs = self.network.forward(self.output_layers)

        # erstelle bees, die Liste aller Bienen mit Scores über dem Threshhold aus settings.py
        bees = []
        for output in outputs:
            for detection in output:
                confidence = detection[5 + self.bee_ind]
                if confidence > Settings.bee_confidence_tresh:
                    ctr = int(detection[0] * w), int(detection[1] * h)
                    dim = int(detection[2] * w), int(detection[3] * h)
                    
                    bees.append(Bee(ctr, dim))
        return bees
