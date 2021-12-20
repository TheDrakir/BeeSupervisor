from pathlib import Path

class Settings():
    '''Klasse zum speichern und abrufen aller Nutzereingaben'''

    # Name des Eingabevideos
    vin_name = Path("varroa2.mp4")

    # Path der main.py Datei, über die settings.py aufgerufen wird
    cwd = Path.cwd()

    # Ordner der neuornalen Netze
    network_path = cwd / "network-data"

    # Ordner der Eingabedateien
    input_path = cwd / "input"

    # Ordner der Eingabevideos
    vin_path = input_path / "videos"

    # Ordner der Ausgabedateien
    output_path = cwd / "output"

    # Startzeitpunkt der Videoanalyse in Frames
    start_frame = 0
    # Endzeitpunkt der Videoanalyse in Frames
    end_frame = float("inf")

    # nach Bienen untersuchter Bildausschnitt
    x0 = 0
    x1 = 1920
    y0 = 500
    y1 = 800

    # Abstand der untersuchten Frames
    frame_dist = 2

    # Einstellungen zur Erstellung des editierten Videos
    alpha_overlay = 0.7
    healthy_color = (42, 219, 151)
    infected_color = (0,51,204)
    white = (255, 255, 255)

    # werden die Bounding Boxes der Bienen eingezeichnet?
    draw_rectangles = True
    # werden die Bounding Boxes der Bienen relativ zum Hintergrund erhellt?
    darken_background = False
    # werden irgendwelche Bildbearbeitungen im Ausgabevideo getätigt?
    # falls nicht, sinkt die Laufzeit dramatisch, weil das Video direkt extrahiert wird, ohne es zu de- und enkodieren
    draw_edits = draw_rectangles or darken_background


    # schreibe alle Videoclips, in denen Bienen sichtbar sind?
    write_bee_clips = False
    # schreibe alle Videoclips, in denen infizierte Bienen sichtbar sind?
    write_infected_clips = False
    # schreibe das gesamte editierte Video
    write_whole = True