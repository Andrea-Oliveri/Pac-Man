# -*- coding: utf-8 -*-


from src.constants import (GHOSTS_ALL_SPRITES,
                           GHOSTS_MOVE_ANIMATION_PERIOD_FRAMES,
                           GHOSTS_FRIGHT_FLASH_ANIMATION_PERIOD_FRAMES,
                           PACMAN_GHOSTS_SPRITES_PX_SIZE,
                           GHOST_SPRITE_IDX)


from src.graphics import utils


class GhostSprite:

    def __init__(self):
        self._sprites = utils.load_image_grid(GHOSTS_ALL_SPRITES, PACMAN_GHOSTS_SPRITES_PX_SIZE)

        self.reset()
        
    def reset(self):
        self._movement_counter     = 0
        self._fright_flash_counter = 0

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


    def draw(self, ghosts):
        # Ghosts should be drawn in reverse order so that Clyde appears on bottom and Blinky on top. 
        for ghost in reversed(list(ghosts)):
            if ghost.was_just_eaten:
                continue

            sprite_idx = self._get_sprite_idx(ghost.name, ghost.frightened, ghost.transparent, ghost.eyes_direction)
            ghost_coords = utils.calculate_coords_sprites(ghost.position)
            self._sprites[sprite_idx].blit(x=ghost_coords.x, y=ghost_coords.y)


    def update(self):
        self._movement_counter     += 1
        self._fright_flash_counter += 1


    def _get_sprite_idx(self, name, frightened, transparent, direction):

        # Calculate index of frame animation for sprite.
        frame_idx = (self._movement_counter // GHOSTS_MOVE_ANIMATION_PERIOD_FRAMES) % 2

        if frightened:
            frightened_blue = self._fright_flash_counter < 0 or \
                              (self._fright_flash_counter // GHOSTS_FRIGHT_FLASH_ANIMATION_PERIOD_FRAMES) % 2 == 1
            frightened_white = not frightened_blue
        else:
            frightened_blue = frightened_white = False

        sprite_idx = GHOST_SPRITE_IDX(name, frightened_blue, frightened_white, transparent, direction, frame_idx)
        return sprite_idx
