from lib.settings import Settings
from lib.bee_detector import Bee_Detector
from lib.vra_detector import Vra_Detector
from lib.tracker import Tracker
from lib.timer import Timer
from lib.video_clipper import Video_Clipper

def main():
    '''die Hauptfunktion, über die das gesamte Programm ausgeführt wird'''

    # t0 ist ein Timer für die gesamte main()-Funktion
    t0 = Timer("absolute")
    t0.begin()

    # Objekt zur Bienenerkennung
    bee_detector = Bee_Detector("bee_detector.weights")

    # Objekt zur Milbenerkennung
    vra_detector = Vra_Detector("hii.weights")

    # Objekt zur Verfolgung der Bienen und Untersuchung auf Varroainfektionen
    tracker = Tracker(Settings.input_path / Settings.vin_name, bee_detector, vra_detector)

    # lasse tracker laufen
    tracker.run(Settings.start_frame, Settings.end_frame, Settings.frame_dist)

    print(tracker.bee_counter)
    print(tracker.infected_counter)
    
    t0.end()
    print(t0)
    

# falls main.py direkt ausgeführt wurde, rufe die Hauptfunktion auf
if __name__ == "__main__":
    main()