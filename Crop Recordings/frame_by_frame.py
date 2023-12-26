# -*- coding: utf-8 -*-

import pyglet
pyglet.options['shadow_window'] = False

from pyglet.window import key




class Window(pyglet.window.Window):
    def __init__(self):
        super().__init__(300, 300, vsync = True)
        
        self.set_minimum_size(300, 300)

        _files_and_sizes = [('intermission1.png', 88 , 224),
                            ('intermission2.png', 88 , 224),
                            ('intermission3.png', 88 , 224),
                            ('intro.png'        , 288, 224),
                            ('attract.png'      , 288, 224)][:4]

        self._image_grids = [self.load_image_grid(p, w, h) for p, h, w in _files_and_sizes]

        self._file_idx  = 0
        self._frame_idx = 0

        self._frame_delta = 1

        pyglet.clock.schedule_interval(self._on_state_update, 1/60)


    
    def load_image_grid(self, path, w, h):
        sprite_sheet = pyglet.image.load(path)

        n_rows = sprite_sheet.height // h
        n_cols = sprite_sheet.width // w

        image_grid = pyglet.image.ImageGrid(sprite_sheet, rows=n_rows, columns=n_cols)

        # Set anchor points to center and interpolate avoiding blur for every frame of animation.
        for image in image_grid:
            image.anchor_x = w // 2
            image.anchor_y = h // 2

            texture = image.get_texture()
            pyglet.gl.glBindTexture(pyglet.gl.GL_TEXTURE_2D, texture.id)
            pyglet.gl.glTexParameteri(pyglet.gl.GL_TEXTURE_2D, pyglet.gl.GL_TEXTURE_MAG_FILTER, pyglet.gl.GL_NEAREST)

        return image_grid        

    def _on_state_update(self, _):
        self._frame_idx = (self._frame_idx - self._frame_delta) % len(self._image_grids[self._file_idx])


    def on_resize(self, width, height):
        desired_width, desired_height = 300, 300

        scale = min(width // desired_width, height // desired_height)
        viewport_width  = desired_width * scale
        viewport_height = desired_height * scale

        pad_x = (width  - viewport_width ) / 2
        pad_y = (height - viewport_height) / 2

        self.viewport = (pad_x, pad_y, viewport_width, viewport_height)

        x_max = desired_width  / 2
        y_max = desired_height / 2

        self.projection = pyglet.math.Mat4.orthogonal_projection(-x_max, +x_max, -y_max, +y_max, -255, 255)
        
        return pyglet.event.EVENT_HANDLED   # Don't call the default handler


    def on_key_press(self, symbol, modifiers):
        if symbol == key.UP:
            self._file_idx -= 1
            self._frame_idx = 0
        elif symbol == key.DOWN:
            self._file_idx += 1
            self._frame_idx = 0
        elif symbol == key.RIGHT:
            self._frame_delta = +1
        elif symbol == key.LEFT:
            self._frame_delta = -1

        self._file_idx = self._file_idx  % len(self._image_grids)


    def on_draw(self):
        self.clear()
        self._image_grids[self._file_idx][self._frame_idx].blit(0, 0)


a = Window()
pyglet.app.run()