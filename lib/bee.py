from typing import Set
from lib.settings import Settings
from lib.animal import Animal


class Bee(Animal):
    '''Klasse zum Erstellen eines Bienen-Objekts'''
    def __init__(self, ctr, dim):
        super().__init__(ctr, dim)

        # self.prev_ctr ist der Mittelpunkt der Biene im letzten Frame
        self.prev_ctr = None

        # self.infected ist der Infektionsstatus der Biene mit der Varroamilbe
        self.infected = False

    # gibt die Distanz der Biene zu other zurück
    def dist(self, other):
        return ((self.ctr[0] - other.ctr[0])**2 + (self.ctr[1] - other.ctr[1])**2)**0.5

    def track(self, other):
        '''
        verfolgt die Biene zu einer anderen Biene im nächsten Videoeinzelbild
        
        :param other: andere Biene
        '''
        self.prev_ctr = self.ctr
        self.ctr = other.ctr
        self.dim = other.dim
        self.set_corners()

    # setze den Infektionsstatus auf wahr
    def infect(self, vra):
        self.infected = True
        self.vra = vra