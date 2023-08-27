# -*- coding: utf-8 -*-

from enum import IntEnum

from src.directions import Vector2
from src.game_objects.character import Character

from src.constants import (GAME_ORIGINAL_UPDATES_INTERVAL,
                           PACMAN_SPEED,
                           PACMAN_START_POSITION,
                           PacManStates,
                           PACMAN_PELLET_PENALTIES)





class PacMan(Character):

    def __init__(self):
        super().__init__(position  = PACMAN_START_POSITION,
                         direction = Vector2.LEFT)

        self._old_position = self._position
        self._state     = PacManStates.SPAWNING
        self._penalty   = 0

        self._direction_input = None



        # --------------------------------
        # TODO: implement proper swicthing
        # --------------------------------
        self._state = PacManStates.MOVING
        # --------------------------------
        



    def update(self, level, fright, maze):

        if self._state in (PacManStates.SPAWNING, PacManStates.DEAD):
            # Ignore any request to change direction.
            self._direction_input = None

            # Do nothing.
            return

        elif self._state in (PacManStates.MOVING, PacManStates.STUCK, PacManStates.TURNING):
            # Pac-Man is not allowed to change direction if he is already turning.
            if self._state != PacManStates.TURNING:
                # Try to change direction.
                turning = self._update_direction(maze)

                # Update state based on if Pac-Man turns or not.
                if turning:
                    self._state = PacManStates.TURNING
            
            # Try to move.
            is_stuck, turning = self._update_position(level, fright, maze)

            # Update state based on if Pac-Man stuck or not, only if not still turning.
            if not turning:
                if is_stuck:
                    self._state = PacManStates.STUCK
                else:
                    self._state = PacManStates.MOVING
            

    def _update_direction(self, maze):
        # Note that reversing direction is allowed in Pac-Man.

        # If nothing to do, reset and return.
        if self._direction_input is None or self._direction_input == self._direction:
            self._direction_input = None
            return False

        # If turn allowed in that direction, do it.
        if not maze.tile_is_not_walkable(self._position + self._direction_input):
            self._direction       = self._direction_input
            self._direction_input = None
            return True

        # If turn will be allowed soon (one-cell forwards), allow anticipating it.
        if maze.tile_is_not_walkable(self._position + self._direction + self._direction_input):
            self._direction_input = None

        return False


    def add_penalty(self, pellet_type):
        self._penalty += PACMAN_PELLET_PENALTIES[pellet_type]



    def _update_position(self, level, fright, maze):
        self._old_position = self._position
        
        # Update penalty to movement speed.
        if self._penalty > 0:
            self._penalty -= 1
            return self._state == PacManStates.STUCK, self._state == PacManStates.TURNING # No change in state
        
        # Calculate how far Pac-Man has theoretically moved.
        distance = PACMAN_SPEED(level, fright) * GAME_ORIGINAL_UPDATES_INTERVAL

        # When turning, specific movement logic needed to bring Pac-Man back to center of corridor.
        # No collision detection because this was already checked by PacMan._update_direction method.
        if self._state == PacManStates.TURNING:
            self._position += self._direction * distance

            match self._direction:
                case Vector2.LEFT | Vector2.RIGHT:
                    coord_to_move = 'y'
                case Vector2.UP   | Vector2.DOWN:
                    coord_to_move = 'x'

            desired_value_coord = int(getattr(self._position, coord_to_move)) + 0.5
            offset = desired_value_coord - getattr(self._position, coord_to_move)

            if abs(offset) <= distance:
                setattr(self._position, coord_to_move, desired_value_coord)
                return False, False # Not stuck, not turning anymore.

            if offset >= 0:
                new_value_coord = getattr(self._position, coord_to_move) + distance
            else:
                new_value_coord = getattr(self._position, coord_to_move) - distance

            setattr(self._position, coord_to_move, new_value_coord)
            return False, True # Not stuck, still turning.

        residual_distance = distance
        is_stuck = False
        while residual_distance > 0 and not is_stuck:
            residual_distance, is_stuck, _, _ = super()._update_position_within_tile(residual_distance, maze)

        return is_stuck, False # If he wasn't turning, he is not turning due to this function.



    # Defining properties for some private attributes.
    def _set_direction(self, direction):
        if direction not in (Vector2.LEFT, Vector2.RIGHT, Vector2.UP, Vector2.DOWN):
            raise ValueError('Invalid direction provided to Pacman._set_direction')

        # Setting a temporary variable holding the requested direction.
        # True direction will be set during next game tick only if appropriate.
        self._direction_input = direction


    position      = property(lambda self: self._position)
    old_position  = property(lambda self: self._old_position)
    direction     = property(lambda self: self._direction, _set_direction)
    state         = property(lambda self: self._state)
