# -*- coding: utf-8 -*-

from src.graphics.sprites.sprite import AbstractSprite
from src.constants import (FRUIT_SPAWN_POSITION,
                           SCORE_FRUIT_VISIBLE_DURATION_FRAMES,
                           SCORE_GHOST_EATEN_DURATION_FRAMES,
                           SCORE_SPRITE_TEX_REGION,
                           Z_COORD_SCORE_FRUIT,
                           Z_COORD_SCORE_GHOST_EAT)
from src.graphics.utils import convert_maze_coord_to_layout_coord


class ScoreSprite(AbstractSprite):

    def reset(self):
        self._fruit_score_frame_counter = 0
        self._fruit_score_value = None

        self._ghost_score_frame_counter = 0
        self._ghost_score_value = None
        self._ghost_score_position = None
        

    def update(self):
        if self._fruit_score_frame_counter > 0:
            self._fruit_score_frame_counter -= 1

        if self._ghost_score_frame_counter > 0:
            self._ghost_score_frame_counter -= 1


    def send_vertex_data(self):
        if self._fruit_score_frame_counter > 0:
            tex_region = SCORE_SPRITE_TEX_REGION(self._fruit_score_value)
            coords = convert_maze_coord_to_layout_coord(FRUIT_SPAWN_POSITION)
            self._painter.add_quad(coords.x, coords.y, *tex_region, Z_COORD_SCORE_FRUIT)
        
        if self._ghost_score_frame_counter > 0:
            tex_region = SCORE_SPRITE_TEX_REGION(self._ghost_score_value)
            coords = convert_maze_coord_to_layout_coord(self._ghost_score_position)
            self._painter.add_quad(coords.x, coords.y, *tex_region, Z_COORD_SCORE_GHOST_EAT)

    
    def notify_fruit_eaten(self, score):
        self._fruit_score_frame_counter = SCORE_FRUIT_VISIBLE_DURATION_FRAMES
        self._fruit_score_value = score


    def notify_ghost_eaten(self, score, position):
        self._ghost_score_frame_counter = SCORE_GHOST_EATEN_DURATION_FRAMES
        self._ghost_score_value = score
        self._ghost_score_position = position