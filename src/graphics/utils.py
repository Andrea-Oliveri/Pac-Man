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

        pyglet.gl.glBindTexture(pyglet.gl.GL_TEXTURE_2D, image.get_texture().id)
        pyglet.gl.glTexParameteri(pyglet.gl.GL_TEXTURE_2D, pyglet.gl.GL_TEXTURE_MAG_FILTER, pyglet.gl.GL_NEAREST)

    return image_grid


def load_animated_sprite(path, tile_size_px, duration, copies = 1):
    image_grid = load_image_grid(path, tile_size_px)

    animation = pyglet.image.Animation.from_image_sequence(image_grid, duration=duration)

    if copies == 1:
        return pyglet.sprite.Sprite(img=animation)
    elif not isinstance(copies, int) or copies <= 0:
        raise ValueError(f"Incorrect value provided to graphics.utils.load_animated_sprite for copies parameter: {copies}")

    return tuple(pyglet.sprite.Sprite(img=animation) for _ in range(copies))


def load_image(path):
    image = pyglet.image.load(path)
        
    # Set anchor points to center.
    image.anchor_x = image.width // 2
    image.anchor_y = image.height // 2

    # Interpolate avoiding blur.
    texture = image.get_texture()
    pyglet.gl.glBindTexture(texture.target, texture.id)
    pyglet.gl.glTexParameteri(texture.target, pyglet.gl.GL_TEXTURE_MAG_FILTER, pyglet.gl.GL_NEAREST)

    return image


def freeze_animated_sprite(sprite, frame_index):
    sprite.paused = True
    sprite.frame_index = frame_index

    # Needed due to Pyglet issue #908 present in Pyglet version 2.0.8:
    # https://github.com/pyglet/pyglet/issues/906
    frame = sprite._animation.frames[sprite._frame_index]
    sprite._set_texture(frame.image.get_texture())

    if frame.duration is not None:
        sprite._next_dt = frame.duration