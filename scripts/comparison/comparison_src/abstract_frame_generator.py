import abc

from tqdm import tqdm

from .constants import Region, Position


class AbstractFrameGenerator(abc.ABC):

    def __init__(self, frames_start = 0, frames_step = 1, frames_number = None, viewport = None, progress_bar = False):
        self._frame_to_grab = _FramesToGrab(frames_start, frames_step, frames_number, self._get_frames_count())
        self._progress_bar = progress_bar
        self._viewport = None
        self._set_viewport(viewport)


    def __iter__(self):
        with self._make_stream():
            current_frame = -1

            with tqdm(total = self._frame_to_grab.len(), ascii = True, leave = False, disable = not self._progress_bar) as pbar:
                while True:
                    current_frame += 1
                    to_grab = current_frame in self._frame_to_grab

                    if to_grab:
                        grabbed, frame = self._read_frame()
                    else:
                        grabbed = self._grab_frame()

                    if not grabbed:
                        break
                    elif self._frame_to_grab.after_last(current_frame):
                        break
                    elif not to_grab:
                        continue

                    pbar.update()
                    if self._viewport is not None:
                        frame = frame[self._viewport.start.row:self._viewport.stop.row, self._viewport.start.col:self._viewport.stop.col]
                    yield frame

    def _set_viewport(self, viewport):
        height, width = self._get_height_width()
        frame_region = Region(start = Position(row = 0, col = 0), height = height, width = width)

        if viewport is None:
            self._viewport = frame_region
            return
        if not isinstance(viewport, Region):
            raise TypeError(f"viewport argument must be of type Region. Got {type(viewport)} instead.")
        if viewport not in frame_region:
            raise RuntimeError(f"viewport falls outside of frame: viewport={viewport} and frame={frame_region}")
        self._viewport = viewport

    @abc.abstractmethod
    def _get_height_width(self):
        raise NotImplementedError

    @abc.abstractmethod
    def _get_fps(self):
        raise NotImplementedError

    @abc.abstractmethod
    def _get_frames_count(self):
        raise NotImplementedError

    @abc.abstractmethod
    def _read_frame(self):
        raise NotImplementedError

    @abc.abstractmethod
    def _grab_frame(self):
        raise NotImplementedError

    viewport = property(lambda self: self._viewport, _set_viewport)


class _FramesToGrab:
    def __init__(self, start, step, number, end):
        if not isinstance(start, int) or start < 0:
            raise ValueError("parameter 'start' must be a non-negative integer.")
        if not isinstance(step, int) or step <= 0:
            raise ValueError("parameter 'step' must be a strictly positive integer.")
        if number is not None and (not isinstance(number, int) or number < 0):
            raise ValueError("parameter 'frames_number' must be a non-negative integer.")
        if end is not None and (not isinstance(end, int) or end < 0):
            raise ValueError("parameter 'end' must be a non-negative integer.")

        self._start = start
        self._step = step
        self._end, self._number = self._calculate_last_and_len(start, step, number, end)

    @staticmethod
    def _calculate_last_and_len(start, step, number, end):

        # Unbounded sequence.
        if number is None and end is None:
            return None, None

        # Empty sequence.
        if number == 0:
            return None, 0

        # End before start.
        if end is not None and end < start:
            return None, 0

        # Normal path from now on.
        max_count = (
            None if end is None else
            (end - start) // step + 1
        )

        count = (
            max_count if number is None else
            number if max_count is None else
            min(number, max_count)
        )

        return (
            start + (count - 1) * step,
            count,
        )

    def len(self):
        return self._number

    def after_last(self, n):
        if not isinstance(n, int) or n < 0:
            raise ValueError("parameter 'n' must be a non-negative integer.")

        return self._end is None or n > self._end

    def __contains__(self, n):
        if not isinstance(n, int) or n < 0:
            raise ValueError("parameter 'n' must be a non-negative integer.")

        if self._number == 0 or n < self._start or self.after_last(n):
            return False

        return (n - self._start) % self._step == 0