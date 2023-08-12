# -*- coding: utf-8 -*-

from abc import ABC
from math import floor, ceil

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
        # Using (floor + 1) and (ceil - 1) instead of ceil and floor respectively allows to deal with integers correctly.
        coord_val = getattr(self._position, coord_changing)
        if getattr(self._direction, coord_changing) < 0:
            max_distance = coord_val - ((ceil(coord_val * 2) - 1) / 2)
        else:
            max_distance = ((floor(coord_val * 2) + 1) / 2) - coord_val
        new_distance = min(max_distance, distance)
        residual_distance = distance - new_distance
        distance = new_distance

        # Calculate new position and check if movement will cause a collision. If so, clip instead of moving into wall.
        new_position = self._position + self._direction * distance
        is_stuck = True

        collision_point = new_position + (self._direction * 0.500000000001)
        
        if maze.tile_is_wall(new_position):
            new_position += self._direction * (-0.5)
        elif maze.tile_is_wall(collision_point):
            setattr(new_position, coord_changing, floor(getattr(new_position, coord_changing)) + 0.5)
        else:
            is_stuck = False

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

        # Calculate if at new position we are at a tile center or edge.
        offset_in_tile = getattr(new_position, coord_changing) % 1
        is_at_tile_center = offset_in_tile == 0.5
        is_at_tile_edge   = offset_in_tile == 0.0
        
        # If at tile edge, slightly push in correct direction to clearly be in one tile for subsequent calculations.
        if is_at_tile_edge:
            new_position      += 0.000000000001 * self._direction
            residual_distance -= 0.000000000001

        # Set new position.
        self._position = new_position

        return residual_distance, is_stuck, is_at_tile_center, is_at_tile_edge