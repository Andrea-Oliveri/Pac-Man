# -*- coding: utf-8 -*-

from src.utils import Vector2
from src.constants import (MazeTiles,
                           MAZE_START_TILES,
                           MAZE_TILES_COLS,
                           MAZE_TILES_ROWS)


class Maze:
    """Class Maze. Class storing the current state of the maze.
    Coordinate system chosen: (0,0) is at the top left, first coordinate is row and
    second coordinate is column."""
    
    def __init__(self):
        """Constructor for the class Maze."""
        self._tiles = list(MAZE_START_TILES)
        self._n_pellets = sum(elem in (MazeTiles.PELLET, MazeTiles.POWER_PELLET) for elem in self._tiles)

        # Sanity check
        if len(self._tiles) != MAZE_TILES_ROWS * MAZE_TILES_COLS:
            raise RuntimeError('There is an error in the maze constants: lenght of initial tile array is not as expected.')


    def __getitem__(self, index):
        """Special function that allows to get items of attribute _tiles from the exterior."""
        index = self._index_convert(index)

        return self._tiles[index]

    def _index_convert(self, index):
        if isinstance(index, Vector2):
            # If a Vector2 instance, convert to tile coordinates by dividing tile size.
            row = int(index.y)
            col = int(index.x)
        elif isinstance(index, tuple) and len(index) == 2 and all(isinstance(elem, int) for elem in index):
            # If a 2-elements tuple of integers, interpret it as (row, col).
            row, col = index
        else:
            raise IndexError(f"Unsupported indexing value for class Maze: {index}")

        # Check coordinates are within boundaries.
        if row < 0 or row >= MAZE_TILES_ROWS or col < 0 or col >= MAZE_TILES_COLS:
            raise IndexError(f"Index {(row, col)} is out of maze bounds")

        return row * MAZE_TILES_COLS + col


    def tile_is_wall(self, index):
        """Function that returns True if the tile at desired index is not walkable (is a wall)."""
        return self[index] == MazeTiles.WALL
    

    def update_tile(self, pacman_position):
        """Updates maze if needed by replacing a pellet with an empty tile. Returns the index of
        the tile in the array if such a replacement was performed, None otherwise."""
        index = self._index_convert(pacman_position)
        tile = self._tiles[index]

        if tile in (MazeTiles.PELLET, MazeTiles.POWER_PELLET):
            self._tiles[index] = MazeTiles.EMPTY
            self._n_pellets -= 1
            return index, tile
        
        return None, None
    
    def completed(self):
        """Function that returns True if all the pellets were eaten, False otherwise."""
        return self._n_pellets == 0