# -*- coding: utf-8 -*-

from src.game_objects.prng import PRNG
from src.game_objects.ghosts.ghost_personalities import (Blinky,
                                                         Pinky,
                                                         Inky,
                                                         Clyde)

from src.constants import (Ghost,
                           GhostBehaviour,
                           SCATTER_CHASE_ALTERNATIONS)


class GhostsCoordinator:

    def __init__(self):
        self._mode_timer = 0
        self._prng = PRNG()

        # Variables needed to decide when ghosts leave house.
        self._dot_counter_ghosts = [0 for _ in Ghost]
        self._dot_counter_global = 0
        self._dot_counter_global_enable = False
        self._time_since_dot_eaten = 0

        # Instanciate ghosts.
        blinky = Blinky(self._prng)
        self._ghosts = (blinky, Pinky(self._prng), Inky(self._prng, blinky), Clyde(self._prng))

    def _update_movement_mode(self, level, fright):
        
        # If fright is on, we can't change mode and must not update timer. 
        if fright:
            return

        # If fright is off, remove it from all ghosts.
        for ghost in self._ghosts:
            ghost.clear_fright()

        # Update timer.
        self._mode_timer += 1

        # Calculate current mode based on timer value.
        mode_durations = SCATTER_CHASE_ALTERNATIONS(level)
        
        cumtime = 0
        for mode, duration in mode_durations:
            cumtime += duration

            if self._mode_timer <= cumtime:
                self._add_behaviour_to_all(mode)
                return

        raise RuntimeError('Reached end of GhostCoordinator._update_mode without finding a behaviour for current timer')

    def _add_behaviour_to_all(self, behaviour):
        for ghost in self._ghosts:
            ghost.add_behaviour(behaviour)

    def update(self, level, fright, maze, pacman):
        self._update_movement_mode(level, fright)
        self._time_since_dot_eaten += 1
        
        # Update all ghosts.
        for ghost in self._ghosts:
            ghost.update(level, fright, maze, pacman)

    def notify_pellet_eaten(self):
        self._time_since_dot_eaten = 0


    def check_collision(self, maze, pacman):
        pacman_tile = maze.get_tile_center(pacman.position)

        life_lost = False
        count_eaten = 0
        for ghost in self._ghosts:
            ghost_tile = maze.get_tile_center(ghost.position)

            if pacman_tile != ghost_tile:
                continue

            if ghost.frightened:
                ghost.notify_was_eaten(maze, pacman)
                count_eaten += 1
                continue
            
            life_lost = True

        return life_lost, count_eaten

    def notify_fright_on(self, fright_duration):
        self._add_behaviour_to_all(GhostBehaviour.FRIGHTENED)

        if fright_duration <= 0:
            for ghost in self._ghosts:
                ghost.clear_fright()

    def __iter__(self):
        return iter(self._ghosts)