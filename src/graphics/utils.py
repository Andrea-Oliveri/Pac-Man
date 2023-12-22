# -*- coding: utf-8 -*-

import pyglet.image
import pyglet.gl

from src.constants import (MAZE_TILE_PX_SIZE,
                           MAZE_TILES_COLS,
                           MAZE_TILES_ROWS)
from src.directions import Vector2




def calculate_coords_sprites(maze_coords):
    new_coords = Vector2(x = (- MAZE_TILES_COLS / 2 + maze_coords.x) * MAZE_TILE_PX_SIZE,
                         y = (+ MAZE_TILES_ROWS / 2 - maze_coords.y) * MAZE_TILE_PX_SIZE)
    return new_coords


def load_image_grid(path, tile_size_px):
    sprite_sheet = pyglet.image.load(path)

    n_rows = sprite_sheet.height // tile_size_px
    n_cols = sprite_sheet.width // tile_size_px

    image_grid = pyglet.image.ImageGrid(sprite_sheet, rows=n_rows, columns=n_cols)

    # Set anchor points to center and interpolate avoiding blur for every frame of animation.
    for image in image_grid:
        image.anchor_x = tile_size_px // 2
        image.anchor_y = tile_size_px // 2

        texture = image.get_texture()
        set_texture_interp_mode(texture)

    return image_grid


def load_image(path):
    image = pyglet.image.load(path)
        
    # Set anchor points to center.
    image.anchor_x = image.width // 2
    image.anchor_y = image.height // 2

    # Interpolate avoiding blur.
    texture = image.get_texture()
    set_texture_interp_mode(texture)

    return image


def set_texture_interp_mode(texture):
    pyglet.gl.glBindTexture(pyglet.gl.GL_TEXTURE_2D, texture.id)
    pyglet.gl.glTexParameteri(pyglet.gl.GL_TEXTURE_2D, pyglet.gl.GL_TEXTURE_MAG_FILTER, pyglet.gl.GL_NEAREST)


def enable_transparency_blit():
    # Note that when calling and Pyglet function to draw shapes or text, this is disabled again.
    pyglet.gl.glEnable(pyglet.gl.GL_BLEND)
    pyglet.gl.glBlendFunc(pyglet.gl.GL_SRC_ALPHA, pyglet.gl.GL_ONE_MINUS_SRC_ALPHA)