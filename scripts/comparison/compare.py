import os
import sys
os.chdir(os.path.relpath(os.path.join(os.path.dirname(__file__), '../..')))
sys.path.append(".")

import inspect

import pyglet
pyglet.options.shadow_window = False

import numpy as np
import cv2

from src.activities.game import Game
from src.constants import WINDOW_MINIMUM_SIZE, BACKGROUND_COLOR
from src.graphics import Graphics
from src.sounds import Sounds
from src.window import Window


# Mock Sounds class with all methods replaced by no-op.
for name, _ in inspect.getmembers(Sounds, predicate=inspect.isfunction):
    setattr(Sounds, name, lambda *args, **kwargs: None)


from collections import deque
queue = deque(maxlen = 100)
import time
def _print_fps():
    queue.append(time.time())
    if len(queue) > 1:
        mean = sum(queue[i] - queue[i-1] for i in range(1, len(queue))) / len(queue)
        print(1 / mean)




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
        
        _print_fps()
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




window = Window(*WINDOW_MINIMUM_SIZE, BACKGROUND_COLOR)
game = Game(Graphics(), Sounds())

while True:
    if game.event_update_state() is True:
        break
    frame = window.draw_frame(game)

    continue
    frame = cv2.resize(
        frame,
        None,
        fx=2,
        fy=2,
        interpolation=cv2.INTER_NEAREST
    )
    cv2.imshow("", frame)
    if cv2.waitKey(1) == ord("q"):
        quit()

print("Game Over")