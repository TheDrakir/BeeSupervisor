from lib.settings import Settings
from lib.video_tools import Video_Tools

def clip_video(tracker):
    if Settings.write_bee_clips:
        bee_intervals = Video_Tools.get_video_intervals(tracker.bee_frames)
        write_videos(tracker, bee_intervals, "bees")
    if Settings.write_infected_clips:
        infected_intervals = Video_Tools.get_video_intervals(tracker.infected_frames)
        write_videos(tracker, infected_intervals, "infected")

def write_videos(tracker, intervals, object_name):
    for i, interval in enumerate(intervals):
        frame0, frame1 = interval
        if Settings.draw_edits:
            tracker.write_cutted(frame0, frame1, Settings.output_path / "{}{}.mp4".format(object_name, i))
        else:
            second0 = frame0 / 30
            second1 = frame1 / 30
            from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
            ffmpeg_extract_subclip(str(tracker.vin_path), second0, second1, targetname=str(Settings.output_path / "{}{}.mp4".format(object_name, i)))
