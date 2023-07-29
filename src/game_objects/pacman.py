# -*- coding: utf-8 -*-

from src.utils import Vector2

from src.constants import (PACMAN_MOVE_SPEED_TILES,
                           PACMAN_START_TILE)


class PacMan:

    def __init__(self):
        self._position = Vector2(*PACMAN_START_TILE)

        self._direction = Vector2.LEFT

    def update_position(self, dt, maze):
        new_position = self.position + self._direction * (PACMAN_MOVE_SPEED_TILES * dt)

        if maze.tile_is_walkable(new_position):
            self._position = new_position

    def set_direction(self, direction):
        if direction not in (Vector2.LEFT, Vector2.RIGHT, Vector2.UP, Vector2.DOWN):
            raise ValueError('Unvalid direction provided for Pac-Man to Pacman.set_direction')

        self._direction = direction

    position  = property(lambda self: self._position)
    direction = property(lambda self: self._direction, set_direction)
