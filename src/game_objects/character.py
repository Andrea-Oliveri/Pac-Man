# -*- coding: utf-8 -*-

from src.directions import Vector2

from src.constants import (MAZE_TILES_COLS,
                           WARP_TUNNEL_TELEPORT_MARGIN)


class Character:

    def __init__(self, position, direction):
        self._position  = position
        self._direction = direction


    def _update_position(self, distance, maze):
        
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
        return is_stuck

