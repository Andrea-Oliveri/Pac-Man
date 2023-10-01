# -*- coding: utf-8 -*-

from src.game_objects.prng import PRNG
from src.game_objects.ghosts.ghost_personalities import (Blinky,
                                                         Pinky,
                                                         Inky,
                                                         Clyde)

from src.constants import (Ghost,
                           GhostBehaviour,
                           SCATTER_CHASE_ALTERNATIONS,
                           DOT_COUNTER_LIMIT,
                           DOT_GLOBAL_COUNTER_LIMIT,
                           DOTS_NOT_EATEN_TIMER_THR)


class GhostsCoordinator:

    def __init__(self):
        self._reset_new_life()

        # Variables needed to decide when ghosts leave house.
        self._dot_counter_ghosts = [0 for _ in Ghost]
        self._dot_counter_global = 0
        self._dot_counter_global_enable = False


    def _reset_new_life(self):
        self._mode_timer = 0
        self._prng = PRNG()

        self._time_since_dot_eaten = 0

        # Instanciate ghosts.
        blinky = Blinky(self._prng)
        self._ghosts = (blinky, Pinky(self._prng), Inky(self._prng, blinky), Clyde(self._prng))


    def __iter__(self):
        return iter(self._ghosts)


    def _update_movement_mode(self, level, fright):
        
        # If fright is on, we can't change mode and must not update timer. 
        if fright:
            return

        # If fright is off, remove it from all ghosts.
        self._clear_fright_from_all()

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

    def update(self, level, fright, maze, pacman):
        self._update_movement_mode(level, fright)
        self._time_since_dot_eaten += 1

        # Check if ghost needs to leave house.
        self._check_leave_house(level)

        # Update all ghosts.
        for ghost in self._ghosts:
            ghost.update(level, fright, maze, pacman)

    def notify_pellet_eaten(self):
        self._time_since_dot_eaten = 0

        if self._dot_counter_global_enable:
            self._dot_counter_global += 1
            return

        for name in Ghost.PINKY, Ghost.INKY, Ghost.CLYDE:
            ghost = self._ghosts[name]

            if ghost.is_in_house:
                self._dot_counter_ghosts[name] += 1
                return


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
            self._clear_fright_from_all()

    def notify_life_lost(self):
        self._reset_new_life()

        self._dot_counter_global = 0
        self._dot_counter_global_enable = True
        

    def _add_behaviour_to_all(self, behaviour):
        for ghost in self._ghosts:
            ghost.add_behaviour(behaviour)

    def _clear_fright_from_all(self):
        for ghost in self._ghosts:
            ghost.clear_fright()


    def _check_leave_house(self, level):
        for name in Ghost:
            ghost = self._ghosts[name]

            if not ghost.is_in_house:
                continue

            if self._time_since_dot_eaten >= DOTS_NOT_EATEN_TIMER_THR(level):
                self._time_since_dot_eaten = 0
                ghost.add_behaviour(GhostBehaviour.EXITING_HOUSE)
                continue

            if self._dot_counter_global_enable:
                if self._dot_counter_global == DOT_GLOBAL_COUNTER_LIMIT[name]:
                   ghost.add_behaviour(GhostBehaviour.EXITING_HOUSE)
                   self._dot_counter_global_enable = (name != Ghost.CLYDE)
                
                # If global dot counter enabled, don't perform the check with regular dot counters. 
                continue 

            if self._dot_counter_ghosts[name] >= DOT_COUNTER_LIMIT(name, level):
                ghost.add_behaviour(GhostBehaviour.EXITING_HOUSE)