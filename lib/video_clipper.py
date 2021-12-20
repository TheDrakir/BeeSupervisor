from pathlib import Path
from typing import Set

from lib.settings import Settings
from lib.video_tools import Video_Tools

class Video_Clipper:
    '''Klasse zum Erstellen von Video-Clips'''

    def __init__(self, tracker):
        self.tracker = tracker
        self.vt = Video_Tools(tracker.fps)

    # erstelle alle Clips, die durch den tracker generiert wurden
    def clip(self):
        if Settings.write_bee_clips:
            bee_intervals = Video_Tools.get_video_intervals(self.tracker.bee_frames)
            self.write_videos(bee_intervals, "bees")
        
        if Settings.write_infected_clips:
            infected_intervals = Video_Tools.get_video_intervals(self.tracker.infected_frames)
            self.write_videos(infected_intervals, "infected")

    def clear(self):
        for object_type in ["bees", "infected", "whole"]:
            Video_Clipper.clear_dir(object_type)


    # schreibt die Videos aus den intervals in das Verzeichnis des object-type
    def write_videos(self, intervals, object_type):
        out_path = Settings.output_path / object_type
        for interval in intervals:
            frame0, frame1 = interval
            clip_path = out_path / "clip_from-{}.mp4".format(self.vt.get_time_stamp(frame0))
            if Settings.draw_edits:
                self.tracker.write_cutted(frame0, frame1, clip_path)
            else:
                second0 = frame0 / self.tracker.fps
                second1 = frame1 / self.tracker.fps
                from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
                ffmpeg_extract_subclip(str(self.tracker.vin_path), second0, second1, targetname=str(clip_path))

    # löscht ein Verzeichnis und seine Inhalte, falls es existiert
    @staticmethod
    def rm_tree(p):
        if p.is_dir():
            for child in p.iterdir():
                if child.is_file():
                    child.unlink()
                else:
                    Video_Clipper.rm_tree(child)
            p.rmdir()

    # erstellt ein leeres output-Verzeichnis für den object_type
    @staticmethod
    def clear_dir(object_type):
        out_path = Settings.output_path / object_type
        Video_Clipper.rm_tree(out_path)
        out_path.mkdir(parents=True, exist_ok=True)