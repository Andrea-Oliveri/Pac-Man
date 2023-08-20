# -*- coding: utf-8 -*-

from src.game_objects.ghosts.ghost_personalities import (Blinky,
                                                         Pinky,
                                                         Inky,
                                                         Clyde)

from src.constants import (Ghost,
                           SCATTER_CHASE_ALTERNATIONS)


class GhostsCoordinator:

    def __init__(self):
        self._mode_timer = 0

        self._ghosts = {Ghost.BLINKY: Blinky(), Ghost.PINKY: Pinky(), Ghost.INKY: Inky(), Ghost.CLYDE: Clyde()}


    def _update_mode(self, level, fright):
        
        # If fright is on, we can't change mode and must not update timer. 
        if fright:
            return

        # Update timer.
        self._mode_timer += 1

        # Calculate current mode based on timer value.
        mode_durations = SCATTER_CHASE_ALTERNATIONS(level)
        
        cumtime = 0
        for mode, duration in mode_durations:
            cumtime += duration

            if self._mode_timer <= cumtime:
                self._set_behaviour(mode)
                return

        raise RuntimeError('Reached end of GhostCoordinator._update_mode without finding a behaviour for current timer')

    def _set_behaviour(self, behaviour):
        print(behaviour.name)
        print(self._ghosts[Ghost.BLINKY].behaviour)
        print(self._ghosts[Ghost.BLINKY]._reverse_direction_signal)

        for ghost in self._ghosts.values():
            ghost.behaviour = behaviour

    def update(self, level, fright, maze, pacman):
        self._update_mode(level, fright)
        
        # Update all ghosts.
        for ghost in self._ghosts.values():
            ghost.update(level, fright, maze, pacman)

    def check_collision(self, maze, pacman_position):
        pacman_tile = maze.get_tile_center(pacman_position)

        for ghost in self._ghosts.values():
            ghost_tile = maze.get_tile_center(ghost.position)
            if pacman_tile == ghost_tile:
                return True

        return False

    def notify_fright_on(self):
        # TODO
        pass

    def __iter__(self):
        return iter(self._ghosts.items())