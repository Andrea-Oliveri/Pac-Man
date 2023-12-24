# -*- coding: utf-8 -*-

import pyglet.gl

from src.constants import (MAZE_START_IMAGE,
                           MAZE_START_IMAGE_EMPTY_TILE_REGION_COORDS,
                           MAZE_TILE_PX_SIZE,
                           MAZE_TILES_ROWS)


from src.graphics import utils


class MazeSprite:

    def __init__(self):
        self._maze_image = None
        self._maze_empty_tile = None
        
    def reset(self):
        self._maze_image = utils.load_image(MAZE_START_IMAGE)
        self._maze_empty_tile = self._maze_image.get_region(*MAZE_START_IMAGE_EMPTY_TILE_REGION_COORDS, MAZE_TILE_PX_SIZE, MAZE_TILE_PX_SIZE)
        
    def draw(self):
        self._maze_image.blit(0, 0)

    def update(self):
        return

    def set_empty_tile(self, maze_row, maze_col):
        destination_left_px   = maze_col * MAZE_TILE_PX_SIZE
        destination_bottom_px = (MAZE_TILES_ROWS - maze_row - 1) * MAZE_TILE_PX_SIZE

        source_texture      = self._maze_empty_tile.get_texture()
        destination_texture = self._maze_image.get_texture()

        pyglet.gl.glCopyImageSubData(source_texture.id,
 	                                 source_texture.target,
 	                                 source_texture.level,
                                     0,
                                     0,
                                     0,
                                     destination_texture.id,
                                     destination_texture.target,
                                     destination_texture.level,
                                     destination_left_px, 
                                     destination_bottom_px,
                                     0,
                                     source_texture.width,
                                     source_texture.height,
                                     1)