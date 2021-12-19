import cv2
import numpy as np
import pathlib

from lib.settings import Settings
from lib.video_tools import Video_Tools

class Editor:
    
    # gibt das editierte Bild zum Eingabebild zurück
    # Bildzahl im Video: frame, Bienen: bees
    @staticmethod
    def get_edited(image, frame, bees):
        edited = image.copy()
        if Settings.darken_background:
            mask = np.full(image.shape[:2] + (1,), 0.25, np.float)
        for bee in bees:
            if Settings.draw_rectangles:
                cv2.rectangle(edited, Editor.decrop_pos(bee.pos0), Editor.decrop_pos(bee.pos1), Editor.get_color(bee), 2)
            if Settings.darken_background:
                cv2.rectangle(mask, Editor.decrop_pos(bee.pos0), Editor.decrop_pos(bee.pos1), 1, -1)
                cv2.rectangle(mask, Editor.decrop_pos(bee.pos0), Editor.decrop_pos(bee.pos1), 1, 2)
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
        return image[Settings.y0 : , Settings.x0 : ][bee.pos0[1] : bee.pos1[1], bee.pos0[0] : bee.pos1[0]]
        
    # konvertiert Koordinaten im untersuchten Bildausschnitt zu Koordinaten im Gesamtbild
    @staticmethod
    def decrop_pos(pos):
        return int(pos[0] + Settings.x0), int(pos[1] + Settings.y0)
