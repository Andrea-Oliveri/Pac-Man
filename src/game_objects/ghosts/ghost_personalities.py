# -*- coding: utf-8 -*-


from src.game_objects.ghosts.ghost_abstract import GhostAbstract

from src.constants import (Ghost,
                           GHOSTS_SCATTER_MODE_TARGET_TILES)
from src.directions import Vector2


class Blinky(GhostAbstract):

    def __init__(self, prng):
        super().__init__(Ghost.BLINKY, prng)
        self._just_exited_pen()

    def _calculate_personal_target_tile(self, pacman, maze):
        pacman_tile = maze.get_tile_center(pacman.position)
        return pacman_tile


class Pinky(GhostAbstract):

    def __init__(self, prng):
        super().__init__(Ghost.PINKY, prng)
    
        # ----------------------
        # DEBUG
        # ----------------------
        from src.directions import Vector2
        self._position = Vector2(x = 14, y = 11.5)
        self._just_exited_pen()
        # ----------------------

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

        # ----------------------
        # DEBUG
        # ----------------------
        from src.directions import Vector2
        self._position = Vector2(x = 14, y = 11.5)
        self._just_exited_pen()
        # ----------------------

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

        # ----------------------
        # DEBUG
        # ----------------------
        from src.directions import Vector2
        self._position = Vector2(x = 14, y = 11.5)
        self._just_exited_pen()
        # ----------------------

    def _calculate_personal_target_tile(self, pacman, maze):
        distance_squared = Vector2.distance_squared(self._position, pacman.position)

        # If distance from Pac-Man is larger than 8 tiles.
        if distance_squared > 64:
            pacman_tile = maze.get_tile_center(pacman.position)
            return pacman_tile

        return GHOSTS_SCATTER_MODE_TARGET_TILES[Ghost.CLYDE]