from lib.settings import Settings
from lib.bee_detector import Bee_Detector
from lib.vra_detector import Vra_Detector
from lib.tracker import Tracker
from lib.timer import Timer
from lib.counter import Counter
from lib.video_clipper import Video_Clipper

def main():
    '''die Hauptfunktion, über die das gesamte Programm ausgeführt wird'''

    # t0 ist ein Timer für die gesamte main()-Funktion
    t0 = Timer("absolute")
    t0.begin()

    # Objekt zur Bienenerkennung
    bee_detector = Bee_Detector("bee_detector.weights", "yolov4-tiny.cfg")

    # Objekt zur Milbenerkennung
    vra_detector = Vra_Detector("custom-yolov4-tiny-detector_best.weights", "yolov4-tiny.cfg")

    bee_counter = Counter("bees")
    infected_counter = Counter("infected bees")

    for object_type in ["bees", "infected", "whole"]:
        Video_Clipper.clear_dir(Settings.output_path / object_type)

    for video in (Settings.vin_path).iterdir():
        if video.suffix == ".mp4":
            print(video)
            # Objekt zur Verfolgung der Bienen und Untersuchung auf Varroainfektionen
            tracker = Tracker(video, bee_detector, vra_detector)

            # lasse tracker laufen
            tracker.run(Settings.start_frame, Settings.end_frame, Settings.frame_dist)

            bee_counter.sub_counter(tracker.bee_counter)
            infected_counter.sub_counter(tracker.infected_counter)

    print(bee_counter)
    print(infected_counter)
    
    t0.end()
    print(t0)
    

# falls main.py direkt ausgeführt wurde, rufe die Hauptfunktion auf
if __name__ == "__main__":
    main()