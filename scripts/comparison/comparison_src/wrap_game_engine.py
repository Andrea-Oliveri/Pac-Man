# -----------------------------------------------------------------
# Import standard library and installed packages.
# -----------------------------------------------------------------
import inspect
from copy import deepcopy as _deepcopy
from contextlib import contextmanager

import pyglet
pyglet.options.shadow_window = False  # See explaination in pacman.py at repo root.

import numpy as np
import cv2

from .abstract_frame_generator import AbstractFrameGenerator

# -----------------------------------------------------------------

# -----------------------------------------------------------------
# Import game objects.
# -----------------------------------------------------------------
import os
import sys

_GAME_ROOT_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), '../../..'))
sys.path.insert(0, _GAME_ROOT_DIR)

from src.constants import GAME_ORIGINAL_FPS, BACKGROUND_COLOR, LAYOUT_N_COLS_TILES, LAYOUT_N_ROWS_TILES, LAYOUT_PX_PER_UNIT_LENGHT
from src.activities.game import Game as _Game
from src.graphics import Graphics
from src.sounds import Sounds
from src.graphics.painter import Painter

sys.path.pop(0)
del _GAME_ROOT_DIR

# -----------------------------------------------------------------

# -----------------------------------------------------------------
# Mock game objects.
# -----------------------------------------------------------------
# Mock Sounds class with all methods replaced by no-op.
for name, _ in inspect.getmembers(Sounds, predicate=inspect.isfunction):
    setattr(Sounds, name, lambda *args, **kwargs: None)

# Mock Painter class so that deepcopy actually returns a shallow copy.
# This is needed because textures and other OpenGL context can't be safely deepcopied.
Painter.__deepcopy__ = lambda self, memo: self

# Create minimal-implementation Window class to replace the one used in the real game.
class Window(pyglet.window.Window):
    def __init__(self, width, height, background):
        super().__init__(
            width = width,
            height = height,
            fullscreen = False,
            resizable = False,
            visible = False,
        )
        pyglet.gl.glClearColor(*background, 1)
        self._buffer = (pyglet.gl.GLubyte * (width * height * 3))()

    def draw_frame(self, game):
        if not isinstance(game, Game):
            raise RuntimeError(f"Parameter 'game' must be an instance of class 'Game'. Got {type(game)}")

        self.switch_to()
        self.clear()
        game.event_draw_screen()
        return self._grab_frame()

    def _grab_frame(self):
        pyglet.gl.glPixelStorei(pyglet.gl.GL_PACK_ALIGNMENT, 1)

        pyglet.gl.glReadPixels(
            0, 0,
            self.width, self.height,
            pyglet.gl.GL_RGB,
            pyglet.gl.GL_UNSIGNED_BYTE,
            self._buffer
        )

        # Convert to numpy without copying.
        frame = np.frombuffer(self._buffer, dtype=np.uint8)
        frame = frame.reshape((self.height, self.width, 3))

        # Flip vertically (OpenGL origin is bottom-left).
        frame = np.flipud(frame)

        # Convert colorspaces.
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        return frame


class Game(_Game):

    def __init__(self, level = 1):
        super().__init__(Graphics(), Sounds())
        self._level = level

        # Add an attribute storing if a new game update can be done.
        self._can_be_updated = True

    # Add a deepcopy method to Game class for convenience.
    def deepcopy(self):
        return _deepcopy(self)

    # Override to raise if an update can't be done.
    def event_update_state(self):
        if not self._can_be_updated:
            raise RuntimeError("Game object can no longer be updated.")

        retval = super().event_update_state()
        self._can_be_updated = retval is False

# -----------------------------------------------------------------

# -----------------------------------------------------------------
# Module's private attributes.
# -----------------------------------------------------------------
_WINDOW = Window(LAYOUT_N_COLS_TILES*LAYOUT_PX_PER_UNIT_LENGHT,
                 LAYOUT_N_ROWS_TILES*LAYOUT_PX_PER_UNIT_LENGHT,
                 BACKGROUND_COLOR)

# -----------------------------------------------------------------

# -----------------------------------------------------------------
# Module's public interface.
# -----------------------------------------------------------------

class GameFrames(AbstractFrameGenerator):
    def __init__(self, game = None, **kwargs):
        super().__init__(**kwargs)

        # Public attribute: game can be accessed and modified from the exterior.
        self.game = game if game is not None else Game()

    @contextmanager
    def _make_stream(self):
        self._check_game_attribute()
        yield

    def _get_height_width(self):
        return _WINDOW.height, _WINDOW.width

    def _get_fps(self):
        return GAME_ORIGINAL_FPS

    def _get_frames_count(self):
        return None

    def _read_frame(self):
        success = self._grab_frame()
        return success, _WINDOW.draw_frame(self.game)

    def _grab_frame(self):
        self._check_game_attribute()
        try:
            self.game.event_update_state()
        except Exception:
            return False
        return True

    def _check_game_attribute(self):
        if not isinstance(self.game, Game):
            raise TypeError(f"self.game must be of type {Game.__name__}. Got: {self.game.__class__.__name__}.")


__all__ = ["GameFrames"]

# -----------------------------------------------------------------
