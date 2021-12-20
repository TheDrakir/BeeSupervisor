from pathlib import Path
from typing import Set

from lib.settings import Settings
from lib.video_tools import Video_Tools
from lib.editor import Editor

import cv2

class Video_Clipper:
    '''Klasse zum Erstellen von Video-Clips'''

    merge_dist = 10

    def __init__(self, tracker, object_type, apply=True, active=False):
        self.tracker = tracker
        self.path = Settings.output_path / object_type
        self.apply = apply
        self.active = active

        self.editor = Editor(tracker)

        self.writing = False
        self.start_frame = 0
        self.last_active_frame = 0
        self.vt = Video_Tools(tracker.fps)

    def update(self):
        '''Wird '''
        if self.apply:
            if self.active:
                self.last_active_frame = self.tracker.frame
                if not self.writing:
                    self.open()
            if self.writing:
                if self.tracker.frame < self.last_active_frame + Video_Clipper.merge_dist:
                    self.write_frame()
                else:
                    self.release()

    # öffnet das Ausgabevideo
    def open(self):
        self.start_frame = self.last_active_frame
        self.vout_path = self.path / "{}-{}.mp4".format(self.tracker.vin_path.stem, self.vt.get_time_stamp(self.last_active_frame))
        if Settings.draw_edits:
            self.vout = cv2.VideoWriter()
            fps = self.tracker.fps / Settings.frame_dist
            dim = self.tracker.width, self.tracker.height
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            self.vout.open(str(self.vout_path), fourcc, fps, dim, True)
        self.writing = True

    # schreibt das nächste Videoeinzelbild in das Ausgabevideo
    def write_frame(self):
        if Settings.draw_edits:
            edited = self.editor.get_edited()
            self.vout.write(edited)

    # schreibt das Ausgabevideo in den Zielordner
    def release(self):
        if Settings.draw_edits:
            self.vout.release()
        else:
            from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
            second0 = self.start_frame / self.tracker.fps
            second1 = self.tracker.frame / self.tracker.fps
            ffmpeg_extract_subclip(str(self.tracker.vin_path), second0, second1, targetname=str(self.vout_path))
        self.writing = False

    # erstellt ein leeres output-Verzeichnis für den object_type
    @staticmethod
    def clear_dir(p):
        Video_Clipper.rm_tree(p)
        p.mkdir(parents=True, exist_ok=True)

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