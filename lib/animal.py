from lib.settings import Settings
from lib.pos import Pos

class Animal:
    '''Klasse zum Erstellen eines Tier-Objekts'''

    def __init__(self, ctr, dim):
        # self.ctr ist der Mittelpunkt der Bounding Box der Biene
        self.ctr = ctr
        # self.dim ist das Tupel von (Höhe, Breite) der Biene
        self.dim = dim

        self.set_corners()

    # setze die Ecken der Bounding Box des Tiers
    def set_corners(self):
        pos0 = tuple(self.ctr[i] - self.dim[i] // 2 for i in range(2))
        pos1 = tuple(self.ctr[i] + self.dim[i] // 2 for i in range(2))
        self.pos0 = Pos(max(0, pos0[0]), max(0, pos0[1]))
        self.pos1 = Pos(min(Settings.x1, pos1[0]), min(Settings.y1, pos1[1]))

        