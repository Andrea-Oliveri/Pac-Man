# -*- coding: utf-8 -*-


from src.game_objects.ghosts.ghost_abstract import GhostAbstract

from src.constants import (Ghost,
                           CruiseElroyLevel,
                           CRUISE_ELROY_PELLETS_THR)
from src.directions import Vector2


class Blinky(GhostAbstract):

    def __init__(self, prng):
        super().__init__(Ghost.BLINKY, prng)
        self._direction_next      = Vector2.LEFT
        self._direction_next_next = Vector2.LEFT

    def _calculate_personal_target_tile(self, pacman, maze):
        pacman_tile = maze.get_tile_center(pacman.position)
        return pacman_tile

    def _update_cruise_elroy_level(self, level, pellets_remaining, clyde_in_house, died_this_level):
        if died_this_level and clyde_in_house:
            self._cruise_elroy_level = CruiseElroyLevel.NULL
            return

        first_thr, second_thr = CRUISE_ELROY_PELLETS_THR(level)

        if pellets_remaining <= second_thr:
            self._cruise_elroy_level = CruiseElroyLevel.SECOND
        elif pellets_remaining <= first_thr:
            self._cruise_elroy_level = CruiseElroyLevel.FIRST
        else:
            self._cruise_elroy_level = CruiseElroyLevel.NULL


class Pinky(GhostAbstract):

    def __init__(self, prng):
        super().__init__(Ghost.PINKY, prng)

    def _calculate_personal_target_tile(self, pacman, maze):
        in_front_tile = maze.get_tile_center(pacman.position)
        in_front_tile += pacman.direction * 4

        if pacman.direction == Vector2.UP:
            in_front_tile += Vector2.LEFT * 4

        return in_front_tile


class Inky(GhostAbstract):

    def __init__(self, prng, blinky):
        super().__init__(Ghost.INKY, prng)
        self._blinky = blinky


    def _calculate_personal_target_tile(self, pacman, maze):
        in_front_tile = maze.get_tile_center(pacman.position)
        in_front_tile += pacman.direction * 2

        if pacman.direction == Vector2.UP:
            in_front_tile += Vector2.LEFT * 2

        blinky_tile = maze.get_tile_center(self._blinky.position)

        target_tile = 2 * in_front_tile - blinky_tile

        return target_tile


class Clyde(GhostAbstract):

    def __init__(self, prng):
        super().__init__(Ghost.CLYDE, prng)


    def _calculate_personal_target_tile(self, pacman, maze):
        distance_squared = Vector2.distance_squared(self._position, pacman.position)

        # If distance from Pac-Man is larger than 8 tiles.
        if distance_squared > 64:
            pacman_tile = maze.get_tile_center(pacman.position)
            return pacman_tile

        return self._scatter_mode_target_tile