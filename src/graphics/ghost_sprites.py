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
        # The number of flashes vary, but the pattern goes: blue, white for this amount of time, blue for this amount of time, ...., white for this amount of time and then normal.

        flashing_time = (2 * fright_flashes - 1) * GHOSTS_FRIGHT_FLASH_ANIMATION_PERIOD_FRAMES

        if fright_duration > flashing_time:
            self._fright_flash_counter = flashing_time - fright_duration - 1
            return
        
        self._fright_flash_counter = 0


    def draw(self, ghosts):
        utils.enable_transparency_blit()

        for ghost in ghosts:
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
