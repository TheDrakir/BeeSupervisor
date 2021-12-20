from lib.settings import Settings

class Pos:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __iter__(self):
        yield self.x
        yield self.y

    def __add__(self, other):
        return Pos(self.x + other.x, self.y + other.y)

    # konvertiert Koordinaten im untersuchten Bildausschnitt zu Koordinaten im Gesamtbild
    def decropped(self):
        return Pos(self.x + Settings.x0, self.y + Settings.y0)