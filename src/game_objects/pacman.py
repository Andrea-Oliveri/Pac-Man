# -*- coding: utf-8 -*-

from enum import IntEnum

from src.directions import Vector2

from src.constants import (PACMAN_SPEED,
                           PACMAN_START_TILE,
                           PacManStates,
                           PACMAN_PELLET_PENALTIES,
                           MAZE_TILES_COLS,
                           WARP_TUNNEL_TELEPORT_MARGIN)





class PacMan:

    def __init__(self):
        self._position  = Vector2(*PACMAN_START_TILE)
        self._direction = Vector2.LEFT
        self._state     = PacManStates.SPAWNING
        self._penalty   = 0

        self._direction_input = None

        # -----------------------------------------
        # TODO: Remove placeholder to go from spawning to moving.
        # -----------------------------------------
        import pyglet
        def f(_):
            self._state = PacManStates.MOVING
        pyglet.clock.schedule_once(f, 1.5) 
        def f2(_):
            self._state = PacManStates.DEAD
        #pyglet.clock.schedule_once(f2, 4.5) 
        # -----------------------------------------



    def update(self, dt, level, fright, maze):

        if self._state in (PacManStates.SPAWNING, PacManStates.DEAD):
            # Ignore any request to change direction.
            self._direction_input = None

            # Do nothing.
            return

        elif self._state in (PacManStates.MOVING, PacManStates.STUCK, PacManStates.TURNING):
            # Pac-Man is not allowed to change direction if he is already turning.
            if self._state == PacManStates.TURNING:
                self._direction_input = None
            else:
                # Try to change direction.
                turning = self.update_direction(maze)

                # Update state based on if Pac-Man turns or not.
                if turning:
                    self._state = PacManStates.TURNING
            
            # Try to move.
            is_stuck, turning = self.update_position(dt, level, fright, maze)

            # Update state based on if Pac-Man stuck or not, only if not still turning.
            if not turning:
                if is_stuck:
                    self._state = PacManStates.STUCK
                else:
                    self._state = PacManStates.MOVING
            

    def update_direction(self, maze):
        # Note that reversing direction is allowed in Pac-Man.

        # If nothing to do, reset and return.
        if self._direction_input is None or self._direction_input == self._direction:
            self._direction_input = None
            return False

        # If turn allowed in that direction, do it.
        if not maze.tile_is_wall(self._position + self._direction_input):
            self._direction       = self._direction_input
            self._direction_input = None
            return True

        # If turn will be allowed soon (one-cell forwards), allow anticipating it.
        if maze.tile_is_wall(self._position + self._direction + self._direction_input):
            self._direction_input = None

        return False


    def add_penalty(self, pellet_type):
        self._penalty += PACMAN_PELLET_PENALTIES[pellet_type]


    def update_position(self, dt, level, fright, maze):

        
        # Update penalty to movement speed.
        if self._penalty >= dt:
            self._penalty -= dt
            return self._state == PacManStates.STUCK, self._state == PacManStates.TURNING # No change in state
        
        dt -= self._penalty
        self._penalty = 0

        # Calculate how far Pac-Man has theoretically moved.
        distance = PACMAN_SPEED(level, fright) * dt

        # When turning, specific movement logic needed to bring Pac-Man back to center of corridor.
        # No collision detection because this was already checked by PacMan.update_direction method.
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


        # Calculate new position and check if movement will cause a collision. If so, clip instead of moving into wall.
        # Only allow movement if both corners of Pac-Man's collision box are not into wall.
        # This collision detection does not account for high speeds or large dt, which could allow Pac-Man to pass through wall
        # (only final position is checked for a collision, not points in between).
        new_position = self._position + self._direction * distance
        is_stuck = False

        collision_point = self._position + (self._direction * 0.5000001)

        # TODO: remove DEBUG
        self.collision_point = collision_point


        if maze.tile_is_wall(collision_point):
            match self._direction:
                case Vector2.LEFT | Vector2.RIGHT:
                    coord_to_clip = 'x'
                case Vector2.UP   | Vector2.DOWN:
                    coord_to_clip = 'y'

            setattr(new_position, coord_to_clip, int(getattr(new_position, coord_to_clip)) + 0.5)
            is_stuck = True

        # Perform warping if needed.
        if maze.tile_is_warp_tunnel(new_position):
            right_warp_edge = MAZE_TILES_COLS + WARP_TUNNEL_TELEPORT_MARGIN
            left_warp_edge  = -WARP_TUNNEL_TELEPORT_MARGIN

            if new_position.x > right_warp_edge:
                offset = new_position.x - right_warp_edge
                new_position.x = left_warp_edge + offset
            elif new_position.x < left_warp_edge:
                offset = left_warp_edge - new_position.x
                new_position.x = right_warp_edge - offset


        self._position = new_position
        return is_stuck, False # If he wasn't turning, he is not turning due to this function.



    # Defining properties for some private attributes.
    def _set_direction(self, direction):
        if direction not in (Vector2.LEFT, Vector2.RIGHT, Vector2.UP, Vector2.DOWN):
            raise ValueError('Invalid direction provided to Pacman._set_direction')

        # Setting a temporary variable holding the requested direction.
        # True direction will be set during next game tick only if appropriate.
        self._direction_input = direction


    position  = property(lambda self: self._position)
    direction = property(lambda self: self._direction, _set_direction)
    state     = property(lambda self: self._state)
