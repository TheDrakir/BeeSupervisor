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

    # gibt die Frame-Intervalle zurück, die alle Frames aus frames enthalten
    # Lücken der Länge < merge_dist werden zu den Intervallen hinzugefügt
    @staticmethod
    def get_video_intervals(frames):
        merge_dist = 10
        intervals = []
        i = 0
        while i < len(frames):
            for j in range(i, len(frames)):
                if j + 1 == len(frames) or frames[j+1] > frames[j] + merge_dist:
                    break
            intervals.append((frames[i], frames[j] + merge_dist))
            i = j + 1
        return intervals