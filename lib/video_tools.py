class Video_Tools:
    '''Klasse zum konvertieren zwischen Video-Zeiteinheiten'''

    def __init__(self, fps):
        self.fps = fps

    # gibt den Zeitstempel zu frame im Video mit Pfad video_path zurück
    def get_time_stamp(self, frame):
        seconds = self.get_seconds(frame)
        minutes = seconds // 60
        hours = minutes // 60
        out = "{}_{}".format(Video_Tools.str_of_length(minutes % 60, 2), Video_Tools.str_of_length(seconds % 60, 2))
        if hours > 0:
            out = "{}_{}".format(Video_Tools.str_of_length(hours % 24, 2), out)
        return out

    # gibt die Sekunde zu frame im Video mit Pfad video_path zurück
    def get_seconds(self, frame):
        return frame / self.fps

    # gibt die frame-Zahl zu seconds im Video mit Pfad video_path zurück
    def get_frames(self, seconds):
        return seconds * self.fps

    # gibt die Ganzzahl n als String der Länge l mit eventuell führenden Nullen zurück
    @staticmethod
    def str_of_length( n, l):
        out = str(int(n))
        while len(out) < l:
            out = "0" + out
        return out