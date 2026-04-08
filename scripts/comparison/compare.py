import os
import sys
os.chdir(os.path.relpath(os.path.join(os.path.dirname(__file__), '../..')))
sys.path.append(".")

import inspect
from threading import Thread

import pyglet
pyglet.options.shadow_window = False

import numpy as np

from src.activities.game import Game
from src.constants import *
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


width = WINDOW_MINIMUM_SIZE[0]
height = WINDOW_MINIMUM_SIZE[1]
buffer = (pyglet.gl.GLubyte * (width * height * 3))()


class Window(pyglet.window.Window):
    def __init__(self):
        super().__init__(
            width = width,
            height = height,
            fullscreen = False,
            resizable = False,
            visible = False
        )
        pyglet.gl.glClearColor(*BACKGROUND_COLOR, 1)
        self._game = Game(Graphics(), Sounds())

    def on_draw(self):
        _print_fps()
        self.clear()
        self._game.event_draw_screen()
        
        
        import cv2        
        frame = self.grab_frame()
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
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


    def grab_frame(self):
        global buffer
        pyglet.gl.glPixelStorei(pyglet.gl.GL_PACK_ALIGNMENT, 1)

        pyglet.gl.glReadPixels(
            0, 0,
            width, height,
            pyglet.gl.GL_RGB,
            pyglet.gl.GL_UNSIGNED_BYTE,
            buffer
        )

        # Convert to numpy without copying.
        frame = np.frombuffer(buffer, dtype=np.uint8)
        frame = frame.reshape((height, width, 3))

        # Flip vertically (OpenGL origin is bottom-left).
        frame = np.flipud(frame)

        return frame


    def update(self, _):
        return self._game.event_update_state()



window = Window()

while True:
    if window.update(0) is True:
        break
    window.on_draw()

print("Game Over")