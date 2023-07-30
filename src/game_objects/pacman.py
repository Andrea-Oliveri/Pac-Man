# -*- coding: utf-8 -*-

from enum import IntEnum

from src.utils import Vector2

from src.constants import (PACMAN_MOVE_SPEED_TILES,
                           PACMAN_START_TILE,
                           PacManStates)





class PacMan:

    def __init__(self):
        self._position  = Vector2(*PACMAN_START_TILE)
        self._direction = Vector2.LEFT
        self._state     = PacManStates.SPAWNING

        self._direction_input = None

        # -----------------------------------------
        # Placeholder to go from spawning to moving.
        # -----------------------------------------
        import pyglet
        def f(_):
            self._state = PacManStates.MOVING
        pyglet.clock.schedule_once(f, 1.5) 
        # -----------------------------------------

        # -----------------------------------------
        # DEBUG: collision.
        # -----------------------------------------
        def print_collision_debug(_):
            try:
                print(self.position, self.collision_point_1, self.collision_point_2)
            except:
                pass
        pyglet.clock.schedule_interval(print_collision_debug, 1)
        # -----------------------------------------


    def update(self, dt, maze):





        if self.state in (PacManStates.SPAWNING, PacManStates.DEAD):
            # Ignore any request to change direction.
            self._direction_input = None

            # Do nothing.
            return

        elif self.state in (PacManStates.MOVING, PacManStates.STUCK):
            # Try to change direction.
            self.update_direction(maze)

            # Try to move.
            is_stuck = self.update_position(dt, maze)

            # Update state based on if Pac-Man stuck or not.
            if is_stuck:
                self.state = PacManStates.STUCK
            else:
                self.state = PacManStates.MOVING




    def update_direction(self, maze):
        # Note that reversing direction is allowed in Pac-Man.

        new_direction = self._direction_input
        self._direction_input = None
        
        if new_direction is None or new_direction == self._direction:
            return

        # Check if turn allowed in that direction.
        if maze.tile_is_wall(self._position + new_direction):
            return
        
        self._direction = new_direction




    def update_position(self, dt, maze):

        new_position = self.position + self._direction * (PACMAN_MOVE_SPEED_TILES * dt)
        is_stuck = False

        # Check if movement will cause a collision. If so, clip instead of moving into wall.
        # Only allow movement if both corners of Pac-Man's collision box are not into wall.
        # This collision detection does not account for very high speeds, which could allow Pac-Man to pass through wall
        # (only final position is checked for a collision, not points in between).
        point_forwards    = self._position + (self._direction        * 0.5000001)
        collision_point_1 = point_forwards + (self._direction.swap() * 0.4999999)
        collision_point_2 = point_forwards - (self._direction.swap() * 0.4999999)


        # TODO: remove DEBUG
        self.collision_point_1 = collision_point_1
        self.collision_point_2 = collision_point_2


        if maze.tile_is_wall(collision_point_1) or maze.tile_is_wall(collision_point_2):
            match self._direction:
                case Vector2.LEFT | Vector2.RIGHT:
                    new_position.x = int(new_position.x) + 0.5
                case Vector2.UP   | Vector2.DOWN:
                    new_position.y = int(new_position.y) + 0.5

            is_stuck = True

        self._position = new_position
        return is_stuck



    # Defining properties for some private attributes.
    def _set_direction(self, direction):
        if direction not in (Vector2.LEFT, Vector2.RIGHT, Vector2.UP, Vector2.DOWN):
            raise ValueError('Invalid direction provided to Pacman._set_direction')

        # Setting a temporary variable holding the requested direction.
        # True direction will be set during next game tick only if appropriate.
        self._direction_input = direction

    def _set_state(self, state):
        if state not in PacManStates:
            raise ValueError('Invalid state provided to Pacman._set_state')

        self._state = state

    position  = property(lambda self: self._position)
    direction = property(lambda self: self._direction, _set_direction)
    state     = property(lambda self: self._state    , _set_state)
