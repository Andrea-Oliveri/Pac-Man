import pathlib
from dataclasses import dataclass


@dataclass(slots = True, frozen = True)
class Position:
    row: int
    col: int

    def __add__(self, other):
        if not isinstance(other, Position):
            raise ValueError(f"argument 'other' must be of type Position. Got {type(other)}")
        return Position(row = self.row + other.row, col = self.col + other.col)
    

@dataclass(slots = True, frozen = True)
class MatchResults:
    pos: Position
    score: float


@dataclass(slots = True, frozen = True)
class Region:
    start: Position
    stop: Position
    height = property(lambda self: self.stop.row - self.start.row)
    width  = property(lambda self: self.stop.col - self.start.col)

    def __init__(self, start, stop = None, height = None, width = None):
        if not isinstance(start, Position):
            raise ValueError(f"argument 'start' must be of type Position. Got {type(start)}")
        if stop is None:
            if not isinstance(height, int) or not isinstance(width, int):
                raise ValueError(f"when argument 'stop' is not provided, both 'width' and 'height' must be provided and must be integers. Got {type(width)} and {type(height)} respectively.")
            stop = Position(row = start.row + height, col = start.col + width)
        else:
            if height is not None or width is not None:
                raise ValueError(f"when argument 'stop' is provided, both 'width' and 'height' must not be provided")
        
        if start.row > stop.row or start.col > stop.col:
            raise ValueError(f"start must have row and col <= to stop. Got start: {start} and stop {stop}")

        object.__setattr__(self, "start", start)
        object.__setattr__(self, "stop" , stop)





_ASSETS_FOLDER = pathlib.Path(__file__).parent / "assets"

VIDEOS_PATHS = list((_ASSETS_FOLDER / "videos").glob("*.mp4"))

_TEMPLATES_FOLDER = _ASSETS_FOLDER / "templates"
TEMPLATE_LEVEL_START_PATH = _TEMPLATES_FOLDER / "level_start.png"
TEMPLATE_LEVEL_END_PATH = _TEMPLATES_FOLDER / "level_end.png"
TEMPLATE_PACMAN_PATH = _TEMPLATES_FOLDER / "pacman.png"

PARALLEL_MAX_WORKERS = 12

LEVEL_START_END_DETECTION_THR = 50

TEMPLATE_PACMAN_LABEL_PER_ROW = ["RIGHT", "LEFT", "UP", "DOWN", "FULL_CIRCLE", "DEATH"]
TEMPLATE_PACMAN_ELEMENT_WIDTH = 16
TEMPLATE_PACMAN_ELEMENT_HEIGHT = 16
