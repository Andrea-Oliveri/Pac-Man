# -*- coding: utf-8 -*-

import pyglet

from src.constants import LAYOUT_MAZE_COORDS
from src.directions import Vector2


def load_image(path, file = None):
    image = pyglet.image.load(path, file)
        
    # Set anchor points to center.
    image.anchor_x = image.width // 2
    image.anchor_y = image.height // 2

    # Interpolate avoiding blur.
    texture = image.get_texture()
    set_texture_interp_mode(texture)

    return image


def load_image_grid(path, width_px, height_px = None, file = None):
    if height_px is None:
        height_px = width_px

    sheet = pyglet.image.load(path, file)

    n_rows = sheet.height // height_px
    n_cols = sheet.width // width_px

    image_grid = pyglet.image.ImageGrid(sheet, rows=n_rows, columns=n_cols)

    # Set anchor points to center and interpolate avoiding blur for every frame of animation.
    for image in image_grid:
        image.anchor_x = width_px // 2
        image.anchor_y = height_px // 2

        texture = image.get_texture()
        set_texture_interp_mode(texture)

    return image_grid


def set_texture_interp_mode(texture):
    pyglet.gl.glBindTexture(pyglet.gl.GL_TEXTURE_2D, texture.id)
    pyglet.gl.glTexParameteri(pyglet.gl.GL_TEXTURE_2D, pyglet.gl.GL_TEXTURE_MAG_FILTER, pyglet.gl.GL_NEAREST)


def enable_transparency_blit():
    # Note that when calling and Pyglet function to draw shapes or text, this is disabled again.
    pyglet.gl.glEnable(pyglet.gl.GL_BLEND)
    pyglet.gl.glBlendFunc(pyglet.gl.GL_SRC_ALPHA, pyglet.gl.GL_ONE_MINUS_SRC_ALPHA)


def enable_depth_testing():
    pyglet.gl.glEnable(pyglet.gl.GL_DEPTH_TEST)


def convert_maze_coord_to_layout_coord(position):
    return position + Vector2(0, int(LAYOUT_MAZE_COORDS[1]))