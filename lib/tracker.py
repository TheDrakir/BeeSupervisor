import cv2

from lib.settings import Settings
from lib.editor import Editor
from lib.timer import Timer
from lib.counter import Counter


class Tracker:
    def __init__(self, vin_path, bee_detector, vra_detector, vout_path=None):
        self.vin_path = vin_path
        if vout_path is None:
            self.write = False
        else:
            self.vout_path = vout_path
            self.write = True

        # setze den genutzten Bee_Detector
        self.bee_detector = bee_detector
        # setze den genutzten Vra_Detector
        self.vra_detector = vra_detector

        # Bienen im vorherigen Videoeinzelbild
        self.prev_bees = []
        # Bienen im aktuellen Videoeinzelbild
        self.bees = []


        # Videoeinzelbildzahlen, zu denen eine Biene erkannt wird
        self.bee_frames = []
        # Videoeinzelbildzahlen, zu denen eine Varroamilbe erkannt wird
        self.vra_frames = []

        # Zähler der bisher erkannten Bienen
        self.bee_counter = Counter("bees")
        # Zähler der bisher erkannten infizierten Bienen
        self.infected_counter = Counter("infected bees")
        
        self.set_vin()

    # setze das Eingabevideo
    def set_vin(self):
        self.vin = cv2.VideoCapture(str(self.vin_path))
        self.height = int(self.vin.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.width = int(self.vin.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.frame_rate = self.vin.get(cv2.CAP_PROP_FPS) 
 
    # setze das Ausgabevideo
    def set_vout(self, frame0):
        self.vout = cv2.VideoWriter()
        self.dim = (self.width, self.height)
        self.fps = self.vin.get(cv2.CAP_PROP_FPS)
        self.fourcc = cv2.VideoWriter_fourcc(*'mp4v')

    # laufe den Tracker über das Video in der Frame-range (frame0, frame1, frame_dist)
    def run(self, frame0, frame1, frame_dist):
        if self.write:
            self.set_vout(frame0)
            self.vout.open(str(self.vout_path), self.fourcc, self.fps, self.dim, True)
        
        
        self.frame = frame0
        self.vin.set(cv2.CAP_PROP_POS_FRAMES, self.frame - 1)

        while self.frame < frame1:
            for _ in range(frame_dist - 1):
                self.vin.read()
            success, image = self.vin.read()
            if not success:
                break
            self.track_image(image)
            self.frame += frame_dist
        if self.write:
            self.vout.release()

    # tracke die Bienen im aktuellen Videoeinzelbild bezüglich des vorherigen
    def track_image(self, image):
        self.prev_bees = self.bees
        self.bees = []


        self.cropped = image[Settings.y0 : Settings.y1, Settings.x0 : Settings.x1]
        self.detected_bees = self.bee_detector.get_bees(self.cropped)

        for bee in self.prev_bees:
            bee.prev_ctr = None
        for detected_bee in self.detected_bees:
            self.add_bee(detected_bee)
        for bee in self.bees:
           self.set_infected(bee)
        if self.bees:
            self.bee_frames.append(self.frame)
        if self.write:
            edited = Editor.get_edited(image, self.frame, self.bees)
            self.vout.write(edited)

    # füge eine Biene zu self.bees hinzu
    # tracke sie zum vorherigen Videoeinzelbild, falls sie dort schon sichtbar war
    def add_bee(self, new_bee):
        closest_dist = Settings.bee_dist_thresh
        closest_bee = new_bee

        for prev_bee in self.prev_bees:
            if prev_bee.prev_ctr is None:
                dist = prev_bee.dist(new_bee)
                if dist < closest_dist:
                    closest_dist = dist
                    closest_bee = prev_bee

        for bee in self.bees:
            if bee.dist(new_bee) <= Settings.bee_duplicate_dist:
                return

        closest_bee.track(new_bee)
        if closest_dist == Settings.bee_dist_thresh:
            closest_bee.id = self.bee_counter.value
            self.bee_counter.increment()
        self.bees.append(closest_bee)

    # setze den Infektionsstatus der Biene bee auf True
    def set_infected(self, bee):
        if bee.infected:
            return
        cropped_bee = self.cropped[bee.pos0[1] : bee.pos1[1], bee.pos0[0] : bee.pos1[0]]
        if self.vra_detector.contains_vra(cropped_bee):
            bee.infect()
            self.vra_frames.append(self.frame)
            self.infected_counter.increment()

    # schreibe ein geschnittenes Video der Frame-range (frame0, frame1) nach vout_path
    def write_cutted(self, frame0, frame1, vout_path):
        write_tracker = Tracker(self.vin_path, self.bee_detector, self.vra_detector, vout_path)
        write_tracker.run(frame0, frame1, 1)