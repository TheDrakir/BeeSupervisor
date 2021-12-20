import cv2

from lib.settings import Settings
from lib.editor import Editor
from lib.timer import Timer
from lib.counter import Counter
from lib.video_clipper import Video_Clipper


class Tracker:
    '''Klasse zur Verfolgung und Untersuchung von Bienen in einem Video'''

    # maximale Bewegungsdistanz einer Biene zwischen zwei untersuchten Frames
    bee_dist_thresh = Settings.frame_dist * 40

    # maximale Distanz zwischen mehreren Bounding Boxes einer Biene
    # damit wird die mehrfache Erkennung einer Biene verhindert
    bee_duplicate_dist = 30

    def __init__(self, vin_path, bee_detector, vra_detector):
        self.vin_path = vin_path

        # setze den genutzten Bee_Detector
        self.bee_detector = bee_detector
        # setze den genutzten Vra_Detector
        self.vra_detector = vra_detector

        # Bienen im vorherigen Videoeinzelbild
        self.prev_bees = []
        # Bienen im aktuellen Videoeinzelbild
        self.bees = []
        # infizierte Bienen im aktuellen Videoeinzelbild
        self.infected_bees = []

        # Zähler der bisher erkannten Bienen
        self.bee_counter = Counter("bees")
        # Zähler der bisher erkannten infizierten Bienen
        self.infected_counter = Counter("infected bees")
        
        self.set_vin()

        self.vc_bees = Video_Clipper(self, "bees", apply=Settings.write_bee_clips)
        self.vc_infected = Video_Clipper(self, "infected", apply=Settings.write_infected_clips)
        self.vc_whole = Video_Clipper(self, "whole", apply=Settings.write_whole, active=True)
        self.vc_whole.active = True

        self.vcs = [self.vc_bees, self.vc_infected, self.vc_whole]

    # setze das Eingabevideo
    def set_vin(self):
        self.vin = cv2.VideoCapture(str(self.vin_path))
        self.height = int(self.vin.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.width = int(self.vin.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.fps = self.vin.get(cv2.CAP_PROP_FPS)
 
    

    def run(self, frame0, frame1, frame_dist):
        '''
        lässt den Tracker über die Videoeinzelbilder des Videos laufen

        :param frame0: Startbildnummer
        :param frame1: Endbildnummer
        :param frame_dist: Abstand aufeinanderfolgender, untersuchter Einzelbilder
        '''
    
        self.frame = frame0
        self.vin.set(cv2.CAP_PROP_POS_FRAMES, self.frame - 1)

        while self.frame < frame1:
            for _ in range(frame_dist - 1):
                self.vin.read()
            success, self.image = self.vin.read()
            if not success:
                break
            self.track_image()
            self.frame += frame_dist
        
        for vc in self.vcs:
            if vc.writing:
                vc.release()

    def track_image(self):
        '''
        erkenne alle Bienen aus dem Bild, tracke sie zu Bienen aus dem vorherigen Bild, untersuche alle Bienen im Bild auf eine Infektion
        '''
        self.prev_bees = self.bees
        self.bees = []


        self.cropped = self.image[Settings.y0 : Settings.y1, Settings.x0 : Settings.x1]
        self.detected_bees = self.bee_detector.get_bees(self.cropped)

        for bee in self.prev_bees:
            bee.prev_ctr = None
        for detected_bee in self.detected_bees:
            self.add_bee(detected_bee)
        self.infected_bees = []
        for bee in self.bees:
           self.set_infected(bee)

        self.vc_bees.active = bool(self.bees)
        self.vc_infected.active = bool(self.infected_bees)

        for vc in self.vcs:
            vc.update()

    # füge eine Biene zu self.bees hinzu
    # tracke sie zum vorherigen Videoeinzelbild, falls sie dort schon sichtbar war
    def add_bee(self, new_bee):
        '''
        füge eine Biene zu der Liste der Bienen im aktuellen Videoeinzelbild hinzu und tracke sie ggf. zum vorherigen Bild
        
        :param new_bee: hinzugefügte Biene
        '''
        closest_dist = Tracker.bee_dist_thresh
        closest_bee = new_bee

        for prev_bee in self.prev_bees:
            if prev_bee.prev_ctr is None:
                dist = prev_bee.dist(new_bee)
                if dist < closest_dist:
                    closest_dist = dist
                    closest_bee = prev_bee

        for bee in self.bees:
            if bee.dist(new_bee) <= Tracker.bee_duplicate_dist:
                return

        closest_bee.track(new_bee)
        if closest_dist == Tracker.bee_dist_thresh:
            closest_bee.id = self.bee_counter.value
            self.bee_counter.increment()
        self.bees.append(closest_bee)

    # setze den Infektionsstatus der Biene bee
    def set_infected(self, bee):
        cropped_bee = self.cropped[bee.pos0.y : bee.pos1.y, bee.pos0.x : bee.pos1.x]
        vra = self.vra_detector.get_vra(cropped_bee)
        if vra is not None:
            if not bee.infected:
                self.infected_counter.increment()
            bee.infect(vra)
        if bee.infected:
            self.infected_bees.append(bee)