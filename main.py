from cv2 import displayOverlay
from pathlib import Path

from lib.settings import Settings
from lib.bee_detector import Bee_Detector
from lib.vra_detector import Vra_Detector
from lib.tracker import Tracker
from lib.timer import Timer
from lib.clip_video import clip_video

def main():
    t0 = Timer("absolute")
    t0.begin()
    vin_name = "varroa2.mp4"

    bee_detector = Bee_Detector("bee_detector.weights", "yolov4-tiny.cfg")
    vra_detector = Vra_Detector("vra_detector.weights", "yolov4-tiny.cfg")


    tracker = Tracker(Settings.input_path / vin_name, bee_detector, vra_detector)
    tracker.run(0, 300, Settings.frame_dist)

    clip_video(tracker)

    print(tracker.bee_counter)
    print(tracker.infected_counter)
    
    t0.end()
    print(t0)
    

if __name__ == "__main__":
    main()
    