# -*- coding: utf-8 -*-


from src.constants import (PACMAN_ALL_SPRITES,
                           PACMAN_GHOSTS_SPRITES_PX_SIZE,
                           PACMAN_MOVE_ANIMATION_PERIOD_FRAMES,
                           PACMAN_DEATH_ANIMATION_PERIOD_FRAMES,
                           PacManStates,
                           PACMAN_SPAWNING_FRAME_IDX,
                           PACMAN_SPRITE_IDX)
from src.graphics import utils


class PacManSprite:

    def __init__(self):
        self._sprites = utils.load_image_grid(PACMAN_ALL_SPRITES, PACMAN_GHOSTS_SPRITES_PX_SIZE)

        self.reset()

    def reset(self):
        self._frame_counter = 0
        self._valid_stuck_frame = False
        self._was_already_dead = False

    def draw(self, pacman):
        sprite_idx = self._get_sprite_idx(pacman.direction, pacman.state)
        pacman_coords = utils.calculate_coords_sprites(pacman.position)
        self._sprites[sprite_idx].blit(x=pacman_coords.x, y=pacman_coords.y)

        # Update boolean describing if current frame is valid for remaining on it if Pac-Man stuck.
        self._valid_stuck_frame = sprite_idx != PACMAN_SPAWNING_FRAME_IDX

    def update(self, pacman):
        match pacman.state:
            case PacManStates.STUCK:
                # Freeze the animation, as long as Pac-Man is not a full yellow circle.
                self._frame_counter += not self._valid_stuck_frame

            case PacManStates.SPAWNING:
                # Do not increase frame counter, set it to start instead.
                self._frame_counter = 0

            case PacManStates.DEAD:
                if not self._was_already_dead:
                    self._frame_counter = 0
                else:
                    self._frame_counter += 1

                self._was_already_dead = True

            case PacManStates.MOVING | PacManStates.TURNING:
                self._frame_counter += 1

            case _:
                raise ValueError('Unvalid state provided for Pac-Man to PacManSprites.update') 


    def _get_sprite_idx(self, direction, state):

        spawning = state == PacManStates.SPAWNING
        dead     = state == PacManStates.DEAD

        # Calculate index of frame animation for sprite.
        if dead:
            if self._frame_counter >= sum(PACMAN_DEATH_ANIMATION_PERIOD_FRAMES):
                frame_idx = -1

            else:
                cumtime = 0
                for frame_idx, duration in enumerate(PACMAN_DEATH_ANIMATION_PERIOD_FRAMES):
                    cumtime += duration

                    if self._frame_counter < cumtime:
                        break

        else:
            frame_idx = (self._frame_counter // PACMAN_MOVE_ANIMATION_PERIOD_FRAMES) % 4

        sprite_idx = PACMAN_SPRITE_IDX(direction, spawning, dead, frame_idx)
        return sprite_idx