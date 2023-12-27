# -*- coding: utf-8 -*-

import pyglet

from tilemap import TileMap
from renderer import VertexBufferedRenderer, GeomBufferedRenderer, VertexBufferedRendererPyglet, N_ROWS, N_COLS

WINDOW_MINIMUM_SIZE = (N_COLS * 8, N_ROWS * 8)


class Window(pyglet.window.Window):
    def __init__(self):
        super().__init__(*WINDOW_MINIMUM_SIZE, vsync = False, resizable = True)
        
        self.set_minimum_size(*WINDOW_MINIMUM_SIZE)

        self._tilemap = TileMap()
        self._tilemap.random_fill()

        self._renderer = VertexBufferedRenderer(self._tilemap)

        
    def on_resize(self, width, height):
        desired_width, desired_height = WINDOW_MINIMUM_SIZE

        scale = min(width // desired_width, height // desired_height)
        viewport_width  = desired_width * scale
        viewport_height = desired_height * scale

        pad_x = (width  - viewport_width ) / 2
        pad_y = (height - viewport_height) / 2

        self.viewport = (pad_x, pad_y, viewport_width, viewport_height)

        #self.projection = pyglet.math.Mat4.orthogonal_projection(-1, +1, -1, +1, -255, 255)

        return pyglet.event.EVENT_HANDLED   # Don't call the default handler


    def on_key_press(self, symbol, modifiers):
        self._tilemap.random_fill()
        self._renderer.recalculate()

        
    def on_draw(self):
        self.clear()
        self._renderer.draw(self.width, self.height)

        # Draw FPS counter
        if not hasattr(self, 'fps_display'):
            self.fps_display = pyglet.window.FPSDisplay(window=self)
            self.fps_display.label = pyglet.text.Label('', x=70, y=135, font_size=12, bold=True, color = (255, 0, 0, 255))

        self.fps_display.draw()
        
        # Draw coordinate set
        #pyglet.shapes.Line(0, 0, 100, 0, width=2, color = (255, 0, 0)).draw()
        #pyglet.shapes.Line(0, 0, 0, 100, width=2, color = (0, 255, 0)).draw()
        #pyglet.shapes.Circle(0, 0, 5, color=(0, 0, 255)).draw()

        #pyglet.shapes.Circle(-150, -150, 5, color=(0, 0, 255)).draw()
