import json
from os import stat
from pathlib import Path
import cv2
import numpy as np

import lib.settings as se

class ROI_Setter:
    def __init__(self, vin_path):
        self.vin_path = vin_path
        self.file_path = se.INPUT_SETTINGS_PATH

    def set_roi(self):
        with open(self.file_path) as f:
            self.data = json.load(f)
        vin = cv2.VideoCapture(str(self.vin_path))
        _, self.image = vin.read()


        self.h, self.w, _ = self.image.shape
        self.r = se.WIDTH_FOR_DRAWING_ROI / self.w

        # skaliere das Bild auf die Breite aus settings.py
        self.resized = cv2.resize(self.image, (se.WIDTH_FOR_DRAWING_ROI, int(self.r * self.h)))
        self.edited0 = self.resized.copy()
        self.edited1 = self.edited0.copy()
        self.is_drawing = False
        self.ix = -1
        self.iy = -1

        # definiere das Fenster mit Callback zu self.update
        win_name = "Draw the region of interest!"
        cv2.namedWindow(win_name)
        cv2.setMouseCallback(win_name, self.update)
        # öffne das Fenster bis zur Schließung durch den Nutzer mit der ESC-Taste
        while True:
            cv2.imshow(win_name, self.edited1)
            if cv2.waitKey(5) & 0xFF == 27:
                break
        cv2.destroyAllWindows() 

    # beende das zeichnen des Rechtecks und speichere seine Werte in der Ausgabedatei
    def stop_drawing(self, x, y):
        self.is_drawing = False
        mask = np.full(self.edited0.shape[:2] + (1,), 0.25, np.float)
        cv2.rectangle(mask, (self.ix, self.iy), (x, y), 1, -1)
        cv2.rectangle(mask, (self.ix, self.iy), (x, y), 1, 2)

        self.edited0 = (self.edited0 * mask).astype(np.uint8)

        self.data["x0"] = max(int(min(x, self.ix) / self.r), 0)
        self.data["x1"] = min(int(max(x, self.ix) / self.r), self.w)
        self.data["y0"] = max(int(min(y, self.iy) / self.r), 0)
        self.data["y1"] = min(int(max(y, self.iy) / self.r), self.h)
        with open(self.file_path, "w") as f:
            json.dump(self.data, f, indent=4, sort_keys=True)

        cv2.rectangle(self.edited0, (self.ix, self.iy), (x, y), se.HEALTHY_COLOR, 2)
        self.ix = -1
        self.iy = -1

    def update(self, event, x, y, flags, param):
        self.edited1 = self.edited0.copy()
        if event == cv2.EVENT_LBUTTONDOWN:
            self.edited0 = self.resized.copy()
            self.is_drawing = True
            self.ix = x
            self.iy = y
        elif event == cv2.EVENT_LBUTTONUP:
            if self.is_drawing:
                self.stop_drawing(x, y)
        elif event == cv2.EVENT_MOUSEMOVE:
            if self.is_drawing:
                if 0 <= x < self.w * self.r and 0 <= y < self.h * self.r:
                    cv2.rectangle(self.edited1, (self.ix, self.iy), (x, y), se.HEALTHY_COLOR, 2)
                else:
                    self.stop_drawing(x, y)


def main():
    se.init(Path.cwd() / "input" / "settings.json")

    rs = ROI_Setter(list((se.VIN_PATH).iterdir())[0])
    
    rs.set_roi()

if __name__ == "__main__":
    main()