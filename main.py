from pathlib import Path
from moviepy.editor import VideoFileClip


import lib.settings as se
from lib.output_writer import Output_Writer
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

    print(Path.cwd())

    se.init(Path.cwd() / "input" / "settings.json")

    # Objekt zur Bienenerkennung
    bee_detector = Bee_Detector("bee_detector.weights", "yolov4-tiny.cfg")

    # Objekt zur Milbenerkennung
    vra_detector = Vra_Detector("vra_detector.weights", "yolov4-tiny.cfg")

    # Objekt zum Zählen der Bienen in den Eingabevideos
    bee_counter = Counter("bees")

    # Objekt zum Zählen der infizierten Bienen in den Eingabevideos
    infected_counter = Counter("infected bees")

    seconds_counter = Counter("analyzed seconds")

    duration_counter = Counter("duration")

    for video in (se.VIN_PATH).iterdir():
        if video.suffix == ".mp4":
            clip = VideoFileClip(str(video))
            duration_counter.set(duration_counter.value + clip.duration)
    duration_counter.value = int(duration_counter.value + 1)

    # Objekt zum schreiben der Counter in die Ausgabedatei
    Output_Writer([bee_counter, infected_counter, seconds_counter, duration_counter])

    for object_type in ["bees", "infected", "whole"]:
        Video_Clipper.clear_dir(se.OUTPUT_PATH / object_type)

    for video in (se.VIN_PATH).iterdir():
        if video.suffix == ".mp4":
            print("analyzing: {:>30}\n...".format(video.name))
            # Objekt zur Verfolgung der Bienen und Untersuchung auf Varroainfektionen
            tracker = Tracker(video, bee_detector, vra_detector)

            # setze die sub-counters, die die jeweiligen Werte für tracker aufnehmen
            tracker.bee_counter = Counter("bees", bee_counter)
            tracker.infected_counter = Counter("infected bees", infected_counter)
            tracker.seconds_counter = Counter("analyzed seconds", seconds_counter)
            tracker.counters = [tracker.bee_counter, tracker.infected_counter, tracker.seconds_counter]

            # lasse tracker laufen
            tracker.run(se.FRAME_DIST)

    print(bee_counter)
    print(infected_counter)
    print(seconds_counter)
    
    t0.end()
    print(t0)
    

# falls main.py direkt ausgeführt wurde, rufe die Hauptfunktion auf
if __name__ == "__main__":
    main()