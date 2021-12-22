import cv2

import lib.settings as se
from lib.editor import Editor
from lib.timer import Timer
from lib.counter import Counter
from lib.video_clipper import Video_Clipper


class Tracker:
    '''Klasse zur Verfolgung und Untersuchung von Bienen in einem Video'''

    def __init__(self, vin_path, bee_detector, vra_detector, laser = None):
        self.vin_path = vin_path

        # setze den genutzten Bee_Detector
        self.bee_detector = bee_detector
        # setze den genutzten Vra_Detector
        self.vra_detector = vra_detector

        # setze den angesteuerten Laser
        self.laser = laser

        # maximale Bewegungsdistanz einer Biene zwischen zwei untersuchten Frames
        bee_dist_thresh = se.FRAME_DIST * 40

        # maximale Distanz zwischen mehreren Bounding Boxes einer Biene
        # damit wird die mehrfache Erkennung einer Biene verhindert
        bee_duplicate_dist = 30

        # Bienen im vorherigen Videoeinzelbild
        self.prev_bees = []
        # Bienen im aktuellen Videoeinzelbild
        self.bees = []
        # infizierte Bienen im aktuellen Videoeinzelbild
        self.infected_bees = []
        
        self.set_vin()

        self.vc_bees = Video_Clipper(self, "bees", apply=se.WRITE_BEE_CLIPS)
        self.vc_infected = Video_Clipper(self, "infected", apply=se.WRITE_INFECTED_CLIPS)
        self.vc_whole = Video_Clipper(self, "whole", apply=se.WRITE_WHOLE, active=True)
        self.vc_whole.active = True

        self.vcs = [self.vc_bees, self.vc_infected, self.vc_whole]

    # setze das Eingabevideo
    def set_vin(self):
        self.vin = cv2.VideoCapture(str(self.vin_path))
        self.height = int(self.vin.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.width = int(self.vin.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.fps = self.vin.get(cv2.CAP_PROP_FPS)
 
    
    def run(self, frame_dist):
        '''
        lässt den Tracker über die Videoeinzelbilder des Videos laufen

        :param frame_dist: Abstand aufeinanderfolgender, untersuchter Einzelbilder
        '''
    
        self.frame = 0
        self.vin.set(cv2.CAP_PROP_POS_FRAMES, self.frame - 1)

        while True:
            for _ in range(frame_dist - 1):
                self.vin.read()
            success, self.image = self.vin.read()
            if not success:
                break
            self.track_image()
            self.frame += frame_dist
            self.seconds_counter.set(int(self.frame // self.fps))
        
        for vc in self.vcs:
            if vc.writing:
                vc.release()

    def track_image(self):
        '''
        erkenne alle Bienen aus dem Bild, tracke sie zu Bienen aus dem vorherigen Bild, untersuche alle Bienen im Bild auf eine Infektion
        '''
        self.prev_bees = self.bees
        self.bees = []


        self.cropped = self.image[se.Y0_ANALYSIS : se.Y1_ANALYSIS, se.X0_ANALYSIS : se.X1_ANALYSIS]
        # ermittle die Bienen im Bild
        self.detected_bees = self.bee_detector.get_bees(self.cropped)

        for bee in self.prev_bees:
            bee.prev_ctr = None
        # füge die Bienen im Bild dem Tracker hinzu
        for detected_bee in self.detected_bees:
            self.add_bee(detected_bee)
        # teste alle Bienen des Trackers auf eine Varroainfektion
        self.infected_bees = []
        for bee in self.bees:
           self.set_infected(bee)

        self.vc_bees.active = bool(self.bees)
        self.vc_infected.active = bool(self.infected_bees)
        if se.CONTROL_LASER and self.infected_bees:
            bee = self.infected_bees[0]
            self.laser.pointAt(se.X0_ANALYSIS + bee.pos0.x + bee.vra.ctr[0], se.y0_ANALYSIS + bee.pos0.y + bee.vra.ctr[1])

        # update alle video_clippers
        for vc in self.vcs:
            vc.update()

        # Bienenclips werden nach 15s abgebrochen
        # daher entstehen auch für sehr dichte Eingabeivideos kurze Bienenclips
        if self.vc_bees.writing:
            if self.vc_bees.start_frame <= self.frame - 15 * self.fps:
                self.vc_bees.release()

    # füge eine Biene zu self.bees hinzu
    # tracke sie zum vorherigen Videoeinzelbild, falls sie dort schon sichtbar war
    def add_bee(self, new_bee):
        '''
        füge eine Biene zu der Liste der Bienen im aktuellen Videoeinzelbild hinzu und tracke sie ggf. zum vorherigen Bild
        
        :param new_bee: hinzugefügte Biene
        '''
        closest_dist = se.MOVEMENT_THRESH * se.FRAME_DIST
        closest_bee = new_bee

        # finde die nächste Biene, falls diese näher als die Minimaldistanz ist
        for prev_bee in self.prev_bees:
            if prev_bee.prev_ctr is None:
                dist = prev_bee.dist(new_bee)
                if dist < closest_dist:
                    closest_dist = dist
                    closest_bee = prev_bee

        # lösche Mehrfacherkennungen einer Biene
        for bee in self.bees:
            if bee.dist(new_bee) <= se.DUPLICATE_THRESH:
                return

        # tracke die nächste Biene von den letzten Frame auf die aktuelle Position
        closest_bee.track(new_bee)
        if closest_dist == se.MOVEMENT_THRESH * se.FRAME_DIST:
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