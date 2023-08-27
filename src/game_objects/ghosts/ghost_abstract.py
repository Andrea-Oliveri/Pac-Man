# -*- coding: utf-8 -*-


from abc import ABC, abstractmethod

from src.game_objects.character import Character

from src.directions import Vector2
from src.constants import (GAME_ORIGINAL_UPDATES_INTERVAL,
                           GHOSTS_START_POSITIONS,
                           GHOSTS_START_DIRECTIONS,
                           GHOSTS_START_BEHAVIOUR,
                           GhostBehaviour,
                           GHOSTS_SPEED,
                           GHOSTS_FORBIDDEN_TURNING_UP_TILES,
                           GHOSTS_SCATTER_MODE_TARGET_TILES,
                           GHOSTS_EATEN_TARGET_TILE)





class GhostAbstract(Character, ABC):
    def __init__(self, name, prng):
        super().__init__(position  = GHOSTS_START_POSITIONS [name],
                         direction = GHOSTS_START_DIRECTIONS[name])

        self._name = name
        self._prng = prng
        self._direction_next      = None
        self._direction_next_next = None

        self._behaviour = GHOSTS_START_BEHAVIOUR[name]

        self._reverse_direction_signal = False

        # Variable capturing whether the last callback called was for the tile edge or tile center. 
        # Needed to ensure consistency with original game: ghost eyes change as soon as they enter a new tile, even if they have not made the turn yet.
        # Also needed to avoid oscillations in in-house behaviour.
        self._last_step_was_edge = False



    def update(self, level, fright, maze, pacman):
        # Update position and directions.
        self._update_position(level, fright, maze, pacman)

    def _just_exited_house(self):
        self._direction           = Vector2.LEFT
        self._direction_next      = Vector2.LEFT
        self._direction_next_next = Vector2.LEFT
    
    
    def _calculate_direction_at_tile_center(self, maze, pacman, direction_from_current_tile):
        target_tile = self._calculate_target_tile(pacman, maze)
        
        # Ghost has just entered a new tile. Hence it did not switch yet his current direction of travel with the
        # one calculated for this tile (switch will only happen once he reaches the center of the current tile). 
        current_tile = maze.get_tile_center(self._position)
        next_tile = current_tile + direction_from_current_tile

        # Direction is chosen so that euclidean distance between next next tile and target tile is minimized.
        # In case of equivalency, preference is in this order (from most preferred to least): up, left, down, right.
        min_distance   = float('inf')
        best_direction = None
        for direction in (Vector2.UP, Vector2.LEFT, Vector2.DOWN, Vector2.RIGHT):
            # Ghosts are not allowed to willingly flip direction.
            if direction == -direction_from_current_tile:
                continue

            # Ghosts are not allowed to turn upwards on certain tiles when in chase or frightened mode.
            if next_tile in GHOSTS_FORBIDDEN_TURNING_UP_TILES and direction == Vector2.UP:
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


    def _calculate_target_tile(self, pacman, maze):
        
        if GhostBehaviour.CHASE in self._behaviour:
            return self._calculate_personal_target_tile(pacman, maze)

        elif GhostBehaviour.SCATTER in self._behaviour:
            return GHOSTS_SCATTER_MODE_TARGET_TILES[self._name]

        raise RuntimeError("GhostAbtract._calculate_target_tile was called with invalid behaviour: {self._behaviour.name}")


    def _update_position(self, level, fright, maze, pacman):
        
        dt = GAME_ORIGINAL_UPDATES_INTERVAL            

        while True:
            # Distance that can still be travelled depends on the tile (whether in warp tunnel or not).
            in_warp_tunnel = maze.tile_is_warp_tunnel(self._position)
            in_or_exiting_house = (GhostBehaviour.IN_HOUSE in self._behaviour) or (GhostBehaviour.EXITING_HOUSE in self._behaviour)
            speed = GHOSTS_SPEED(level, fright, in_warp_tunnel, in_or_exiting_house)
            residual_distance = speed * dt
            
            # Update position clipping to closest half-tile.
            residual_distance, _, is_at_tile_center, is_at_tile_edge = super()._update_position_within_tile(residual_distance, maze)

            # Update direction attributes based on behaviours.
            if is_at_tile_center:
                self._callback_is_at_tile_center()
                self._last_step_was_edge = False
            elif is_at_tile_edge:
                self._callback_is_at_tile_edge(maze, pacman)
                self._last_step_was_edge = True

            # Calculate residual dt not used by movement at this speed, if any.
            if residual_distance <= 0:
                break

            dt = residual_distance / speed


    def _callback_is_at_tile_edge(self, maze, pacman):

        if GhostBehaviour.IN_HOUSE in self._behaviour:
            if not self._last_step_was_edge:
                self._direction *= -1
                self._direction_next = self._direction
                self._direction_next_next = None

        elif GhostBehaviour.FRIGHTENED in self._behaviour:
            if self._reverse_direction_signal:
                self._reverse_direction_signal = False
                self._direction *= -1

                # We need to invalidate and future directions. Will be recalculated once we step back in the previous tile (next iteration).
                self._direction_next = None
                self._direction_next_next = None 
                
            else:
                self._direction_next = self._frightened_ghost_random_direction(maze)
                self._direction_next_next = self._calculate_direction_at_tile_center(maze, pacman, self._direction_next)
        
        elif any(behaviour in self._behaviour for behaviour in (GhostBehaviour.CHASE, GhostBehaviour.SCATTER)):

            if self._reverse_direction_signal:
                self._reverse_direction_signal = False
                self._direction *= -1

                # We need to invalidate and recalculate the direction of the next tile.
                self._direction_next = self._calculate_direction_at_tile_center(maze, pacman, self._direction)

                # This will be recalculated once we step back in the previous tile (next iteration).
                self._direction_next_next = None
            else:
                # When entering new tile, ghost must decide what it will do in next tile along this direction.
                self._direction_next_next = self._calculate_direction_at_tile_center(maze, pacman, self._direction_next)
            
                      


    def _frightened_ghost_random_direction(self, maze):
        current_tile = maze.get_tile_center(self._position)
        directions_clockwise = [Vector2.UP, Vector2.RIGHT, Vector2.DOWN, Vector2.LEFT]

        direction = self._prng.get_random_direction()
        starting_idx = directions_clockwise.index(direction)

        for offset in range(0, len(directions_clockwise)):
            direction =  directions_clockwise[(starting_idx + offset) % len(directions_clockwise)]
            next_tile = current_tile + direction

            if not maze.tile_is_wall(next_tile) and direction != -self._direction:
                return direction

        raise RuntimeError("No valid direction found in GhostAbstract._frightened_ghost_random_direction")



    def _callback_is_at_tile_center(self):
        
        if GhostBehaviour.IN_HOUSE in self._behaviour:
            return

        elif any(behaviour in self._behaviour for behaviour in (GhostBehaviour.CHASE, GhostBehaviour.SCATTER, GhostBehaviour.FRIGHTENED)):
            self._direction           = self._direction_next
            self._direction_next      = self._direction_next_next
            self._direction_next_next = None




    def add_behaviour(self, behaviour):
        if behaviour not in GhostBehaviour:
            raise ValueError('Invalid behaviour provided to Ghost.add_behaviour')

        # Ignore calls in excess, but still force direction if frightened and already frightened.
        if behaviour in self._behaviour and behaviour != GhostBehaviour.FRIGHTENED:
            return

        match behaviour:
            case GhostBehaviour.CHASE | GhostBehaviour.SCATTER:
                self._behaviour = self._behaviour & (~GhostBehaviour.CHASE) & (~GhostBehaviour.SCATTER) | behaviour
                self._reverse_direction_signal = True

            case GhostBehaviour.FRIGHTENED:
                self._behaviour = self._behaviour | GhostBehaviour.FRIGHTENED
                self._reverse_direction_signal = True

            case GhostBehaviour.IN_HOUSE | GhostBehaviour.EXITING_HOUSE | GhostBehaviour.GOING_TO_HOUSE:
                self._behaviour = self._behaviour & (~GhostBehaviour.IN_HOUSE) & (~GhostBehaviour.EXITING_HOUSE) & (~GhostBehaviour.GOING_TO_HOUSE) | behaviour


    def clear_fright(self):
        self._behaviour &= (~GhostBehaviour.FRIGHTENED)


    # Defining properties for some private attributes.
    position    = property(lambda self: self._position)
    frightened  = property(lambda self: GhostBehaviour.FRIGHTENED in self._behaviour)
    transparent = property(lambda self: GhostBehaviour.GOING_TO_HOUSE in self._behaviour)
    eyes_direction = property(lambda self: self._direction_next if self._last_step_was_edge else self._direction)
