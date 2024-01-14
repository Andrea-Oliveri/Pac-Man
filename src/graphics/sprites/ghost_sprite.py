# -*- coding: utf-8 -*-

from src.graphics.sprites.sprite import AbstractSprite
from src.constants import (GHOSTS_MOVE_ANIMATION_PERIOD_FRAMES,
                           GHOSTS_FRIGHT_FLASH_ANIMATION_PERIOD_FRAMES,
                           GHOST_SPRITE_TEX_REGION,
                           Z_COORD_GHOSTS)



class GhostSprite(AbstractSprite):
        
    def reset(self):
        self._movement_counter     = 0
        self._fright_flash_counter = 0


    def update(self):
        self._movement_counter     += 1
        self._fright_flash_counter += 1


    def send_vertex_data(self, ghosts):
        for ghost in ghosts:
            if ghost.was_just_eaten:
                continue

            tex_region = self._get_tex_region(ghost.name, ghost.frightened, ghost.transparent, ghost.eyes_direction)
            self._painter.add_quad(ghost.position.x, ghost.position.y, *tex_region, Z_COORD_GHOSTS)


    def notify_fright_on(self, fright_duration, fright_flashes):
        # The regular pattern of flashes goes: blue, white for 14 frames, blue for 14 frames, ...., white for 14 frames and then ghosts not frightened anymore.
        # On some levels, the full pattern with the correct number of flashes may not fit entirely given the expected duration.
        # In this case, the pattern starts with white for 14 frames and ends with white, which can however be shorter than 14 frames.
        # This is consistent with the original game. What is not completely consistent is that the original game does not guarantee 14 white frames even when the
        # whole flashing could fit. The reason and logic behind this is a mistery and completely undocumented.

        flashing_time = (2 * fright_flashes - 1) * GHOSTS_FRIGHT_FLASH_ANIMATION_PERIOD_FRAMES

        if fright_duration > flashing_time:
            self._fright_flash_counter = flashing_time - fright_duration - 1
            return
        
        self._fright_flash_counter = 0


    def _get_tex_region(self, name, frightened, transparent, eyes_direction):
        movement_frame_idx = (self._movement_counter // GHOSTS_MOVE_ANIMATION_PERIOD_FRAMES) % 2

        if frightened:
            frightened_blue = self._fright_flash_counter < 0 or \
                                (self._fright_flash_counter // GHOSTS_FRIGHT_FLASH_ANIMATION_PERIOD_FRAMES) % 2 == 1
            frightened_white = not frightened_blue
        else:
            frightened_blue = frightened_white = False

        return GHOST_SPRITE_TEX_REGION(name, frightened_blue, frightened_white, transparent, eyes_direction, movement_frame_idx)