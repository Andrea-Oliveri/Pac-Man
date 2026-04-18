# -----------------------------------------------------------------
# Change directory to avoid relative imports in project breaking.
# -----------------------------------------------------------------
import os
import sys

GAME_ROOT_DIR = os.path.relpath(os.path.join(os.path.dirname(__file__), '../../..'))
os.chdir(GAME_ROOT_DIR)
sys.path.append(".")
# -----------------------------------------------------------------

# -----------------------------------------------------------------
# Import standard library and installed packages.
# -----------------------------------------------------------------
import inspect
from copy import deepcopy

import pyglet
pyglet.options.shadow_window = False  # See explaination in pacman.py at repo root.

import numpy as np
import cv2
# -----------------------------------------------------------------

# -----------------------------------------------------------------
# Import game objects.
# -----------------------------------------------------------------
from src.constants import BACKGROUND_COLOR, LAYOUT_N_COLS_TILES, LAYOUT_N_ROWS_TILES, LAYOUT_PX_PER_UNIT_LENGHT
from src.activities.game import Game
from src.graphics import Graphics
from src.sounds import Sounds
from src.graphics.painter import Painter
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

# Add a deepcopy method to Game class for convenience.
Game.deepcopy = lambda self: deepcopy(self)

# Add a method to draw the game and return the frame as a cv2 image for convenience.
Game.draw = lambda self: _WINDOW.draw_frame(self)

# -----------------------------------------------------------------

# -----------------------------------------------------------------
# Instance module objects.
# -----------------------------------------------------------------
_WINDOW = Window(LAYOUT_N_COLS_TILES*LAYOUT_PX_PER_UNIT_LENGHT,
                 LAYOUT_N_ROWS_TILES*LAYOUT_PX_PER_UNIT_LENGHT,
                 BACKGROUND_COLOR)

# -----------------------------------------------------------------

# -----------------------------------------------------------------
# Module's public interface.
# -----------------------------------------------------------------
def make_initial_game():
    return Game(Graphics(), Sounds())

__all__ = ["make_initial_game"]
# -----------------------------------------------------------------
