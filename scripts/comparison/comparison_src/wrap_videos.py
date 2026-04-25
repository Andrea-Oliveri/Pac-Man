from contextlib import contextmanager

import cv2
from tqdm import tqdm

from .constants import Region, Position


class Video:

    def __init__(self, video_path, frames_start = 0, frames_step = 1, frames_number = None, viewport = None, progress_bar = False):
        self._video_path = video_path
        self._frames_start = frames_start
        self._frames_step = frames_step
        self._frames_number = frames_number
        self._progress_bar = progress_bar
        self._viewport = None
        self._set_viewport(viewport)

    def __iter__(self):
        with self._make_video_capture() as stream:
            n_frames_video = int(stream.get(cv2.CAP_PROP_FRAME_COUNT))

            frames_end = n_frames_video if self._frames_number is None else min(n_frames_video, self._frames_start + self._frames_step * self._frames_number)
            frames_to_yield = range(self._frames_start, frames_end, self._frames_step)

            current_frame = -1

            with tqdm(total = len(frames_to_yield), ascii = True, leave = False, disable = not self._progress_bar) as pbar:
                while True:
                    current_frame += 1

                    if current_frame in frames_to_yield:
                        grabbed, frame = stream.read()
                    else:
                        grabbed = stream.grab()

                    if not grabbed:
                        break
                    elif current_frame >= frames_end:
                        break
                    elif current_frame not in frames_to_yield:
                        continue

                    pbar.update()
                    if self._viewport is not None:
                        frame = frame[self._viewport.start.row:self._viewport.stop.row, self._viewport.start.col:self._viewport.stop.col]
                    yield frame

    def get_fps(self):
        with self._make_video_capture() as stream:
            fps = float(stream.get(cv2.CAP_PROP_FPS))

        if fps == 0.0:
            raise RuntimeError("unable to detect frames per second of video.")

        return fps

    @contextmanager
    def _make_video_capture(self):
        stream = cv2.VideoCapture(self._video_path, cv2.CAP_FFMPEG)
        try:
            yield stream
        finally:
            stream.release()

    def _set_viewport(self, viewport):
        if viewport is None:
            self._viewport = None
            return

        if not isinstance(viewport, Region):
            raise TypeError(f"viewport argument must be of type Region. Got {type(viewport)} instead.")
        with self._make_video_capture() as stream:
            video_height = int(stream.get(cv2.CAP_PROP_FRAME_HEIGHT))
            video_width = int(stream.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_region = Region(start = Position(row = 0, col = 0), height = video_height, width = video_width)
        if viewport not in frame_region:
            raise RuntimeError(f"viewport falls outside of frame: viewport={viewport} and frame={frame_region}")
        self._viewport = viewport


    viewport = property(lambda self: self._viewport, _set_viewport)
