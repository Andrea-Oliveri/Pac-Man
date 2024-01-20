# -*- coding: utf-8 -*-

import pyglet

from src.constants import LAYOUT_MAZE_COORDS
from src.directions import Vector2


def load_image(path, file = None):
    image = pyglet.image.load(path, file)

    # Interpolate avoiding blur.
    texture = image.get_texture()
    set_texture_interp_mode(texture)

    return image


def load_recording(path, frame_width_px, frame_height_px, file = None):
# This function generates a different texture for every frame.
# This would generally impact negatively performance, but drawing when recordings are active is not performance-intensive.
# Crucially, doing this bypasses the maximum texture size limit which applies to single textures. 

    recording = pyglet.image.load(path, file)

    n_rows = recording.height // frame_height_px
    n_cols = recording.width  // frame_width_px

    frames_grid = pyglet.image.ImageGrid(recording, rows=n_rows, columns=n_cols)

    # Interpolate avoiding blur for every frame of animation.
    for frame in frames_grid:
        texture = frame.get_texture()
        set_texture_interp_mode(texture)

    return frames_grid


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