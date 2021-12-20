import cv2
import numpy as np
import pathlib

from lib.settings import Settings
from lib.video_tools import Video_Tools

class Editor:
    '''Klasse zum editieren von Bildern'''
    
    def __init__(self, tracker):
        self.tracker = tracker

    def get_edited(self):
        '''
       gibt ein editiertes Bild für das Ausgabevideo auf Basis der Einstellungen aus settings.py zurück
        
        :param image: das zu editierende Bild
        :param bees: die Bienen im zu editierenden Bild
        '''
        edited = self.tracker.image.copy()
        if Settings.darken_background:
            mask = np.full(self.tracker.image.shape[:2] + (1,), 0.25, np.float)
        for bee in self.tracker.bees:
            if bee.infected:
                cv2.imwrite(str(Settings.output_path / "images" / "{}-{}.jpg".format(self.tracker.vin_path.stem, self.tracker.frame)), Editor.get_cropped_bee(self.tracker.image, bee))
            if Settings.draw_rectangles:
                cv2.rectangle(edited, tuple(bee.pos0.decropped()), tuple(bee.pos1.decropped()), Editor.get_color(bee), 2)
                cv2.putText(edited, str(bee.id), tuple(bee.pos0.decropped()), cv2.FONT_HERSHEY_SIMPLEX, 1, Editor.get_color(bee), 2, 2)
                if bee.infected:
                    cv2.rectangle(edited, tuple((bee.pos0 + bee.vra.pos0).decropped()), tuple((bee.pos0 + bee.vra.pos1).decropped()), Editor.get_color(bee), 2)
            if Settings.darken_background:
                cv2.rectangle(mask, tuple(bee.pos0.decropped()), tuple(bee.pos1.decropped()), 1, -1)
                cv2.rectangle(mask, tuple(bee.pos0.decropped()), tuple(bee.pos1.decropped()), 1, 2)
        if Settings.darken_background:
            edited = (edited * mask).astype(np.uint8)
        if Settings.draw_rectangles:
            cv2.line(edited, (Settings.x0, Settings.y0), (Settings.x1, Settings.y0), Settings.healthy_color, 5)
            cv2.line(edited, (Settings.x0, Settings.y1), (Settings.x1, Settings.y1), Settings.healthy_color, 5)
        return edited

    # gibt die Farbe der Biene bee im editierten Bild zurück
    @staticmethod
    def get_color(bee):
        if bee.infected:
            return Settings.infected_color
        else:
            return Settings.healthy_color

    # gibt den Bildausschnitt der Biene bee zurück
    @staticmethod
    def get_cropped_bee(image, bee):
        return image[Settings.y0 : , Settings.x0 : ][bee.pos0.y : bee.pos1.y, bee.pos0.x : bee.pos1.x]

import random
import string
def rand_name(chars = string.ascii_lowercase, N=8):
    return ''.join(random.choice(chars) for _ in range(N)) + ".jpg"