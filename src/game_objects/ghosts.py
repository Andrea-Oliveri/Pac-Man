# -*- coding: utf-8 -*-


from src.directions import Vector2

from src.constants import (Ghost,
                           GHOSTS_START_POSITIONS,
                           GHOSTS_START_DIRECTIONS,
                           GhostBehaviour,
                           GHOSTS_SPEED)


class GhostsCoordinator:

    def __init__(self):
        pass




class Ghost:
    def __init__(self, name):
        self._name      = name
        self._position  = GHOSTS_START_POSITIONS [name]
        self._direction = GHOSTS_START_DIRECTIONS[name]
        self._upcoming_direction = None

        self._behaviour = GhostBehaviour.CHASE

        self._reverse_direction_signal = False



    def update(self, dt, level, fright, maze, pacman):
        # Update position only uses dt up to when tile edge is reached. Returns the rest.
        dt = self._update_position(dt, level, fright, maze)

        # If dt remaining, recalculate target, direction and update position.
        while dt > 0:
            self._update_directions(maze, pacman)
            dt = self._update_position(dt, level, fright, maze)
            

    def _set_behaviour(self, behaviour):
        if behaviour not in GhostBehaviour:
            raise ValueError('Invalid behaviour provided to Ghost._set_behaviour')

        if self._behaviour != GhostBehaviour.FRIGHTENED:
            self._reverse_direction_signal = True

        self._behaviour = behaviour


    def _update_directions(self, maze, pacman):

        # If in monster pen, custom logic that even ignores reverse direction signals.
        if maze.tile_is_ghost_house(self._position):
            pass

        if self._reverse_direction_signal:
            self._reverse_direction_signal = False
            self._direction *= -1
            self._calculate_upcoming_direction()
            return



        # TODO: Logic for frightened and (chase or scatter)
        if self._behaviour == GhostBehaviour.FRIGHTENED:
            pass
        else:
            distances = []
            for new_direction in (Vector2.LEFT, Vector2.RIGHT, Vector2.UP, Vector2.DOWN):
                # Ghosts are not allowed to flip direction (except when forced to).
                if new_direction == -self._direction:
                    continue



    def _calculate_upcoming_direction(self, upcoming_tile, pacman):
        raise NotImplementedError

    def _update_position(self, dt, level, fright, maze):
        
        in_warp_tunnel = maze.tile_is_warp_tunnel(self._position)
        speed = GHOSTS_SPEED(level, fright, in_warp_tunnel)


        # Calculate new position and check if movement will cause a collision. If so, clip instead of moving into wall.
        new_position = self._position + self._direction * distance
        is_stuck = False

        collision_point = new_position + (self._direction * 0.5000001)

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



        # Only use the dt which would allow to exactly reach edge of tile.
        # Return remaining dt.

        return remaining_dt
        
        raise NotImplementedError



class Blinky(Ghost):

    def __init__(self):
        super().__init__(Ghost.BLINKY)

    def _update_direction(self, maze, pacman):
        pass