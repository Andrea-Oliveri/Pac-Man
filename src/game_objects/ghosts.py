# -*- coding: utf-8 -*-


from abc import ABC, abstractmethod

from src.game_objects.character import Character

from src.directions import Vector2
from src.constants import (Ghost,
                           GHOSTS_START_POSITIONS,
                           GHOSTS_START_DIRECTIONS,
                           GhostBehaviour,
                           GHOSTS_SPEED)


class GhostsCoordinator:

    def __init__(self):
        pass




class Ghost(Character, ABC):
    def __init__(self, name):
        self._name      = name
        self._position  = GHOSTS_START_POSITIONS [name]

        self._direction = GHOSTS_START_DIRECTIONS[name]
        self._direction_next      = None
        self._direction_next_next = None

        self._behaviour = GhostBehaviour.CHASE

        self._reverse_direction_signal = False



    def update(self, dt, level, fright, maze, pacman):
        self._update_position(dt, level, fright, maze, pacman)
        

    def _set_behaviour(self, behaviour):
        if behaviour not in GhostBehaviour:
            raise ValueError('Invalid behaviour provided to Ghost._set_behaviour')

        if self._behaviour != GhostBehaviour.FRIGHTENED:
            self._reverse_direction_signal = True

        self._behaviour = behaviour


    def _update_direction(self, maze, pacman, is_at_tile_center,is_at_tile_edge):
        
        if is_at_tile_center:
            self._direction           = self._direction_next
            self._direction_next      = self._direction_next_next
            self._direction_next_next = None
        elif is_at_tile_edge:
            if self._reverse_direction_signal:
                self._reverse_direction_signal = False
                self._direction *= -1

                # We need to invalidate and recalculate the direction of the next tile.
                self._direction_next = self._calculate_direction_at_next_tile_center(maze, pacman)

                # This will be recalculated once we step back in the previous tile (next iteration).
                self._direction_next_next = None
            else:
                # When entering new tile, ghost must decide what it will do in next tile along this direction.
                self._direction_next_next = self._calculate_direction_at_next_tile_center(maze, pacman)

        
    

    
    def _calculate_direction_at_next_tile_center(self, maze, pacman):
        target_tile = self._calculate_target_tile(pacman, maze)
        
        next_tile = maze.get_tile_center(self._position + self._direction)

        # Direction is chosen so that euclidean distance between next next tile and target tile is minimized.
        min_distance   = float('inf')
        best_direction = None
        for direction in (Vector2.LEFT, Vector2.RIGHT, Vector2.UP, Vector2.DOWN):
            # Ghosts are not allowed to willingly flip direction.
            if direction == -self._direction:
                continue

            next_next_tile = tile_center + direction

            # Ghosts can't go in a wall.
            if maze.is_wall(next_next_tile):
                continue

            distance = Vector2.distance_squared(target_tile, next_next_tile)
            
            if distance < min_distance:
                distance = min_distance
                best_direction = direction

        return direction


    @abstractmethod
    def _calculate_target_tile(self, pacman, maze):
        return



    def _update_position(self, dt, level, fright, maze, pacman):
        
        while True:
            # Distance that can still be travelled depends on the tile (whether in warp tunnel or not).
            in_warp_tunnel = maze.tile_is_warp_tunnel(self._position)
            speed = GHOSTS_SPEED(level, fright, in_warp_tunnel)
            residual_distance = speed * dt
            
            # Update position clipping to closest half-tile.
            residual_distance, _, is_at_tile_center, is_at_tile_edge = super()._update_position_within_tile(residual_distance, maze)

            # Calculate residual dt not used by movement at this speed.
            dt = residual_distance / speed

            self._update_direction(maze, pacman, is_at_tile_center, is_at_tile_edge)

            if residual_distance <= 0:
                break


class Blinky(Ghost):

    def __init__(self):
        super().__init__(Ghost.BLINKY)


    def _calculate_target_tile(self, pacman, maze):
        # Blinky always targets the tile Pac-Man is on.
        pacman_tile = maze.get_tile_center(pacman.position)
        return pacman_tile