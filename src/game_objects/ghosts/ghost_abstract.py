# -*- coding: utf-8 -*-


from abc import ABC, abstractmethod

from src.game_objects.character import Character

from src.directions import Vector2
from src.constants import (Ghost,
                           GAME_ORIGINAL_UPDATES_INTERVAL,
                           GHOSTS_START_POSITIONS,
                           GHOSTS_START_DIRECTIONS,
                           GHOSTS_START_BEHAVIOUR,
                           GhostBehaviour,
                           CruiseElroyLevel,
                           GHOSTS_SPEED,
                           GHOSTS_FORBIDDEN_TURNING_UP_TILES,
                           GHOSTS_SCATTER_MODE_TARGET_TILES,
                           GHOSTS_EATEN_TARGET_TILE,
                           GHOSTS_EATEN_TARGET_Y_IN_HOUSE)





class GhostAbstract(Character, ABC):
    def __init__(self, name, prng):
        super().__init__(position  = GHOSTS_START_POSITIONS [name],
                         direction = GHOSTS_START_DIRECTIONS[name])

        self._name = name
        self._prng = prng
        self._direction_next      = None
        self._direction_next_next = None
        self._scatter_mode_target_tile = GHOSTS_SCATTER_MODE_TARGET_TILES[name]

        self._behaviour = GHOSTS_START_BEHAVIOUR[name]

        self._reverse_direction_signal = False

        # Variable capturing whether the last callback called was for the tile edge or tile center. 
        # Needed to ensure consistency with original game: ghost eyes change as soon as they enter a new tile, even if they have not made the turn yet.
        # Also needed to avoid oscillations in in-house behaviour.
        self._going_from_tile_edge_to_center = False

        self._cruise_elroy_level = CruiseElroyLevel.NULL

        self._was_just_eaten = False


    def update(self, level, fright, maze, pacman, clyde_in_house, died_this_level):

        dt = GAME_ORIGINAL_UPDATES_INTERVAL

        while dt > 0:
            # Distance that can still be travelled depends on the tile (whether in warp tunnel or not).
            in_warp_tunnel = maze.tile_is_warp_tunnel(self._position)
            going_to_house = GhostBehaviour.GOING_TO_HOUSE in self._behaviour
            in_or_exiting_house = (GhostBehaviour.IN_HOUSE in self._behaviour) or (GhostBehaviour.EXITING_HOUSE in self._behaviour)
            self._update_cruise_elroy_level(level, maze.n_pellets_remaining, clyde_in_house, died_this_level)
            speed = GHOSTS_SPEED(level, fright, in_warp_tunnel, going_to_house, in_or_exiting_house, self._cruise_elroy_level)
            residual_distance = speed * dt
            
            # Update position clipping to closest half-tile.
            collide_with_door = (GhostBehaviour.EXITING_HOUSE not in self._behaviour) and (GhostBehaviour.ENTERING_HOUSE not in self._behaviour)
            residual_distance, _, is_at_tile_center, is_at_tile_edge = super()._update_position_within_tile(residual_distance, maze, collide_with_door)

            # Update direction attributes based on behaviours.
            if GhostBehaviour.IN_HOUSE         in self._behaviour:
                self._behaviour_in_house         (is_at_tile_center, is_at_tile_edge, maze, pacman)
            elif GhostBehaviour.EXITING_HOUSE  in self._behaviour:
                self._behaviour_exiting_house    (is_at_tile_center, is_at_tile_edge, maze, pacman)
            elif GhostBehaviour.GOING_TO_HOUSE in self._behaviour:
                self._behaviour_going_to_house   (is_at_tile_center, is_at_tile_edge, maze, pacman)
            elif GhostBehaviour.ENTERING_HOUSE in self._behaviour:
                self._behaviour_entering_house   (is_at_tile_center, is_at_tile_edge, maze, pacman)
            elif GhostBehaviour.FRIGHTENED     in self._behaviour:
                self._behaviour_frightened       (is_at_tile_center, is_at_tile_edge, maze, pacman)
            elif GhostBehaviour.CHASE          in self._behaviour:
                self._behaviour_reach_target_tile(is_at_tile_center, is_at_tile_edge, maze, pacman)
            elif GhostBehaviour.SCATTER        in self._behaviour:
                self._behaviour_reach_target_tile(is_at_tile_center, is_at_tile_edge, maze, pacman)
                
            # Update variable describing whether going from edge to center of a tile.
            if is_at_tile_center:
                self._going_from_tile_edge_to_center = False
            elif is_at_tile_edge:
                self._going_from_tile_edge_to_center = True

            # Calculate residual dt not used by movement at this speed, if any.
            dt = residual_distance / speed


    def _behaviour_in_house(self, is_at_tile_center, is_at_tile_edge, maze, pacman):
        self._direction_next = self._direction_next_next = None

        # Switch direction, but only if not already switched to avoid oscillations.
        if is_at_tile_edge and not self._going_from_tile_edge_to_center:
            self._direction *= -1


    def _behaviour_exiting_house(self, is_at_tile_center, is_at_tile_edge, maze, pacman):
        self._direction_next = self._direction_next_next = None
        round_position = self._position.round_to_nearest_half()

        if round_position.x > GHOSTS_START_POSITIONS[Ghost.PINKY].x:
            self._direction = Vector2.LEFT
        elif round_position.x < GHOSTS_START_POSITIONS[Ghost.PINKY].x:
            self._direction = Vector2.RIGHT
        elif is_at_tile_edge:
            self._direction = Vector2.UP
        elif is_at_tile_center and round_position.y == GHOSTS_START_POSITIONS[Ghost.BLINKY].y:
            self._behaviour &= (~GhostBehaviour.EXITING_HOUSE)
                                
            self._direction           = Vector2.LEFT
            self._direction_next      = Vector2.LEFT
            self._direction_next_next = Vector2.LEFT


    def _behaviour_going_to_house(self, is_at_tile_center, is_at_tile_edge, maze, pacman):
        round_position = self._position.round_to_nearest_half()

        if round_position == GHOSTS_START_POSITIONS[Ghost.BLINKY] and is_at_tile_edge:
            self._add_behaviour(GhostBehaviour.ENTERING_HOUSE)

            self._direction           = Vector2.DOWN
            self._direction_next      = None
            self._direction_next_next = None

        else:
            self._behaviour_reach_target_tile(is_at_tile_center, is_at_tile_edge, maze, pacman)
            

    def _behaviour_entering_house(self, is_at_tile_center, is_at_tile_edge, maze, pacman):
        self._direction_next = self._direction_next_next = None
        round_position = self._position.round_to_nearest_half()

        if not is_at_tile_edge or round_position.y != GHOSTS_EATEN_TARGET_Y_IN_HOUSE:
            return

        match self._name:
            case Ghost.BLINKY | Ghost.PINKY:
                self._add_behaviour(GhostBehaviour.EXITING_HOUSE)
                self._direction = Vector2.UP
            case Ghost.INKY: 
                self._direction = Vector2.LEFT
            case Ghost.CLYDE:
                self._direction = Vector2.RIGHT

        if is_at_tile_edge and round_position.x == GHOSTS_START_POSITIONS[self._name].x:
           self._add_behaviour(GhostBehaviour.EXITING_HOUSE)


    def _behaviour_frightened(self, is_at_tile_center, is_at_tile_edge, maze, pacman):
        if is_at_tile_center:
            self._direction           = self._direction_next
            self._direction_next      = self._direction_next_next
            self._direction_next_next = None

        elif is_at_tile_edge:
            if self._maybe_reverse_direction():
                pass                
            else:
                self._direction_next = self._frightened_ghost_random_direction(maze)
                self._direction_next_next = None


    def _behaviour_reach_target_tile(self, is_at_tile_center, is_at_tile_edge, maze, pacman):
        
        # Sanitize _direction_next and _direction_next_next if they had been invalidated.
        # This only happens when fright is cleared (due to it ending or being eaten), as all other transitions set all directions before leaving.
        if self._direction_next is None:
            if is_at_tile_center:
                self._direction_next      = self._calculate_direction_at_tile_center(maze, pacman, Vector2.ZERO)
                self._direction_next_next = self._calculate_direction_at_tile_center(maze, pacman, self._direction_next)
            elif is_at_tile_edge:
                if not self._reverse_direction_signal:
                    self._direction_next  = self._calculate_direction_at_tile_center(maze, pacman, Vector2.ZERO)
                # If reverse signal is True, then the regular function behaviour will recalculate _direction_next.
            else:
                if self._going_from_tile_edge_to_center:
                    self._direction_next      = self._calculate_direction_at_tile_center(maze, pacman, Vector2.ZERO)
                    self._direction_next_next = self._calculate_direction_at_tile_center(maze, pacman, self._direction_next)
                elif not self._reverse_direction_signal:
                    self._direction_next      = self._calculate_direction_at_tile_center(maze, pacman, self._direction)
                # If reverse signal is True, then the regular function behaviour will recalculate _direction_next.


        if is_at_tile_center:
            self._direction           = self._direction_next
            self._direction_next      = self._direction_next_next
            self._direction_next_next = None

        elif is_at_tile_edge:
            if self._maybe_reverse_direction():
                self._direction_next = self._calculate_direction_at_tile_center(maze, pacman, self._direction)
                # _direction_next_next will be recalculated once we step back in the previous tile (next iteration).
            else:
                # When entering new tile, ghost must decide what it will do in next tile along this direction.
                self._direction_next_next = self._calculate_direction_at_tile_center(maze, pacman, self._direction_next)  


    def _maybe_reverse_direction(self):
        retval = self._reverse_direction_signal

        if retval:
            self._reverse_direction_signal = False
            self._direction *= -1

            # Invalidate the future directions.
            self._direction_next = None
            self._direction_next_next = None

        return retval


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

            # Ghosts are not allowed to turn upwards on certain tiles when in chase or scatter mode.
            # They can, however, when returning to house (and in frightened mode).
            if next_tile in GHOSTS_FORBIDDEN_TURNING_UP_TILES and direction == Vector2.UP and GhostBehaviour.GOING_TO_HOUSE not in self._behaviour:
                continue

            next_next_tile = next_tile + direction

            # Ghosts can't go in a wall.
            if maze.tile_is_not_walkable(next_next_tile):
                continue

            distance = Vector2.distance_squared(target_tile, next_next_tile)

            if distance < min_distance:
                min_distance = distance
                best_direction = direction

        return best_direction


    def _calculate_target_tile(self, pacman, maze):
        
        if GhostBehaviour.GOING_TO_HOUSE in self._behaviour:
            return GHOSTS_EATEN_TARGET_TILE

        elif GhostBehaviour.CHASE in self._behaviour or self._cruise_elroy_level != CruiseElroyLevel.NULL:
            return self._calculate_personal_target_tile(pacman, maze)

        elif GhostBehaviour.SCATTER in self._behaviour:
            return self._scatter_mode_target_tile

        raise RuntimeError("GhostAbtract._calculate_target_tile was called with invalid behaviour: {self._behaviour.name}")


    def _frightened_ghost_random_direction(self, maze):
        current_tile = maze.get_tile_center(self._position)
        directions_clockwise = [Vector2.UP, Vector2.RIGHT, Vector2.DOWN, Vector2.LEFT]

        direction = self._prng.get_random_direction()
        starting_idx = directions_clockwise.index(direction)

        for offset in range(0, len(directions_clockwise)):
            direction =  directions_clockwise[(starting_idx + offset) % len(directions_clockwise)]
            next_tile = current_tile + direction

            if not maze.tile_is_not_walkable(next_tile) and direction != -self._direction:
                return direction

        raise RuntimeError("No valid direction found in GhostAbstract._frightened_ghost_random_direction")


    def _add_behaviour(self, behaviour):
        if behaviour not in GhostBehaviour:
            raise ValueError('Invalid behaviour provided to Ghost._add_behaviour')

        match behaviour:

            case GhostBehaviour.CHASE | GhostBehaviour.SCATTER:
                # Only reverse direction if actual switch between scatter and chase modes. Otherwise ignore.
                if behaviour in self._behaviour:
                    return

                self._behaviour = self._behaviour & (~GhostBehaviour.CHASE) & (~GhostBehaviour.SCATTER) | behaviour
                self._reverse_direction_signal = True

            case GhostBehaviour.FRIGHTENED:
                # Ghosts going to the house when power pellet eaten are not frightened once they reach it.
                if GhostBehaviour.GOING_TO_HOUSE not in self._behaviour:
                    self._behaviour |= GhostBehaviour.FRIGHTENED

                self._reverse_direction_signal = True

            case GhostBehaviour.IN_HOUSE | GhostBehaviour.EXITING_HOUSE | GhostBehaviour.GOING_TO_HOUSE | GhostBehaviour.ENTERING_HOUSE:
                self._behaviour = self._behaviour & (~GhostBehaviour.IN_HOUSE) \
                                                  & (~GhostBehaviour.EXITING_HOUSE) \
                                                  & (~GhostBehaviour.GOING_TO_HOUSE) \
                                                  & (~GhostBehaviour.ENTERING_HOUSE) \
                                                  | behaviour

    def request_behaviour(self, behaviour):
        if behaviour not in (GhostBehaviour.CHASE, GhostBehaviour.SCATTER, GhostBehaviour.FRIGHTENED, GhostBehaviour.EXITING_HOUSE):
            raise ValueError('Invalid behaviour provided to Ghost.request_behaviour')

        self._add_behaviour(behaviour)
        

    def clear_fright(self):
        self._behaviour &= (~GhostBehaviour.FRIGHTENED)


    def notify_was_just_eaten(self):
        self._add_behaviour(GhostBehaviour.GOING_TO_HOUSE)
        self.clear_fright()
        self._was_just_eaten = True

    def clear_was_just_eaten(self):
        self._was_just_eaten = False



    # Defining properties for some attributes.
    name           = property(lambda self: self._name)
    position       = property(lambda self: self._position)
    frightened     = property(lambda self: GhostBehaviour.FRIGHTENED in self._behaviour)
    transparent    = property(lambda self: GhostBehaviour.GOING_TO_HOUSE in self._behaviour or GhostBehaviour.ENTERING_HOUSE in self._behaviour)
    is_in_house    = property(lambda self: GhostBehaviour.IN_HOUSE in self._behaviour)
    eyes_direction = property(lambda self: self._direction_next if self._going_from_tile_edge_to_center and self._direction_next is not None else self._direction)
    was_just_eaten = property(lambda self: self._was_just_eaten)


    @abstractmethod
    def _calculate_personal_target_tile(self):
        raise NotImplementedError

    def _update_cruise_elroy_level(self, level, pellets_remaining, clyde_in_house, died_this_level):
        return
        