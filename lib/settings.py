from pathlib import Path
import json

def init(input_settings_path):
    with open(input_settings_path) as f:
        data = json.load(f)

    global INPUT_SETTINGS_PATH , OUTPUT_FILE_PATH , WIDTH_FOR_DRAWING_ROI
    global CWD, NETWORK_PATH, INPUT_PATH, VIN_PATH, OUTPUT_PATH, LIB_PATH
    global MOVEMENT_THRESH, DUPLICATE_THRESH
    global CONTROL_LASER
    global X0_ANALYSIS, X1_ANALYSIS, Y0_ANALYSIS, Y1_ANALYSIS
    global FRAME_DIST
    global HEALTHY_COLOR, INFECTED_COLOR
    global DRAW_RECTANGLES, DARKEN_BACKGROUND, DRAW_EDITS
    global WRITE_BEE_CLIPS, WRITE_INFECTED_CLIPS, WRITE_WHOLE

    # Pfad der json-Datei zur Eingabe
    INPUT_SETTINGS_PATH = input_settings_path

    # die Bildweite des Fensters, in dem man die Region-Of-Interest definiert
    WIDTH_FOR_DRAWING_ROI = data["width_for_drawing_roi"]

    # Path der main.py Datei, über die settings.py aufgerufen wird
    CWD = Path.cwd()

    # Ordner der neuornalen Netze
    NETWORK_PATH = CWD / data["network_dir"]

    # Ordner der Eingabedateien
    INPUT_PATH = CWD / data["input_dir"]

    # Ordner der Ausgabedateien
    OUTPUT_PATH = CWD / data["output_dir"]

    # lib-Ordner
    LIB_PATH = CWD / data["lib_dir"]

    # Ordner der Eingabevideos
    VIN_PATH = INPUT_PATH / data["vin_dir"]

    # Pfad der json-Datei zur Ausgabe
    OUTPUT_FILE_PATH = OUTPUT_PATH / data["output_file"]

    # maximale zurückgelegte Distanz einer Biene pro Frame
    MOVEMENT_THRESH = data["movement_thresh"]

    # minimaler Abstand zwischen zwei verschiedenen Bienen
    DUPLICATE_THRESH = data["duplicate_thresh"]

    # wird ein Laser angesteuert?
    CONTROL_LASER = data["control_laser"]

    # nach Bienen untersuchter Bildausschnitt
    X0_ANALYSIS = data["x0"]
    X1_ANALYSIS = data["x1"]
    Y0_ANALYSIS = data["y0"]
    Y1_ANALYSIS = data["y1"]

    # Abstand der untersuchten Frames
    FRAME_DIST = data["frame_dist"]

    # Einstellungen zur Erstellung des editierten Videos
    HEALTHY_COLOR = tuple(data["healthy_color"])
    INFECTED_COLOR = tuple(data["infected_color"])

    # werden die Bounding Boxes der Bienen eingezeichnet?
    DRAW_RECTANGLES = data["draw_rectangles"]
    # werden die Bounding Boxes der Bienen relativ zum Hintergrund erhellt?
    DARKEN_BACKGROUND = data["darken_background"]
    # werden irgendwelche Bildbearbeitungen im Ausgabevideo getätigt?
    # falls nicht, sinkt die Laufzeit dramatisch, weil das Video direkt extrahiert wird, ohne es zu de- und enkodieren
    DRAW_EDITS = DRAW_RECTANGLES or DARKEN_BACKGROUND


    # schreibe alle Videoclips, in denen Bienen sichtbar sind?
    WRITE_BEE_CLIPS = data["write_bee_clips"]
    # schreibe alle Videoclips, in denen infizierte Bienen sichtbar sind?
    WRITE_INFECTED_CLIPS = data["write_infected_clips"]
    # schreibe das gesamte editierte Video
    WRITE_WHOLE = data["write_whole"]