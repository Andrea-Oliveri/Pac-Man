# -*- coding: utf-8 -*-


from src.constants import (SCORE_SHEET_PATH,
                           SCORES_TILE_PX_SIZE,
                           SCORE_SHEET_VALUES,
                           SCORE_FRUIT_EATEN_COORDS,
                           SCORE_FRUIT_VISIBLE_DURATION_FRAMES,
                           SCORE_GHOST_EATEN_DURATION_FRAMES)
from src.graphics import utils


class ScoreSprites:

    def __init__(self):
        image_grid = utils.load_image_grid(SCORE_SHEET_PATH, SCORES_TILE_PX_SIZE)

        iterator = iter(image_grid)
        self._score_tiles = {value: tile for value, tile in zip(SCORE_SHEET_VALUES, iterator)}

        self.reset()

    def reset(self):
        self._fruit_score_frame_counter = 0
        self._fruit_score_value = None

        self._ghost_score_frame_counter = 0
        self._ghost_score_value = None
        self._ghost_score_position = None
        

    def draw(self):
        if self._fruit_score_frame_counter > 0:
            self._score_tiles[self._fruit_score_value].blit(*SCORE_FRUIT_EATEN_COORDS)
        
        if self._ghost_score_frame_counter > 0:
            self._score_tiles[self._ghost_score_value].blit(*self._ghost_score_position)

    def update(self):
        if self._fruit_score_frame_counter > 0:
            self._fruit_score_frame_counter -= 1

        if self._ghost_score_frame_counter > 0:
            self._ghost_score_frame_counter -= 1

    def notify_fruit_eaten(self, score):
        self._fruit_score_frame_counter = SCORE_FRUIT_VISIBLE_DURATION_FRAMES
        self._fruit_score_value = score

    def notify_ghost_eaten(self, score, position):
        position = utils.calculate_coords_sprites(position)

        self._ghost_score_frame_counter = SCORE_GHOST_EATEN_DURATION_FRAMES
        self._ghost_score_value = score
        self._ghost_score_position = (position.x, position.y)