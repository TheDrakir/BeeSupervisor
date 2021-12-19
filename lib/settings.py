from pathlib import Path

class Settings():
    # Name des Eingabevideos
    vin_name = "varroa2.mp4"

    # Ordner der neuornalen Netze
    network_path = Path("D:\\SemiABI\\SemiCode\\network-data")

    # Ordner der Eingabevideos
    input_path = Path("D:\\SemiABI\\SemiCode\\input_videos")

    # Ordner der Ausgabevideos
    output_path = Path("D:\\SemiABI\\SemiCode\\output_videos")

    # Startzeitpunkt der Videoanalyse in Sekunden
    start_time = 0
    # Endzeitpunkt der Videoanalyse in Sekunden
    end_time = 300

    # nach Bienen untersuchter Bildausschnitt
    x0 = 0
    x1 = 1920
    y0 = 500
    y1 = 800

    # Minimal Bewertung zur Bienenerkennenung
    bee_confidence_tresh = 0.8

    # Minimal Bewertung zur Milbenerkennenung
    vra_confidence_tresh = 0

    # Abstand der untersuchten Frames
    frame_dist = 2

    # maximale Bewegungsdistanz einer Biene zwischen zwei untersuchten Frames
    bee_dist_thresh = frame_dist * 40

    # maximale Distanz zwischen mehreren Bounding Boxes einer Biene
    # damit wird die mehrfache Erkennung einer Biene verhindert
    bee_duplicate_dist = 30
    
    # minimale 8-Bit-Helligkeit einer Varroa
    varroa_color_thresh = 180

    # Einstellungen zur Erstellung des editierten Videos
    alpha_overlay = 0.7
    healthy_color = (42, 219, 151)
    infected_color = (0,51,204)
    white = (255, 255, 255)

    # werden die Bounding Boxes der Bienen eingezeichnet?
    draw_rectangles = False
    # werden die Bounding Boxes der Bienen relativ zum Hintergrund erhellt?
    darken_background = False
    # werden irgendwelche Bildbearbeitungen im Ausgabevideo getätigt?
    # falls nicht, sinkt die Laufzeit dramatisch, weil das Video direkt extrahiert wird, ohne es zu de- und enkodieren
    draw_edits = draw_rectangles or darken_background
    # schreibe alle Videoclips, in denen Bienen sichtbar sind?
    write_bee_clips = True
    # schreibe alle Videoclips, in denen infizierte Bienen sichtbar sind?
    write_infected_clips = False