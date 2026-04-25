from contextlib import contextmanager

import cv2
from tqdm import tqdm


class Video:

    def __init__(self, video_path, frames_start = 0, frames_step = 1, frames_number = None, viewport = None, progress_bar = False):
        self._video_path = video_path
        self._frames_start = frames_start
        self._frames_step = frames_step
        self._frames_number = frames_number
        self._viewport = viewport
        self._progress_bar = progress_bar
        self._height, self._width = self._get_height_width()

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

    def _get_height_width(self):
        for frame in self:
            return frame.shape[0], frame.shape[1]

    @property
    def height(self):
        return self._height

    @property
    def width(self):
        return self._width
