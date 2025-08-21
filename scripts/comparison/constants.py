import pathlib

_ASSETS_FOLDER = pathlib.Path(__file__).parent / "assets"

VIDEOS_PATHS = list((_ASSETS_FOLDER / "videos").glob("*.mp4"))

_TEMPLATES_FOLDER = _ASSETS_FOLDER / "templates"
TEMPLATE_LEVEL_START_PATH = _TEMPLATES_FOLDER / "level_start.png"
TEMPLATE_LEVEL_END_PATH = _TEMPLATES_FOLDER / "level_end.png"


PARALLEL_MAX_WORKERS = 12


LEVEL_SEARCH_FRAMES_STEP = 20