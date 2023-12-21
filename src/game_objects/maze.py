# -*- coding: utf-8 -*-

from src.directions import Vector2
from src.constants import (MazeTiles,
                           MAZE_START_TILES,
                           MAZE_TILES_COLS,
                           MAZE_TILES_ROWS,
                           WARP_TUNNEL_ROW,
                           WARP_TUNNEL_COL_LEFT,
                           WARP_TUNNEL_COL_RIGHT,
                           MAZE_START_NUM_PELLET)


class Maze:
    """Class Maze. Class storing the current state of the maze.
    Coordinate system chosen: (0,0) is at the top left, first coordinate is row and
    second coordinate is column."""
    
    def __init__(self):
        """Constructor for the class Maze."""
        self._tiles = list(MAZE_START_TILES)
        self._n_pellets = MAZE_START_NUM_PELLET

        # Sanity check
        if len(self._tiles) != MAZE_TILES_ROWS * MAZE_TILES_COLS:
            raise RuntimeError('There is an error in the maze constants: lenght of initial tile array is not as expected.')


    def __getitem__(self, index):
        """Special function that allows to get items of attribute _tiles from the exterior."""
        index, row, col = self._index_convert(index)

        # If out of maze bounds, all tiles are walls except for warp tunnel.
        if index is None:
            return MazeTiles.EMPTY if row == WARP_TUNNEL_ROW else MazeTiles.WALL

        return self._tiles[index]

    @staticmethod
    def _index_convert(index):
        if isinstance(index, Vector2):
            # If a Vector2 instance, convert to tile coordinates by dividing tile size.
            row = int(index.y)
            col = int(index.x)
        elif isinstance(index, tuple) and len(index) == 2 and all(isinstance(elem, int) for elem in index):
            # If a 2-elements tuple of integers, interpret it as (row, col).
            row, col = index
        else:
            raise IndexError(f"Unsupported indexing value for class Maze: {index}")

        # If coordinates are outside boundaries, return None.
        if row < 0 or row >= MAZE_TILES_ROWS or col < 0 or col >= MAZE_TILES_COLS:
            index = None
        else:
            index = row * MAZE_TILES_COLS + col

        return index, row, col


    def tile_is_warp_tunnel(self, index):
        """Function that returns True if the tile at desired index is in the warp tunnel."""
        _, row, col = self._index_convert(index)

        return (row == WARP_TUNNEL_ROW) and (col <= WARP_TUNNEL_COL_LEFT or col >= WARP_TUNNEL_COL_RIGHT)


    def tile_is_not_walkable(self, index, collide_with_door = True):
        """Function that returns True if the tile at desired index is not walkable."""
        tile_type = self[index]
        return tile_type == MazeTiles.WALL or (tile_type == MazeTiles.DOOR and collide_with_door)
    

    @staticmethod
    def get_tile_center(index):
        _, row, col = Maze._index_convert(index)
        return Vector2(x = col + 0.5, y = row + 0.5)

    def eat_check_pellet(self, pacman_position):
        """Updates maze if needed by replacing a pellet with an empty tile. Returns the (row, col) coordinates of
        the tile in the array if such a replacement was performed and the type, None otherwise."""
        index, row, col = self._index_convert(pacman_position)
        tile = self[pacman_position]

        if tile in (MazeTiles.PELLET, MazeTiles.POWER_PELLET):
            self._tiles[index] = MazeTiles.EMPTY
            self._n_pellets -= 1
            return (row, col), tile
        
        return None, None
    

    n_pellets_remaining = property(lambda self: self._n_pellets)
    completed           = property(lambda self: self._n_pellets == 0)