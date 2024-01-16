# -*- coding: utf-8 -*-

from src.graphics.sprites.sprite import AbstractSprite
from src.constants import (MAZE_TILES_ROWS,
                           MAZE_TILES_COLS,
                           LEVEL_COMPLETED_FLASH_ANIMATION_PERIOD_FRAMES,
                           MAZE_SPRITE_TEX_REGION,
                           Z_COORD_MAZE)
from src.graphics.utils import convert_maze_coord_to_layout_coord
from src.directions import Vector2



class MazeSprite(AbstractSprite):
        
    def reset(self):
        self._flash_counter = None


    def update(self):
        if self._flash_counter is not None:
            self._flash_counter += 1


    def send_vertex_data(self, maze):

        if self._flash_counter is None:
            flash_blue  = False
            flash_white = False
        elif (self._flash_counter // LEVEL_COMPLETED_FLASH_ANIMATION_PERIOD_FRAMES) % 2:
            flash_blue  = True
            flash_white = False
        else:
            flash_blue  = False
            flash_white = True

        origin = convert_maze_coord_to_layout_coord(Vector2.ZERO)
        offset_x = origin.x + 0.5
        offset_y = origin.y + 0.5

        for row in range(MAZE_TILES_ROWS):
            for col in range(MAZE_TILES_COLS):
                tile = maze[row, col]

                tex_region = MAZE_SPRITE_TEX_REGION(row, col, tile, flash_blue, flash_white)

                self._painter.add_quad(col + offset_x, row + offset_y, *tex_region, Z_COORD_MAZE)
 

    def notify_level_end(self):
        self._flash_counter = 0