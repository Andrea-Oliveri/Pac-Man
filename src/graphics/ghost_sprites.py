# -*- coding: utf-8 -*-


from src.constants import (Ghost,
                           GHOSTS_ALL_SPRITES,
                           GHOSTS_MOVE_ANIMATION_PERIOD_FRAMES,
                           GHOSTS_FRIGHT_FLASH_ANIMATION_PERIOD_FRAMES,
                           PACMAN_GHOSTS_SPRITES_PX_SIZE,
                           GHOST_SPRITE_IDX)


from src.graphics import utils


class GhostSprite:

    def __init__(self):
        self._sprites = utils.load_animated_sprite(GHOSTS_ALL_SPRITES, PACMAN_GHOSTS_SPRITES_PX_SIZE, duration=None, copies = len(Ghost))

        self._movement_counter     = 0
        self._fright_flash_counter = 0

    def notify_fright_on(self, fright_duration, fright_flashes):
        # The number of flashes vary, but the pattern goes: blue, white for this amount of time, blue for this amount of time, ...., white for this amount of time and then normal.

        self._fright_flash_counter = 2 * fright_flashes * GHOSTS_FRIGHT_FLASH_ANIMATION_PERIOD_FRAMES - fright_duration - 1


    def draw(self, ghosts):
        for name, ghost in ghosts:
            
            self._update_sprite(name, ghost.frightened, ghost.transparent, ghost.eyes_direction, ghost.position)
            self._sprites[name].draw()


    def update(self):
        self._movement_counter     += 1
        self._fright_flash_counter += 1


    def _update_sprite(self, name, frightened, transparent, direction, position):

        # Calculate index of frame animation for sprite.
        frame_idx = (self._movement_counter // GHOSTS_MOVE_ANIMATION_PERIOD_FRAMES) % 2

        if frightened:
            frightened_blue = self._fright_flash_counter < 0 or \
                              (self._fright_flash_counter // GHOSTS_FRIGHT_FLASH_ANIMATION_PERIOD_FRAMES) % 2 == 0
            frightened_white = not frightened_blue
        else:
            frightened_blue = frightened_white = False

        sprite_idx = GHOST_SPRITE_IDX(name, frightened_blue, frightened_white, transparent, direction, frame_idx)

        # Update sprite frame index.
        utils.freeze_animated_sprite(self._sprites[name], sprite_idx)

        # Update sprite position.
        ghost_coords = utils.calculate_coords_sprites(position)
        self._sprites[name].update(x=ghost_coords.x, y=ghost_coords.y)
