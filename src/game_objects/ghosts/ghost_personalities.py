# -*- coding: utf-8 -*-


from src.game_objects.ghosts.ghost_abstract import GhostAbstract

from src.constants import (Ghost,)



class Blinky(GhostAbstract):

    def __init__(self):
        super().__init__(Ghost.BLINKY)
        self._just_exited_pen()

    def _calculate_target_tile(self, pacman, maze):
        # Blinky always targets the tile Pac-Man is on.
        pacman_tile = maze.get_tile_center(pacman.position)
        return pacman_tile


class Pinky(GhostAbstract):

    def __init__(self):
        super().__init__(Ghost.PINKY)

        
    def update(*args, **kwargs):
        return

    def _calculate_target_tile(self, pacman, maze):
        pass


class Inky(GhostAbstract):

    def __init__(self):
        super().__init__(Ghost.INKY)

    def update(*args, **kwargs):
        return

    def _calculate_target_tile(self, pacman, maze):
        pass


class Clyde(GhostAbstract):

    def __init__(self):
        super().__init__(Ghost.CLYDE)

    def update(*args, **kwargs):
        return

    def _calculate_target_tile(self, pacman, maze):
        pass