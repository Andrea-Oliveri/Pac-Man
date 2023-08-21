# -*- coding: utf-8 -*-


from src.game_objects.ghosts.ghost_abstract import GhostAbstract

from src.constants import (Ghost,)
from src.directions import Vector2


class Blinky(GhostAbstract):

    def __init__(self, prng):
        super().__init__(Ghost.BLINKY, prng)
        self._just_exited_pen()

    def _calculate_personal_target_tile(self, pacman, maze):
        # Blinky targets the tile Pac-Man is on.
        target_tile = maze.get_tile_center(pacman.position)
        return target_tile


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
        # Pinky targets 4 tiles in front of Pac-Man. Due to an error, if Pac-Man direction is upwards, 
        # targets 4 tiles up and 4 tiles left.
        target_tile = maze.get_tile_center(pacman.position)
        target_tile += pacman.direction * 4

        if pacman.direction == Vector2.UP:
            target_tile += Vector2.LEFT * 4

        return target_tile


class Inky(GhostAbstract):

    def __init__(self, prng):
        super().__init__(Ghost.INKY, prng)

    def update(*args, **kwargs):
        return

    def _calculate_personal_target_tile(self, pacman, maze):
        pass


class Clyde(GhostAbstract):

    def __init__(self, prng):
        super().__init__(Ghost.CLYDE, prng)

    def update(*args, **kwargs):
        return

    def _calculate_personal_target_tile(self, pacman, maze):
        pass