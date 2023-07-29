# -*- coding: utf-8 -*-

from enum import IntEnum

from src.utils import Vector2

from src.constants import (PACMAN_MOVE_SPEED_TILES,
                           PACMAN_START_TILE,
                           PacManStates)





class PacMan:

    def __init__(self):
        self._position  = Vector2(*PACMAN_START_TILE)
        self._direction = Vector2.LEFT
        self._state     = PacManStates.SPAWNING


        # To be removed. For debugging.
        self.collision_box_position = self._position + (self._direction * 0.5)


    def update_position(self, dt, maze):

        # -----------------------------------------
        # Placeholder to go from spawning to moving.
        # -----------------------------------------
        self._i = getattr(self, '_i', 0) + 1
        self._deactivate = getattr(self, '_deactivate', False)
        if self._i > 100 and not self._deactivate:
            self._deactivate = True
            self._state = PacManStates.MOVING
        if not self._i % 100:
            print(self.position, self.collision_box_position)
        # -----------------------------------------


        if self._state == PacManStates.SPAWNING or self._state == PacManStates.DEAD:
            return


        new_position = self.position + self._direction * (PACMAN_MOVE_SPEED_TILES * dt)

        # Check if movement will cause a collision. If so, clip instead of moving into wall.
        # This collision detection does not account for very high speeds, which could allow Pac-Man to teleport through wall
        # (only final position is checked for a collision, not points in between).
        collision_box_position = self._position + (self._direction * 0.5000001)
        
        self.collision_box_position = collision_box_position
        if maze.tile_is_wall(collision_box_position):
            match self._direction:
                case Vector2.LEFT, Vector2.RIGHT:
                    new_position.x = int(new_position.x) + 0.5
                case Vector2.UP  , Vector2.DOWN:
                    new_position.y = int(new_position.y) + 0.5

            self._state = PacManStates.STUCK
        else:
            self._state = PacManStates.MOVING


        self._position = new_position




    # Defining properties for some private attributes.
    def _set_direction(self, direction):
        if direction not in (Vector2.LEFT, Vector2.RIGHT, Vector2.UP, Vector2.DOWN):
            raise ValueError('Unvalid direction provided for Pac-Man to Pacman.set_direction')

        self._direction = direction

    position  = property(lambda self: self._position)
    direction = property(lambda self: self._direction, _set_direction)
    state     = property(lambda self: self._state)
