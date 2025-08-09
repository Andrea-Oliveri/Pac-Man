# -*- coding: utf-8 -*-

from src.graphics.sprites.sprite import AbstractSprite
from src.constants import (MazeTiles,
                           MAZE_TILES_ROWS,
                           MAZE_TILES_COLS,
                           LEVEL_COMPLETED_FLASH_ANIMATION_PERIOD_FRAMES,
                           POWER_PELLET_FLASH_ANIMATION_PERIOD_FRAMES,
                           MAZE_SPRITE_TEX_REGION,
                           Z_COORD_MAZE)
from src.graphics.utils import convert_maze_coord_to_layout_coord
from src.directions import Vector2



class MazeSprite(AbstractSprite):
        
    def reset(self):
        self._flash_counter_power_pellet = 0
        self._flash_counter_walls = None


    def update(self):
        self._flash_counter_power_pellet += 1
        if self._flash_counter_walls is not None:
            self._flash_counter_walls += 1


    def send_vertex_data(self, maze):

        if self._flash_counter_walls is None:
            flash_blue  = False
            flash_white = False
        elif (self._flash_counter_walls // LEVEL_COMPLETED_FLASH_ANIMATION_PERIOD_FRAMES) % 2:
            flash_blue  = True
            flash_white = False
        else:
            flash_blue  = False
            flash_white = True

        origin = convert_maze_coord_to_layout_coord(Vector2.ZERO)
        offset_x = origin.x + 0.5
        offset_y = origin.y + 0.5

        for row in range(MAZE_TILES_ROWS):
            y_coord = row + offset_y

            for col in range(MAZE_TILES_COLS):
                x_coord = col + offset_x

                tile = maze[row, col]
                if tile == MazeTiles.POWER_PELLET and (self._flash_counter_power_pellet // POWER_PELLET_FLASH_ANIMATION_PERIOD_FRAMES) % 2:
                    continue

                tex_region = MAZE_SPRITE_TEX_REGION(row, col, tile, flash_blue, flash_white)
                self._painter.add_quad(x_coord, y_coord, *tex_region, Z_COORD_MAZE)
 

    def notify_level_end(self):
        self._flash_counter_walls = 0