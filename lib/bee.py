from typing import Set
from lib.settings import Settings


class Bee:
    def __init__(self, ctr, dim):
        # self.ctr ist der Mittelpunkt der Bounding Box der Biene
        self.ctr = ctr
        # self.dim ist das Tupel von (Höhe, Breite) der Biene
        self.dim = dim
        
        # self.prev_ctr ist der Mittelpunkt der Biene im letzten Frame
        self.prev_ctr = None

        # self.infected ist der Infektionsstatus der Biene mit der Varroamilbe
        self.infected = False

    # setze die Ecken der Bounding Box der Biene
    def set_corners(self):
        pos0 = tuple(self.ctr[i] - self.dim[i] // 2 for i in range(2))
        pos1 = tuple(self.ctr[i] + self.dim[i] // 2 for i in range(2))
        self.pos0 = max(0, pos0[0]), max(0, pos0[1])
        self.pos1 = min(Settings.x1, pos1[0]), min(Settings.y1, pos1[1])

    # gibt die Distanz der Biene zu other zurück
    def dist(self, other):
        return ((self.ctr[0] - other.ctr[0])**2 + (self.ctr[1] - other.ctr[1])**2)**0.5

    # erbe die Eigenschaften von other in den nächsten Frame
    def track(self, other):
        self.prev_ctr = self.ctr
        self.ctr = other.ctr
        self.dim = other.dim
        self.set_corners()

    # setze den Infektionsstatus auf wahr
    def infect(self):
        self.infected = True