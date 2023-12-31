# -*- coding: utf-8 -*-


from src.constants import (SCORE_SHEET_PATH,
                           SCORES_TILE_PX_SIZE,
                           SCORES_SPRITE_IDX,
                           SCORE_FRUIT_EATEN_COORDS)
from src.graphics import utils


class ScoreSprites:

    def __init__(self):
        self._sprites = utils.load_image_grid(SCORE_SHEET_PATH, SCORES_TILE_PX_SIZE)

        self.reset()

    def reset(self):
        self._fruit_score_frame_counter = 0
        self._fruit_score_value = None

        self._ghost_score_position = None
        self._fruit_score_value = None

    def draw(self):
        if self._fruit_score_frame_counter > 0:
            sprite_idx = SCORES_SPRITE_IDX(self._fruit_score_value)
            self._sprites[sprite_idx].blit(*SCORE_FRUIT_EATEN_COORDS)
        
        if self._ghost_score_position is not None:
            sprite_idx = SCORES_SPRITE_IDX(self._fruit_score_value)
            self._sprites[sprite_idx].blit(*self._ghost_score_position)
        
    def update(self, pacman):
        pass
    