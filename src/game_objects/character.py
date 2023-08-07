# -*- coding: utf-8 -*-

from abc import ABC
from math import floor

from src.directions import Vector2
from src.constants import (MAZE_TILES_COLS,
                           WARP_TUNNEL_TELEPORT_MARGIN)


class Character(ABC):

    def __init__(self, position, direction):
        self._position  = position
        self._direction = direction


    def _update_position_within_tile(self, distance, maze):
        
        # Find coordinate along which we are travelling.
        match self._direction:
            case Vector2.LEFT | Vector2.RIGHT:
                coord_changing = 'x'
            case Vector2.UP   | Vector2.DOWN:
                coord_changing = 'y'

        # Clip distance so that it won't leave half-tile.
        coord_val = getattr(self._position, coord_changing)
        is_in_lower_half_tile = (coord_val % 1) <= 0.5
        is_increasing_in_tile = None
        match self._direction:
            case Vector2.LEFT  | Vector2.UP:
                max_distance = coord_val - (floor(coord_val * 2) / 2) + 0.0000001
                is_increasing_within_tile = False
            case Vector2.RIGHT | Vector2.DOWN:
                max_distance = (floor(coord_val * 2) / 2) - coord_val + 0.5000001
                is_increasing_within_tile = True
        new_distance = min(max_distance, distance)
        residual_distance = distance - new_distance
        distance = new_distance
        is_at_tile_center = (new_distance == max_distance) and ((is_in_lower_half_tile and is_increasing_in_tile) or (not is_in_lower_half_tile and not is_increasing_in_tile))
        is_at_tile_edge   = (new_distance == max_distance) and ((is_in_lower_half_tile and not is_increasing_in_tile) or (not is_in_lower_half_tile and is_increasing_in_tile))


        # Calculate new position and check if movement will cause a collision. If so, clip instead of moving into wall.
        new_position = self._position + self._direction * distance
        is_stuck = False

        collision_point = new_position + (self._direction * 0.5000001)

        # TODO: remove DEBUG
        self.collision_point = collision_point


        if maze.tile_is_wall(collision_point):
            setattr(new_position, coord_changing, floor(getattr(new_position, coord_changing)) + 0.5)
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
        
        return residual_distance, is_stuck, is_at_tile_center, is_at_tile_edge