# -*- coding: utf-8 -*-


from src.constants import (Ghost,
                           GHOSTS_START_POSITIONS,
                           GHOSTS_START_DIRECTIONS)


class GhostsCoordinator:

    def __init__(self):
        pass




class Ghost:
    def __init__(self, ghost_id):
        self._ghost_id  = ghost_id
        self._position  = GHOSTS_START_POSITIONS [ghost_id]
        self._direction = GHOSTS_START_DIRECTIONS[ghost_id]

    def update(self, dt, level, fright, maze, pacman):


        position_changed,  = self._update_position(dt, )
        raise NotImplementedError
            
    def _update_direction(self, maze, pacman):
        raise NotImplementedError

    def _update_position(self, dt, level, fright, maze):
        
        # Only use the dt which would allow to exactly reach edge of tile.
        # Return remaining dt.

        return position_changed, remaining_dt
        
        raise NotImplementedError



class Blinky(Ghost):

    def __init__(self):
        super().__init__(Ghost.BLINKY)

    def _update_direction(self, maze, pacman):
        pass