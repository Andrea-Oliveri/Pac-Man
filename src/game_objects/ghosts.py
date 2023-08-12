# -*- coding: utf-8 -*-


from abc import ABC, abstractmethod
from typing import Self

from src.game_objects.character import Character

from src.directions import Vector2
from src.constants import (Ghost,
                           GHOSTS_START_POSITIONS,
                           GHOSTS_START_DIRECTIONS,
                           GhostBehaviour,
                           GHOSTS_SPEED)


class GhostsCoordinator:

    def __init__(self):
        self._ghosts = {Ghost.BLINKY: Blinky(), Ghost.PINKY: Pinky(), Ghost.INKY: Inky(), Ghost.CLYDE: Clyde()}


    def update(self, dt, level, fright, maze, pacman):
        for ghost in self._ghosts.values():
            ghost.update(dt, level, fright, maze, pacman)

    def check_collision(self, maze, pacman_position):
        pacman_tile = maze.get_tile_center(pacman_position)

        for ghost in self._ghosts.values():
            ghost_tile = maze.get_tile_center(ghost.position)
            if pacman_tile == ghost_tile:
                return True

        return False

    def __iter__(self):
        return iter(self._ghosts.items())
 




class GhostClass(Character, ABC):
    def __init__(self, name):
        super().__init__(position  = GHOSTS_START_POSITIONS [name],
                         direction = GHOSTS_START_DIRECTIONS[name])

        self._name = name
        self._direction_next      = None
        self._direction_next_next = None

        self._behaviour = GhostBehaviour.CHASE

        self._reverse_direction_signal = False


    def update(self, dt, level, fright, maze, pacman):
        self._update_position(dt, level, fright, maze, pacman)

        self.is_at_tile_center = self.is_at_tile_center if hasattr(self, 'is_at_tile_center') else None
        self.is_at_tile_edge   = self.is_at_tile_edge   if hasattr(self, 'is_at_tile_edge') else None

        print(self._position, self._direction, self._direction_next, self._direction_next_next, self.is_at_tile_center, self.is_at_tile_edge)


    def _just_exited_pen(self):
        self._direction           = Vector2.LEFT
        self._direction_next      = Vector2.LEFT
        self._direction_next_next = Vector2.LEFT


    def _update_direction(self, maze, pacman, is_at_tile_center, is_at_tile_edge):
        
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
        
        # Ghost has just entered a new tile. Hence it did not switch yet his current direction of travel with the
        # one calculated for this tile (switch will only happen once he reaches the center of the current tile). 
        current_tile = maze.get_tile_center(self._position)
        next_tile = current_tile + self._direction_next


        # ---------------
        # DEBUG
        # ---------------
        if maze.get_tile_center(self._position + self._direction_next) != next_tile:
            print('PROBLEM:')
            print(maze.get_tile_center(self._position + self._direction_next), next_tile)
        # ---------------



        # Direction is chosen so that euclidean distance between next next tile and target tile is minimized.
        # In case of equivalency, preference is in this order (from most preferred to least): up, left, down, right.
        min_distance   = float('inf')
        best_direction = None
        for direction in (Vector2.UP, Vector2.LEFT, Vector2.DOWN, Vector2.RIGHT):
            # Ghosts are not allowed to willingly flip direction.
            if direction == self._direction_next * (-1):
                continue

            next_next_tile = next_tile + direction

            # Ghosts can't go in a wall.
            if maze.tile_is_wall(next_next_tile):
                continue

            distance = Vector2.distance_squared(target_tile, next_next_tile)

            if distance < min_distance:
                min_distance = distance
                best_direction = direction

        return best_direction


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

            # Update direction attributes.
            self._update_direction(maze, pacman, is_at_tile_center, is_at_tile_edge)

            # Calculate residual dt not used by movement at this speed, if any.
            if residual_distance <= 0:
                break

            dt = residual_distance / speed


    # Defining properties for some private attributes.
    def _set_behaviour(self, behaviour):
        if behaviour not in GhostBehaviour:
            raise ValueError('Invalid behaviour provided to Ghost._set_behaviour')

        if self._behaviour != GhostBehaviour.FRIGHTENED:
            self._reverse_direction_signal = True

        self._behaviour = behaviour

    position = property(lambda self: self._position)
    


class Blinky(GhostClass):

    def __init__(self):
        super().__init__(Ghost.BLINKY)
        self._just_exited_pen()

    def _calculate_target_tile(self, pacman, maze):
        # Blinky always targets the tile Pac-Man is on.
        pacman_tile = maze.get_tile_center(pacman.position)
        return pacman_tile


class Pinky(GhostClass):

    def __init__(self):
        super().__init__(Ghost.PINKY)

        
    def update(*args, **kwargs):
        return

    def _calculate_target_tile(self, pacman, maze):
        pass


class Inky(GhostClass):

    def __init__(self):
        super().__init__(Ghost.INKY)

    def update(*args, **kwargs):
        return

    def _calculate_target_tile(self, pacman, maze):
        pass


class Clyde(GhostClass):

    def __init__(self):
        super().__init__(Ghost.CLYDE)

    def update(*args, **kwargs):
        return

    def _calculate_target_tile(self, pacman, maze):
        pass