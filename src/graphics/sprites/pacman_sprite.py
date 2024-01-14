# -*- coding: utf-8 -*-

from src.graphics.sprites.sprite import AbstractSprite
from src.constants import (PACMAN_MOVE_ANIMATION_PERIOD_FRAMES,
                           PACMAN_DEATH_ANIMATION_PERIOD_FRAMES,
                           PacManStates,
                           PACMAN_SPRITE_TEX_REGION,
                           Z_COORD_PACMAN)



class PacManSprite(AbstractSprite):

    def reset(self):
        self._frame_counter = 0
        self._valid_stuck_frame = False   # Boolean describing if current frame is valid for remaining on it if Pac-Man stuck.
        self._was_already_dead = False


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
                    self._was_already_dead = True
                else:
                    self._frame_counter += 1

            case PacManStates.MOVING | PacManStates.TURNING:
                self._frame_counter += 1

            case _:
                raise ValueError('Unvalid state provided for Pac-Man to PacManSprites.update') 


    def send_vertex_data(self, pacman):
        tex_region, self._valid_stuck_frame = self._get_tex_region(pacman.direction, pacman.state)
        self._painter.add_quad(pacman.position.x, pacman.position.y, *tex_region, Z_COORD_PACMAN)


    def _get_tex_region(self, direction, state):

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

        return PACMAN_SPRITE_TEX_REGION(direction, spawning, dead, frame_idx)