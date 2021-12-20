import lib.settings as se

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
        return Pos(self.x + se.X0_ANALYSIS, self.y + se.Y0_ANALYSIS)