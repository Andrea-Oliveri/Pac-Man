from contextlib import contextmanager

import cv2

from .abstract_frame_generator import AbstractFrameGenerator


class Video(AbstractFrameGenerator):

    def __init__(self, video_path, **kwargs):
        self._video_path = video_path
        self._stream = None
        super().__init__(**kwargs)

    @contextmanager
    def _make_stream(self):
        if self._stream is not None:
            raise RuntimeError("context manager _make_stream is reusable but not reentrant.")

        self._stream = cv2.VideoCapture(self._video_path, cv2.CAP_FFMPEG)
        try:
            yield
        finally:
            self._stream.release()
            self._stream = None

    def _get_height_width(self):
        with self._get_stream_alive() as stream:
            height = int(stream.get(cv2.CAP_PROP_FRAME_HEIGHT))
            width = int(stream.get(cv2.CAP_PROP_FRAME_WIDTH))
        return height, width

    def _get_fps(self):
        with self._get_stream_alive() as stream:
           fps = float(stream.get(cv2.CAP_PROP_FPS))

        if fps == 0.0:
            raise RuntimeError("unable to detect frames per second of video.")

        return fps

    def _get_frames_count(self):
        with self._get_stream_alive() as stream:
            return int(stream.get(cv2.CAP_PROP_FRAME_COUNT))

    def _read_frame(self):
        return self._stream.read()

    def _grab_frame(self):
        return self._stream.grab()

    @contextmanager
    def _get_stream_alive(self):
        if self._stream is None:
            with self._make_stream():
                yield self._stream
        else:
            yield self._stream