# -*- coding: utf-8 -*-

from pyglet.window import Window
from enum import IntEnum, IntFlag
import os

from src.directions import Vector2


# --------------------------------------------------------------------
# Constants related to the pyglet window.
# --------------------------------------------------------------------

# Minimum size allowed for the window to prevent poor visualization.
WINDOW_MINIMUM_SIZE = (250, 300)

# Pyglet window initialization arguments.
WINDOW_INIT_KWARGS = {'width' : WINDOW_MINIMUM_SIZE[0],
                      'height': WINDOW_MINIMUM_SIZE[1],
                      'fullscreen': False,
                      'resizable': True,
                      'caption': "Pac-Man",
                      'style': Window.WINDOW_STYLE_DEFAULT,
                      'vsync': True}

# Interval between two game updates in seconds.
GAME_ORIGINAL_FPS = 60.606061
GAME_ORIGINAL_UPDATES_INTERVAL = 1 / GAME_ORIGINAL_FPS
GAME_TENTATIVE_UPDATES_INTERVAL = 1 / 100

# Constant defining where the image are stored.
WINDOW_ICON_PATH = "./assets/images/icon.ico"

# --------------------------------------------------------------------


# --------------------------------------------------------------------
# Constants related to the maze.
# --------------------------------------------------------------------

# Enum defining types of tiles.
MazeTiles = IntEnum('MazeTiles', ['WALL', 'EMPTY', 'PELLET', 'POWER_PELLET', 'DOOR'])

# Location of image with maze starting configuration.
MAZE_START_IMAGE = "./assets/images/Maze Initial.png"

# Coordinates (left pixel counting from left, bottom pixel counting from bottom) of an empty tile in the initial maze.
MAZE_START_IMAGE_EMPTY_TILE_REGION_COORDS = (0, 128)

# Size of maze tiles expressed in pixels.
MAZE_TILE_PX_SIZE = 8

# Initial maze design expressed as a 1D array of tile indices.
MAZE_START_TILES = (MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.POWER_PELLET, MazeTiles.WALL, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.WALL, MazeTiles.POWER_PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.EMPTY, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.EMPTY, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.EMPTY, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.EMPTY, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.EMPTY, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.DOOR, MazeTiles.DOOR, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.EMPTY, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.EMPTY, MazeTiles.WALL, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.WALL, MazeTiles.EMPTY, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.PELLET, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.WALL, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.WALL, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.PELLET, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.EMPTY, MazeTiles.WALL, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.WALL, MazeTiles.EMPTY, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.EMPTY, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.EMPTY, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.EMPTY, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.EMPTY, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.EMPTY, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.EMPTY, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.POWER_PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.POWER_PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL)

# Dimentions of maze expressed in number of tiles.
MAZE_TILES_COLS = 28
MAZE_TILES_ROWS = 31

# Warp tunnel tiles.
WARP_TUNNEL_ROW = 14
WARP_TUNNEL_TELEPORT_MARGIN = 2
WARP_TUNNEL_COL_LEFT = 4
WARP_TUNNEL_COL_RIGHT = 23

# Number of pellets in initial maze state.
MAZE_START_NUM_PELLET = sum(elem in (MazeTiles.PELLET, MazeTiles.POWER_PELLET) for elem in MAZE_START_TILES)


# --------------------------------------------------------------------


# --------------------------------------------------------------------
# Constants related to the animated sprites.
# --------------------------------------------------------------------

# Paths of images containing the sprite sheets for the animations.
PACMAN_ALL_SPRITES = "./assets/images/Pac-Man.png"
GHOSTS_ALL_SPRITES = "./assets/images/Ghosts.png"

# Duration of each frame in the animations.
PACMAN_MOVE_ANIMATION_PERIOD_FRAMES  = 2
PACMAN_DEATH_ANIMATION_PERIOD_FRAMES = (30, 7, 8, 7, 8, 7, 8, 7, 8, 7, 15)
GHOSTS_MOVE_ANIMATION_PERIOD_FRAMES  = 8
GHOSTS_FRIGHT_FLASH_ANIMATION_PERIOD_FRAMES = 14 

# Size of Pac-Man and Ghost sprites expressed in pixels.
PACMAN_GHOSTS_SPRITES_PX_SIZE = 16

# Function providing the right sprite for each pacman condition.
# Rows go from bottom to top due to how pyglet increases y-axis.
PACMAN_SPAWNING_FRAME_IDX = 44
def PACMAN_SPRITE_IDX(direction, spawning, dead, frame_idx):
    if dead:
        return 45 + frame_idx if 0 <= frame_idx <= len(PACMAN_DEATH_ANIMATION_PERIOD_FRAMES) else 3

    if spawning:
        return PACMAN_SPAWNING_FRAME_IDX

    idx = 0

    match frame_idx:
        case 0:
            return PACMAN_SPAWNING_FRAME_IDX
        case 1:
            idx += 1
        case 2:
            idx += 0
        case 3:
            idx += 1

    match direction:
        case Vector2.DOWN:
            idx += 0
        case Vector2.UP:
            idx += 14
        case Vector2.LEFT:
            idx += 28
        case Vector2.RIGHT:
            idx += 42
        
    return idx 

# Function providing the right sprite for each ghost condition.
# Rows go from bottom to top due to how pyglet increases y-axis.
def GHOST_SPRITE_IDX(name, frightened_blue, frightened_white, transparent, direction, frame_idx):
    if transparent:
        match direction:
            case Vector2.RIGHT:
                return 32
            case Vector2.LEFT:
                return 33
            case Vector2.UP:
                return 34
            case Vector2.DOWN:
                return 35

    if frightened_blue:
        return 44 + frame_idx

    if frightened_white:
        return 46 + frame_idx

    idx = 0

    match name:
        case Ghost.BLINKY:
            idx += 36
        case Ghost.PINKY:
            idx += 24
        case Ghost.INKY:
            idx += 12
        case Ghost.CLYDE:
            idx += 0

    match direction:
        case Vector2.RIGHT:
            idx += 0
        case Vector2.LEFT:
            idx += 2
        case Vector2.UP:
            idx += 4
        case Vector2.DOWN:
            idx += 6
        
    return idx + frame_idx 




# --------------------------------------------------------------------


# --------------------------------------------------------------------
# Constants related to the font.
# --------------------------------------------------------------------

# Path of image containing the font sheet.
FONT_SHEET_PATH = "./assets/images/Font.png"

# Size of font tiles expressed in pixels.
FONT_TILE_PX_SIZE = 8

# Colors present in font sheet, ordered as in the font sheet (ordered from bottom to top due to how pyglet increases y-axis).
FontColors = IntEnum('FontColors', ['WHITE', 'YELLOW', 'MELON', 'CASABLANCA', 'CYAN', 'MAUVE', 'RED', 'LAVANDER'], start = 0)

# Characters present, ordered as in the font sheet (rows go from bottom to top due to how pyglet increases y-axis).
FONT_SHEET_CHARACTERS = r'%%%%%%%         0123456789/-"   PQRSTUVWXYZ!cptsABCDEFGHIJKLMNO '

# --------------------------------------------------------------------



# --------------------------------------------------------------------
# Constants related to Pac-Man.
# --------------------------------------------------------------------

# Pac-Man states.
PacManStates = IntEnum('PacManStates', ['SPAWNING', 'MOVING', 'STUCK', 'TURNING', 'DEAD'])

# Coordinates of tile where Pac-Man starts the game.
PACMAN_START_POSITION = Vector2(14, 23.5)

# One-frame penalty when eating pellet, 3 frames penalty when eating power pellet (in original game frame-rate).
PACMAN_PELLET_PENALTIES = {MazeTiles.PELLET: 1, MazeTiles.POWER_PELLET: 3}

# --------------------------------------------------------------------


# --------------------------------------------------------------------
# Constants related to Cruise Elroy.
# --------------------------------------------------------------------

# Levels of speed increase due to ghost becoming Cruise Elroy.
CruiseElroyLevel = IntEnum('CruiseElroyLevel', ['NULL', 'FIRST', 'SECOND'], start = 0)

# Thresholds for the number of pellets remaining in the level for Blinky to turn into Cruise Elroy.
def CRUISE_ELROY_PELLETS_THR(level):
    if level <= 0:
        raise ValueError(f'invalid level value passed to constants.CRUISE_ELROY_DOTS_THR: {level}')
    elif level >= 19:
        return 120, 60
    
    first_thr  = (20, 30, 40, 40, 40, 50, 50, 50, 60, 60, 60, 80, 80, 80, 100, 100, 100, 100)
    second_thr = (10, 15, 20, 20, 20, 25, 25, 25, 30, 30, 30, 40, 40, 40, 50 , 50 , 50 , 50 )
    
    return first_thr[level - 1], second_thr[level - 1]

# --------------------------------------------------------------------



# --------------------------------------------------------------------
# Constants related to speed of Pac-Man and Ghosts.
# --------------------------------------------------------------------

# Maximum Pac-Man move speed in tiles per second.
REFERENCE_SPEED = 75.75757625 / 8

# Function returning the Pac-Man speed depending on the current level and if fright is on.
def PACMAN_SPEED(level, fright):
    multiplier = None

    if level == 1:
        multiplier = 0.90 if fright else 0.80
    elif level <= 4:
        multiplier = 0.95 if fright else 0.90
    elif level <= 20:
        multiplier = 1.00
    else:
        multiplier = 0.90

    return multiplier * REFERENCE_SPEED


# Function returning the Ghost speed depending on the current level, if fright is on, if ghost is in warp tunnel or in the house.
def GHOSTS_SPEED(level, fright, in_warp_tunnel, going_to_house, in_or_exiting_house, cruise_elroy):
    multiplier = None

    if going_to_house:
        multiplier = 1.6
    elif in_or_exiting_house:
        multiplier = 0.40
    elif level == 1:
        multiplier = 0.40 if in_warp_tunnel else 0.50 if fright else 0.80 if cruise_elroy == CruiseElroyLevel.FIRST else 0.85 if cruise_elroy == CruiseElroyLevel.SECOND else 0.75
    elif level <= 4:
        multiplier = 0.45 if in_warp_tunnel else 0.55 if fright else 0.90 if cruise_elroy == CruiseElroyLevel.FIRST else 0.95 if cruise_elroy == CruiseElroyLevel.SECOND else 0.85
    else:
        multiplier = 0.50 if in_warp_tunnel else 0.60 if fright else 1.00 if cruise_elroy == CruiseElroyLevel.FIRST else 1.05 if cruise_elroy == CruiseElroyLevel.SECOND else 0.95
    
    return multiplier * REFERENCE_SPEED


# --------------------------------------------------------------------


# --------------------------------------------------------------------
# Constants related to Level animations.
# --------------------------------------------------------------------

# Possible states for the level.
LevelStates = IntEnum('LevelStates', ['FIRST_WELCOME', 'READY', 'PLAYING', 
                                      'DEATH', 'COMPLETED', 'GAME_OVER',
                                      'PAUSE_AFTER_EATING', 'PAUSE_BEFORE_DEATH', 'PAUSE_BEFORE_COMPLETED'])

# Number and period of white flashes for the level completed animation.
# Level end animation colors: white, blue, white, blue, white, blue, white, blue.
LEVEL_COMPLETED_FLASH_NUM = 4
LEVEL_COMPLETED_FLASH_ANIMATION_PERIOD_FRAMES = 12

# Duration (in original game frames) of animations corresponding to different level states.
LEVEL_STATES_DURATION = {LevelStates.FIRST_WELCOME         : 150,
                         LevelStates.READY                 : 120,
                         LevelStates.PLAYING               : float('inf'),
                         LevelStates.DEATH                 : sum(PACMAN_DEATH_ANIMATION_PERIOD_FRAMES) + 50,
                         LevelStates.COMPLETED             : 2 * LEVEL_COMPLETED_FLASH_NUM * LEVEL_COMPLETED_FLASH_ANIMATION_PERIOD_FRAMES,
                         LevelStates.GAME_OVER             : 120,
                         LevelStates.PAUSE_AFTER_EATING    : 60,
                         LevelStates.PAUSE_BEFORE_DEATH    : 60,
                         LevelStates.PAUSE_BEFORE_COMPLETED: 120}

# --------------------------------------------------------------------


# --------------------------------------------------------------------
# Constants related to Game UI.
# --------------------------------------------------------------------

# Color of background.
UI_BACKGROUND_COLOR = (0, 0, 0)

# Coordinates of 'HIGH SCORE' text.
GAME_HIGH_SCORE_TEXT_COORDS   = (- 4.5 * MAZE_TILE_PX_SIZE, +18 * MAZE_TILE_PX_SIZE)

# Coordinates of '1UP' text.
GAME_1UP_TEXT_COORDS          = (-10.5 * MAZE_TILE_PX_SIZE, +18 * MAZE_TILE_PX_SIZE)

# Coordinates of current score left-most digit.
GAME_SCORE_NUMBER_COORDS      = (-13.5 * MAZE_TILE_PX_SIZE, +17 * MAZE_TILE_PX_SIZE)

# Coordinates of high score left-most digit.
GAME_HIGH_SCORE_NUMBER_COORDS = (- 3.5 * MAZE_TILE_PX_SIZE, +17 * MAZE_TILE_PX_SIZE)

# Number of digits of the theoretical maximum score.
MAX_SCORE_NUM_DIGITS = 7

# In-Game UI colors.
GAME_DEFAULT_TEXT_COLOR = FontColors.WHITE

# Path of image containing the UI tiles (fruits and Pac-Man life).
UI_TILES_SHEET_PATH = "./assets/images/UI.png"

# Size of UI tiles expressed in pixels.
UI_TILES_PX_SIZE = 16

# Elements present in UI tiles sheet, ordered as in the sheet.
Fruits = IntEnum('Fruits', ['CHERRY', 'STRAWBERRY', 'PEACH', 'APPLE', 'GRAPES', 'GALAXIAN', 'BELL', 'KEY'], start = 0)
LIFE_ICON_UI = max(Fruits) + 1

# Coordinates of left-most life icon.
GAME_LEFT_LIVES_ICON_COORDS  = (-11 * MAZE_TILE_PX_SIZE, -16.5 * MAZE_TILE_PX_SIZE) 

# Coordinates of right-most fruit icon.
GAME_RIGHT_FRUIT_ICON_COORDS = (+11 * MAZE_TILE_PX_SIZE, -16.5 * MAZE_TILE_PX_SIZE) 

# Max number of fruits to show on bottom right of screen.
GAME_MAX_FRUIT_ICON_NUMBER = 7

# Fruit associated to each level.
def FRUIT_OF_LEVEL(level):
    if level <= 0:
        raise ValueError(f'invalid level value passed to constants.FRUIT_OF_LEVEL: {level}')
    elif level == 1:
        return Fruits.CHERRY
    elif level == 2:
        return Fruits.STRAWBERRY
    elif level <= 4:
        return Fruits.PEACH
    elif level <= 6:
        return Fruits.APPLE
    elif level <= 8:
        return Fruits.GRAPES
    elif level <= 10:
        return Fruits.GALAXIAN
    elif level <= 12:
        return Fruits.BELL

    return Fruits.KEY

# UI elements which can be optionally drawn during gameplay depending on state.
DynamicUIElements = IntFlag('DynamicUIElements', ['PACMAN', 'GHOSTS', 'FRUIT', 'READY_TEXT', 'PLAYER_ONE_TEXT', 'GAME_OVER_TEXT'])

# Coordinates and color of 'PLAYER ONE' text.
LEVEL_PLAYER_ONE_TEXT_COORDS = (-4.5 * MAZE_TILE_PX_SIZE, +4 * MAZE_TILE_PX_SIZE)
LEVEL_PLAYER_ONE_TEXT_COLOR  = FontColors.CYAN

# Coordinates and color of 'READY!' text.
LEVEL_READY_TEXT_COORDS      = (-2.5 * MAZE_TILE_PX_SIZE, -2 * MAZE_TILE_PX_SIZE)
LEVEL_READY_TEXT_COLOR       = FontColors.YELLOW

# Coordinates and color of 'GAME OVER' text.
LEVEL_GAME_OVER_TEXT_COORDS  = (-4.5 * MAZE_TILE_PX_SIZE, -2 * MAZE_TILE_PX_SIZE)
LEVEL_GAME_OVER_TEXT_COLOR   = FontColors.RED

# --------------------------------------------------------------------


# --------------------------------------------------------------------
# Constants related to Score.
# --------------------------------------------------------------------

# Possible actions causing increase in score.
ScoreActions = IntEnum('ScoreActions', ['EAT_PELLET', 'EAT_POWER_PELLET', 'EAT_GHOST', 'EAT_FRUIT'])

# Points given per action.
SCORE_POINTS_EAT_PELLET = 10
SCORE_POINTS_EAT_POWER_PELLET = 50
SCORE_POINTS_EAT_GHOST_BASE = 200

def SCORE_POINTS_EAT_FRUIT(level):
    points_per_fruit = {Fruits.CHERRY: 100, Fruits.STRAWBERRY: 300, Fruits.PEACH: 500, Fruits.APPLE: 700, Fruits.GRAPES: 1000, Fruits.GALAXIAN: 2000, Fruits.BELL: 3000, Fruits.KEY: 5000}
    
    return points_per_fruit[FRUIT_OF_LEVEL(level)]


# Path of file where to store high score.
HIGH_SCORE_FILE = os.path.join(os.path.expanduser('~'), '.pacman_game')
HIGH_SCORE_FILE_NUM_BYTES = 4

# --------------------------------------------------------------------


# --------------------------------------------------------------------
# Constants related to the Game orchestrator.
# --------------------------------------------------------------------

# Number of lives at the beginning of the game.
STARTING_LIVES_PACMAN = 5 # 1, 2, 3 or 5 are all valid for this setting

# Score above which an extra life is awarded.
EXTRA_LIFE_POINTS_REQUIREMENT = 10000 # 10000, 15000 and 20000 are all valid for this setting

# Thresholds at which fruits appear: after eating 70 pellets and 170 pellets.
FRUIT_SPAWN_THRESHOLDS = (MAZE_START_NUM_PELLET - 70, MAZE_START_NUM_PELLET - 170)

# Coordinates at which fruits appear.
FRUIT_SPAWN_POSITION = Vector2(x = 14, y = 17.5)

# Time for which fruit is vibible and edible: between 9 and 10 seconds. This variable stores it in frames.
FRUIT_TIME_ACTIVE_RANGE = (int(9 * GAME_ORIGINAL_FPS), int(10 * GAME_ORIGINAL_FPS))

# Duration of fright time (in original game frames) and number of flashes before fright mode ends.
def FRIGHT_TIME_AND_FLASHES(level):
    if level <= 0:
        raise ValueError(f'invalid level value passed to constants.FRIGHT_TIME_SECS: {level}')
    elif level >= 19:
        return 0, 0
    
    times_secs  = (6, 5, 4, 3, 2, 5, 2, 2, 1, 5, 2, 1, 1, 3, 1, 1, 0, 1)
    flashes_num = (5, 5, 5, 5, 5, 5, 5, 5, 3, 5, 5, 3, 3, 5, 3, 3, 0, 3)
    
    return times_secs[level - 1] * GAME_ORIGINAL_FPS, flashes_num[level - 1]


# --------------------------------------------------------------------



# --------------------------------------------------------------------
# Constants related to the Ghosts.
# --------------------------------------------------------------------

# Enum defining names of ghost.
Ghost = IntEnum('Ghost', ['BLINKY', 'PINKY', 'INKY', 'CLYDE'], start = 0)

# Enum defining modes of ghost behaviour.
GhostBehaviour = IntFlag('GhostBehaviour', ['CHASE', 'SCATTER', 'FRIGHTENED', 'IN_HOUSE', 'EXITING_HOUSE', 'GOING_TO_HOUSE', 'ENTERING_HOUSE'])

# Starting positions, directions and behaviour of ghosts.
GHOSTS_START_POSITIONS = {Ghost.BLINKY: Vector2(x = 14, y = 11.5),
                          Ghost.PINKY : Vector2(x = 14, y = 14.5),
                          Ghost.INKY  : Vector2(x = 12, y = 14.5),
                          Ghost.CLYDE : Vector2(x = 16, y = 14.5)}

GHOSTS_START_DIRECTIONS = {Ghost.BLINKY: Vector2.LEFT,
                           Ghost.PINKY : Vector2.DOWN,
                           Ghost.INKY  : Vector2.UP,
                           Ghost.CLYDE : Vector2.UP}

GHOSTS_START_BEHAVIOUR  = {Ghost.BLINKY: GhostBehaviour.SCATTER,
                           Ghost.PINKY : GhostBehaviour.SCATTER | GhostBehaviour.IN_HOUSE,
                           Ghost.INKY  : GhostBehaviour.SCATTER | GhostBehaviour.IN_HOUSE,
                           Ghost.CLYDE : GhostBehaviour.SCATTER | GhostBehaviour.IN_HOUSE}

# Tiles where the ghosts are not allowed to turn up.
GHOSTS_FORBIDDEN_TURNING_UP_TILES = (Vector2(15.5, 23.5), Vector2(12.5, 23.5), Vector2(15.5, 11.5), Vector2(12.5, 11.5))

# Target tile of each ghost when in scatter mode.
GHOSTS_SCATTER_MODE_TARGET_TILES = {Ghost.BLINKY: Vector2(25.5, -3.5),
                                    Ghost.PINKY : Vector2( 2.5, -3.5),
                                    Ghost.INKY  : Vector2(27.5, 31.5),
                                    Ghost.CLYDE : Vector2( 0.5, 31.5)}

# Target tile to reach when ghost is eaten.
GHOSTS_EATEN_TARGET_TILE = Vector2(x = 13.5, y = 11.5)

# Target y coord to reach when ghost enters house before resuming chase.
GHOSTS_EATEN_TARGET_Y_IN_HOUSE = GHOSTS_START_POSITIONS[Ghost.PINKY].y + 0.5


# Duration of scatter and chase mode alternations in original game frames.
def SCATTER_CHASE_ALTERNATIONS(level):
    if level <= 0:
        raise ValueError(f'invalid level value passed to constants.SCATTER_CHASE_ALTERNATIONS: {level}')
    
    elif level == 1:
        mode_durations = ((GhostBehaviour.SCATTER, 7    * GAME_ORIGINAL_FPS),
                          (GhostBehaviour.CHASE  , 20   * GAME_ORIGINAL_FPS),
                          (GhostBehaviour.SCATTER, 7    * GAME_ORIGINAL_FPS),
                          (GhostBehaviour.CHASE  , 20   * GAME_ORIGINAL_FPS),
                          (GhostBehaviour.SCATTER, 5    * GAME_ORIGINAL_FPS),
                          (GhostBehaviour.CHASE  , 20   * GAME_ORIGINAL_FPS),
                          (GhostBehaviour.SCATTER, 5    * GAME_ORIGINAL_FPS),
                          (GhostBehaviour.CHASE  , float('inf')))
    elif level <= 4:
        mode_durations = ((GhostBehaviour.SCATTER, 7    * GAME_ORIGINAL_FPS),
                          (GhostBehaviour.CHASE  , 20   * GAME_ORIGINAL_FPS),
                          (GhostBehaviour.SCATTER, 7    * GAME_ORIGINAL_FPS),
                          (GhostBehaviour.CHASE  , 20   * GAME_ORIGINAL_FPS),
                          (GhostBehaviour.SCATTER, 5    * GAME_ORIGINAL_FPS),
                          (GhostBehaviour.CHASE  , 1033 * GAME_ORIGINAL_FPS),
                          (GhostBehaviour.SCATTER, 1),
                          (GhostBehaviour.CHASE  , float('inf')))
    else:
        mode_durations = ((GhostBehaviour.SCATTER, 5    * GAME_ORIGINAL_FPS),
                          (GhostBehaviour.CHASE  , 20   * GAME_ORIGINAL_FPS),
                          (GhostBehaviour.SCATTER, 5    * GAME_ORIGINAL_FPS),
                          (GhostBehaviour.CHASE  , 20   * GAME_ORIGINAL_FPS),
                          (GhostBehaviour.SCATTER, 5    * GAME_ORIGINAL_FPS),
                          (GhostBehaviour.CHASE  , 1037 * GAME_ORIGINAL_FPS),
                          (GhostBehaviour.SCATTER, 1),
                          (GhostBehaviour.CHASE  , float('inf')))
    
    return mode_durations


# Dot counter limits for each ghost and each level.
def DOT_COUNTER_LIMIT(ghost, level):
    if ghost == Ghost.BLINKY or ghost == Ghost.PINKY:
        return 0

    elif ghost == Ghost.INKY:
        if level == 1:
            return 30
        
        return 0

    elif ghost == Ghost.CLYDE:
        if level == 1:
            return 60
        elif level == 2:
            return 50

        return 0

    raise ValueError(f'invalid value passed to constants.DOT_COUNTER_LIMIT: ghost {ghost}, level {level}')


# Global dot counter limits for each ghost.
DOT_GLOBAL_COUNTER_LIMIT = {Ghost.PINKY: 7, Ghost.INKY: 17, Ghost.CLYDE: 32}

# Threshold for timer counting how long since last dot eaten to force one ghost out.
DOTS_NOT_EATEN_TIMER_THR = lambda level: (4 if level < 5 else 3) * GAME_ORIGINAL_FPS


# --------------------------------------------------------------------


# --------------------------------------------------------------------
# Constants related to the Pseudo-Random Number Generator for Frightened Ghost directions.
# --------------------------------------------------------------------

# First 8192 bytes of the Pac-Man ROM.
PRNG_ROM_MEM = "F3 3E 3F ED 47 C3 0B 23 77 23 10 FC C9 C3 0E 07 85 6F 3E 00 8C 67 7E C9 78 87 D7 5F 23 56 EB C9 E1 87 D7 5F 23 56 EB E9 E1 46 23 4E 23 E5 18 12 11 90 4C 06 10 C3 51 00 AF 32 00 50 32 07 50 C3 38 00 2A 80 4C 70 2C 71 2C 20 02 2E C0 22 80 4C C9 1A A7 28 06 1C 1C 1C 10 F7 C9 E1 06 03 7E 12 23 1C 10 FA E9 C3 2D 20 00 01 02 03 04 05 06 07 08 09 0A 0B 0C 0D 0E 0F 10 11 12 13 14 01 03 04 06 07 08 09 0A 0B 0C 0D 0E 0F 10 11 14 F5 32 C0 50 AF 32 00 50 F3 C5 D5 E5 DD E5 FD E5 21 8C 4E 11 50 50 01 10 00 ED B0 3A CC 4E A7 3A CF 4E 20 03 3A 9F 4E 32 45 50 3A DC 4E A7 3A DF 4E 20 03 3A AF 4E 32 4A 50 3A EC 4E A7 3A EF 4E 20 03 3A BF 4E 32 4F 50 21 02 4C 11 22 4C 01 1C 00 ED B0 DD 21 20 4C DD 7E 02 07 07 DD 77 02 DD 7E 04 07 07 DD 77 04 DD 7E 06 07 07 DD 77 06 DD 7E 08 07 07 DD 77 08 DD 7E 0A 07 07 DD 77 0A DD 7E 0C 07 07 DD 77 0C 3A D1 4D FE 01 20 38 DD 21 20 4C 3A A4 4D 87 5F 16 00 DD 19 2A 24 4C ED 5B 34 4C DD 7E 00 32 24 4C DD 7E 01 32 25 4C DD 7E 10 32 34 4C DD 7E 11 32 35 4C DD 75 00 DD 74 01 DD 73 10 DD 72 11 3A A6 4D A7 CA 76 01 ED 4B 22 4C ED 5B 32 4C 2A 2A 4C 22 22 4C 2A 3A 4C 22 32 4C ED 43 2A 4C ED 53 3A 4C 21 22 4C 11 F2 4F 01 0C 00 ED B0 21 32 4C 11 62 50 01 0C 00 ED B0 CD DC 01 CD 21 02 CD C8 03 3A 00 4E A7 28 12 CD 9D 03 CD 90 14 CD 1F 14 CD 67 02 CD AD 02 CD FD 02 3A 00 4E 3D 20 06 32 AC 4E 32 BC 4E CD 0C 2D CD C1 2C FD E1 DD E1 E1 D1 C1 3A 00 4E A7 28 08 3A 40 50 E6 10 CA 00 00 3E 01 32 00 50 FB F1 C9 21 84 4C 34 23 35 23 11 19 02 01 01 04 34 7E E6 0F EB BE 20 13 0C 1A C6 10 E6 F0 12 23 BE 20 08 0C EB 36 00 23 13 10 E5 21 8A 4C 71 2C 7E 87 87 86 3C 77 2C 7E 87 86 87 87 86 3C 77 C9 06 A0 0A 60 0A 60 0A A0 21 90 4C 3A 8A 4C 4F 06 10 7E A7 28 2F E6 C0 07 07 B9 30 28 35 7E E6 3F 20 22 77 C5 E5 2C 7E 2C 46 21 5B 02 E5 E7 94 08 A3 06 8E 05 72 12 00 10 0B 10 63 02 2B 21 F0 21 B9 22 E1 C1 2C 2C 2C 10 C8 C9 EF 1C 86 C9 3A 6E 4E FE 99 17 32 06 50 1F D0 3A 00 50 47 CB 00 3A 66 4E 17 E6 0F 32 66 4E D6 0C CC DF 02 CB 00 3A 67 4E 17 E6 0F 32 67 4E D6 0C C2 9A 02 21 69 4E 34 CB 00 3A 68 4E 17 E6 0F 32 68 4E D6 0C C0 21 69 4E 34 C9 3A 69 4E A7 C8 47 3A 6A 4E 5F FE 00 C2 C4 02 3E 01 32 07 50 CD DF 02 7B FE 08 C2 CE 02 AF 32 07 50 1C 7B 32 6A 4E D6 10 C0 32 6A 4E 05 78 32 69 4E C9 3A 6B 4E 21 6C 4E 34 96 C0 77 3A 6D 4E 21 6E 4E 86 27 D2 F6 02 3E 99 77 21 9C 4E CB CE C9 21 CE 4D 34 7E E6 0F 20 1F 7E 0F 0F 0F 0F 47 3A D6 4D 2F B0 4F 3A 6E 4E D6 01 30 02 AF 4F 28 01 79 32 05 50 79 32 04 50 DD 21 D8 43 FD 21 C5 43 3A 00 4E FE 03 CA 44 03 3A 03 4E FE 02 D2 44 03 CD 69 03 CD 76 03 C9 3A 09 4E A7 3A CE 4D C2 59 03 CB 67 CC 69 03 C4 83 03 C3 61 03 CB 67 CC 76 03 C4 90 03 3A 70 4E A7 CC 90 03 C9 DD 36 00 50 DD 36 01 55 DD 36 02 31 C9 FD 36 00 50 FD 36 01 55 FD 36 02 32 C9 DD 36 00 40 DD 36 01 40 DD 36 02 40 C9 FD 36 00 40 FD 36 01 40 FD 36 02 40 C9 3A 06 4E D6 05 D8 2A 08 4D 06 08 0E 10 7D 32 06 4D 32 D2 4D 91 32 02 4D 32 04 4D 7C 80 32 03 4D 32 07 4D 91 32 05 4D 32 D3 4D C9 3A 00 4E E7 D4 03 FE 03 E5 05 BE 06 3A 01 4E E7 DC 03 0C 00 EF 00 00 EF 06 00 EF 01 00 EF 14 00 EF 18 00 EF 04 00 EF 1E 00 EF 07 00 21 01 4E 34 21 01 50 36 01 C9 CD A1 2B 3A 6E 4E A7 28 0C AF 32 04 4E 32 02 4E 21 00 4E 34 C9 3A 02 4E E7 5F 04 0C 00 71 04 0C 00 7F 04 0C 00 85 04 0C 00 8B 04 0C 00 99 04 0C 00 9F 04 0C 00 A5 04 0C 00 B3 04 0C 00 B9 04 0C 00 BF 04 0C 00 CD 04 0C 00 D3 04 0C 00 D8 04 0C 00 E0 04 0C 00 1C 05 4B 05 56 05 61 05 6C 05 7C 05 EF 00 01 EF 01 00 EF 04 00 EF 1E 00 0E 0C CD 85 05 C9 21 04 43 3E 01 CD BF 05 0E 0C CD 85 05 C9 0E 14 CD 93 05 C9 0E 0D CD 93 05 C9 21 07 43 3E 03 CD BF 05 0E 0C CD 85 05 C9 0E 16 CD 93 05 C9 0E 0F CD 93 05 C9 21 0A 43 3E 05 CD BF 05 0E 0C CD 85 05 C9 0E 33 CD 93 05 C9 0E 2F CD 93 05 C9 21 0D 43 3E 07 CD BF 05 0E 0C CD 85 05 C9 0E 35 CD 93 05 C9 0E 31 C3 80 05 EF 1C 11 0E 12 C3 85 05 0E 13 CD 85 05 CD 79 08 35 EF 11 00 EF 05 01 EF 10 14 EF 04 01 3E 01 32 14 4E AF 32 70 4E 32 15 4E 21 32 43 36 14 3E FC 11 20 00 06 1C DD 21 40 40 DD 77 11 DD 77 13 DD 19 10 F6 C9 21 A0 4D 06 21 3A 3A 4D 90 20 05 36 01 C3 8E 05 CD 17 10 CD 17 10 CD 23 0E CD 0D 0C CD D6 0B CD A5 05 CD FE 1E CD 25 1F CD 4C 1F CD 73 1F C9 21 A1 4D 06 20 3A 32 4D C3 24 05 21 A2 4D 06 22 3A 32 4D C3 24 05 21 A3 4D 06 24 3A 32 4D C3 24 05 3A D0 4D 47 3A D1 4D 80 FE 06 CA 8E 05 C3 2C 05 CD BE 06 C9 3A 75 4E 81 4F 06 1C CD 42 00 F7 4A 02 00 21 02 4E 34 C9 3A 75 4E 81 4F 06 1C CD 42 00 F7 45 02 00 CD 8E 05 C9 3A B5 4D A7 C8 AF 32 B5 4D 3A 30 4D EE 02 32 3C 4D 47 21 FF 32 DF 22 26 4D C9 36 B1 2C 36 B3 2C 36 B5 01 1E 00 09 36 B0 2C 36 B2 2C 36 B4 11 00 04 19 77 2D 77 2D 77 A7 ED 42 77 2D 77 2D 77 C9 3A 03 4E E7 F3 05 1B 06 74 06 0C 00 A8 06 CD A1 2B EF 00 01 EF 01 00 EF 1C 07 EF 1C 0B EF 1E 00 21 03 4E 34 3E 01 32 D6 4D 3A 71 4E FE FF C8 EF 1C 0A EF 1F 00 C9 CD A1 2B 3A 6E 4E FE 01 06 09 20 02 06 08 CD 5E 2C 3A 6E 4E FE 01 3A 40 50 28 0C CB 77 20 08 3E 01 32 70 4E C3 49 06 CB 6F C0 AF 32 70 4E 3A 6B 4E A7 28 15 3A 70 4E A7 3A 6E 4E 28 03 C6 99 27 C6 99 27 32 6E 4E CD A1 2B 21 03 4E 34 AF 32 D6 4D 3C 32 CC 4E 32 DC 4E C9 EF 00 01 EF 01 01 EF 02 00 EF 12 00 EF 03 00 EF 1C 03 EF 1C 06 EF 18 00 EF 1B 00 AF 32 13 4E 3A 6F 4E 32 14 4E 32 15 4E EF 1A 00 F7 57 01 00 21 03 4E 34 C9 21 15 4E 35 CD 6A 2B AF 32 03 4E 32 02 4E 32 04 4E 21 00 4E 34 C9 3A 04 4E E7 79 08 99 08 0C 00 CD 08 0D 09 0C 00 40 09 0C 00 72 09 88 09 0C 00 D2 09 D8 09 0C 00 E8 09 0C 00 FE 09 0C 00 02 0A 0C 00 04 0A 0C 00 06 0A 0C 00 08 0A 0C 00 0A 0A 0C 00 0C 0A 0C 00 0E 0A 0C 00 2C 0A 0C 00 7C 0A A0 0A 0C 00 A3 0A 78 A7 20 04 2A 0A 4E 7E DD 21 96 07 47 87 87 80 80 5F 16 00 DD 19 DD 7E 00 87 47 87 87 4F 87 87 81 80 5F 16 00 21 0F 33 19 CD 14 08 DD 7E 01 32 B0 4D DD 7E 02 47 87 80 5F 16 00 21 43 08 19 CD 3A 08 DD 7E 03 87 5F 16 00 FD 21 4F 08 FD 19 FD 6E 00 FD 66 01 22 BB 4D DD 7E 04 87 5F 16 00 FD 21 61 08 FD 19 FD 6E 00 FD 66 01 22 BD 4D DD 7E 05 87 5F 16 00 FD 21 73 08 FD 19 FD 6E 00 FD 66 01 22 95 4D CD EA 2B C9 03 01 01 00 02 00 04 01 02 01 03 00 04 01 03 02 04 01 04 02 03 02 05 01 05 00 03 02 06 02 05 01 03 03 03 02 05 02 03 03 06 02 05 02 03 03 06 02 05 00 03 04 07 02 05 01 03 04 03 02 05 02 03 04 06 02 05 02 03 05 07 02 05 00 03 05 07 02 05 02 03 05 05 02 05 01 03 06 07 02 05 02 03 06 07 02 05 02 03 06 08 02 05 02 03 06 07 02 05 02 03 07 08 02 05 02 03 07 08 02 06 02 03 07 08 02 11 46 4D 01 1C 00 ED B0 01 0C 00 A7 ED 42 ED B0 01 0C 00 A7 ED 42 ED B0 01 0C 00 A7 ED 42 ED B0 01 0E 00 ED B0 C9 11 B8 4D 01 03 00 ED B0 C9 14 1E 46 00 1E 3C 00 00 32 00 00 00 14 0A 1E 0F 28 14 32 19 3C 1E 50 28 64 32 78 3C 8C 46 C0 03 48 03 D0 02 58 02 E0 01 68 01 F0 00 78 00 01 00 F0 00 F0 00 B4 00 21 09 4E AF 06 0B CF CD C9 24 2A 73 4E 22 0A 4E 21 0A 4E 11 38 4E 01 2E 00 ED B0 21 04 4E 34 C9 3A 00 4E 3D 20 06 3E 09 32 04 4E C9 EF 11 00 EF 1C 83 EF 04 00 EF 05 00 EF 10 00 EF 1A 00 F7 54 00 00 F7 54 06 00 3A 72 4E 47 3A 09 4E A0 32 03 50 C3 94 08 3A 00 50 CB 67 C2 DE 08 21 04 4E 36 0E EF 13 00 C9 3A 0E 4E FE F4 20 06 21 04 4E 36 0C C9 CD 17 10 CD 17 10 CD DD 13 CD 42 0C CD 23 0E CD 36 0E CD C3 0A CD D6 0B CD 0D 0C CD 6C 0E CD AD 0E C9 3E 01 32 12 4E CD 87 24 21 04 4E 34 3A 14 4E A7 20 1F 3A 70 4E A7 28 19 3A 42 4E A7 28 13 3A 09 4E C6 03 4F 06 1C CD 42 00 EF 1C 05 F7 54 00 00 C9 34 C9 3A 70 4E A7 28 06 3A 42 4E A7 20 15 3A 14 4E A7 20 1A CD A1 2B EF 1C 05 F7 54 00 00 21 04 4E 34 C9 CD A6 0A 3A 09 4E EE 01 32 09 4E 3E 09 32 04 4E C9 AF 32 02 4E 32 04 4E 32 70 4E 32 09 4E 32 03 50 3E 01 32 00 4E C9 EF 00 01 EF 01 01 EF 02 00 EF 11 00 EF 13 00 EF 03 00 EF 04 00 EF 05 00 EF 10 00 EF 1A 00 EF 1C 06 3A 00 4E FE 03 28 06 EF 1C 05 EF 1D 00 F7 54 00 00 3A 00 4E 3D 28 04 F7 54 06 00 3A 72 4E 47 3A 09 4E A0 32 03 50 C3 94 08 3E 03 32 04 4E C9 F7 54 00 00 21 04 4E 34 AF 32 AC 4E 32 BC 4E C9 0E 02 06 01 CD 42 00 F7 42 00 00 21 00 00 CD 7E 26 21 04 4E 34 C9 0E 00 18 E8 18 E4 18 F8 18 E0 18 F4 18 DC 18 F0 EF 00 01 EF 06 00 EF 11 00 EF 13 00 EF 04 01 EF 05 01 EF 10 13 F7 43 00 00 21 04 4E 34 C9 AF 32 AC 4E 32 BC 4E 3E 02 32 CC 4E 32 DC 4E 3A 13 4E FE 14 38 02 3E 14 E7 6F 0A 08 21 6F 0A 6F 0A 9E 21 6F 0A 6F 0A 6F 0A 97 22 6F 0A 6F 0A 6F 0A 97 22 6F 0A 6F 0A 6F 0A 97 22 6F 0A 6F 0A 6F 0A 6F 0A 21 04 4E 34 34 AF 32 CC 4E 32 DC 4E C9 AF 32 CC 4E 32 DC 4E 06 07 21 0C 4E CF CD C9 24 21 04 4E 34 21 13 4E 34 2A 0A 4E 7E FE 14 C8 23 22 0A 4E C9 C3 88 09 C3 D2 09 06 2E DD 21 0A 4E FD 21 38 4E DD 56 00 FD 5E 00 FD 72 00 DD 73 00 DD 23 FD 23 10 EE C9 3A A4 4D A7 C0 DD 21 00 4C FD 21 C8 4D 11 00 01 FD BE 00 C2 D2 0B FD 36 00 0E 3A A6 4D A7 28 1B 2A CB 4D A7 ED 52 30 13 21 AC 4E CB FE 3E 09 DD BE 0B 20 04 CB BE 3E 09 32 0B 4C 3A A7 4D A7 28 1D 2A CB 4D A7 ED 52 30 27 3E 11 DD BE 03 28 07 DD 36 03 11 C3 33 0B DD 36 03 12 C3 33 0B 3E 01 DD BE 03 28 07 DD 36 03 01 C3 33 0B DD 36 03 01 3A A8 4D A7 28 1D 2A CB 4D A7 ED 52 30 27 3E 11 DD BE 05 28 07 DD 36 05 11 C3 68 0B DD 36 05 12 C3 68 0B 3E 03 DD BE 05 28 07 DD 36 05 03 C3 68 0B DD 36 05 03 3A A9 4D A7 28 1D 2A CB 4D A7 ED 52 30 27 3E 11 DD BE 07 28 07 DD 36 07 11 C3 9D 0B DD 36 07 12 C3 9D 0B 3E 05 DD BE 07 28 07 DD 36 07 05 C3 9D 0B DD 36 07 05 3A AA 4D A7 28 1D 2A CB 4D A7 ED 52 30 27 3E 11 DD BE 09 28 07 DD 36 09 11 C3 D2 0B DD 36 09 12 C3 D2 0B 3E 07 DD BE 09 28 07 DD 36 09 07 C3 D2 0B DD 36 09 07 FD 35 00 C9 06 19 3A 02 4E FE 22 C2 E2 0B 06 00 DD 21 00 4C 3A AC 4D A7 CA F0 0B DD 70 03 3A AD 4D A7 CA FA 0B DD 70 05 3A AE 4D A7 CA 04 0C DD 70 07 3A AF 4D A7 C8 DD 70 09 C9 21 CF 4D 34 3E 0A BE C0 36 00 3A 04 4E FE 03 20 15 21 64 44 3E 10 BE 20 02 3E 00 77 32 78 44 32 84 47 32 98 47 C9 21 32 47 3E 10 BE 20 02 3E 00 77 32 78 46 C9 3A A4 4D A7 C0 3A 94 4D 07 32 94 4D D0 3A A0 4D A7 C2 90 0C DD 21 05 33 FD 21 00 4D CD 00 20 22 00 4D 3E 03 32 28 4D 32 2C 4D 3A 00 4D FE 64 C2 90 0C 21 2C 2E 22 0A 4D 21 00 01 22 14 4D 22 1E 4D 3E 02 32 28 4D 32 2C 4D 3E 01 32 A0 4D 3A A1 4D FE 01 CA FB 0C FE 00 C2 C1 0C 3A 02 4D FE 78 CC 2E 1F FE 80 CC 2E 1F 3A 2D 4D 32 29 4D DD 21 20 4D FD 21 02 4D CD 00 20 22 02 4D C3 FB 0C DD 21 05 33 FD 21 02 4D CD 00 20 22 02 4D 3E 03 32 2D 4D 32 29 4D 3A 02 4D FE 64 C2 FB 0C 21 2C 2E 22 0C 4D 21 00 01 22 16 4D 22 20 4D 3E 02 32 29 4D 32 2D 4D 3E 01 32 A1 4D 3A A2 4D FE 01 CA 93 0D FE 00 C2 2C 0D 3A 04 4D FE 78 CC 55 1F FE 80 CC 55 1F 3A 2E 4D 32 2A 4D DD 21 22 4D FD 21 04 4D CD 00 20 22 04 4D C3 93 0D 3A A2 4D FE 03 C2 59 0D DD 21 FF 32 FD 21 04 4D CD 00 20 22 04 4D AF 32 2A 4D 32 2E 4D 3A 05 4D FE 80 C2 93 0D 3E 02 32 A2 4D C3 93 0D DD 21 05 33 FD 21 04 4D CD 00 20 22 04 4D 3E 03 32 2A 4D 32 2E 4D 3A 04 4D FE 64 C2 93 0D 21 2C 2E 22 0E 4D 21 00 01 22 18 4D 22 22 4D 3E 02 32 2A 4D 32 2E 4D 3E 01 32 A2 4D 3A A3 4D FE 01 C8 FE 00 C2 C0 0D 3A 06 4D FE 78 CC 7C 1F FE 80 CC 7C 1F 3A 2F 4D 32 2B 4D DD 21 24 4D FD 21 06 4D CD 00 20 22 06 4D C9 3A A3 4D FE 03 C2 EA 0D DD 21 03 33 FD 21 06 4D CD 00 20 22 06 4D 3E 02 32 2B 4D 32 2F 4D 3A 07 4D FE 80 C0 3E 02 32 A3 4D C9 DD 21 05 33 FD 21 06 4D CD 00 20 22 06 4D 3E 03 32 2B 4D 32 2F 4D 3A 06 4D FE 64 C0 21 2C 2E 22 10 4D 21 00 01 22 1A 4D 22 24 4D 3E 02 32 2B 4D 32 2F 4D 3E 01 32 A3 4D C9 21 C4 4D 34 3E 08 BE C0 36 00 3A C0 4D EE 01 32 C0 4D C9 3A A6 4D A7 C0 3A C1 4D FE 07 C8 87 2A C2 4D 23 22 C2 4D 5F 16 00 DD 21 86 4D DD 19 DD 5E 00 DD 56 01 A7 ED 52 C0 CB 3F 3C 32 C1 4D 21 01 01 22 B1 4D 22 B3 4D C9 3A A5 4D A7 28 05 AF 32 AC 4E C9 21 AC 4E 06 E0 3A 0E 4E FE E4 38 06 78 A6 CB E7 77 C9 FE D4 38 06 78 A6 CB DF 77 C9 FE B4 38 06 78 A6 CB D7 77 C9 FE 74 38 06 78 A6 CB CF 77 C9 78 A6 CB C7 77 C9 3A A5 4D A7 C0 3A D4 4D A7 C0 3A 0E 4E FE 46 28 0E FE AA C0 3A 0D 4E A7 C0 21 0D 4E 34 18 09 3A 0C 4E A7 C0 21 0C 4E 34 21 94 80 22 D2 4D 21 FD 0E 3A 13 4E FE 14 38 02 3E 14 47 87 80 D7 32 0C 4C 23 7E 32 0D 4C 23 7E 32 D4 4D F7 8A 04 00 C9 00 14 06 01 0F 07 02 15 08 02 15 08 04 14 09 04 14 09 05 17 0A 05 17 0A 06 09 0B 06 09 0B 03 16 0C 03 16 0C 07 16 0D 07 16 0D 07 16 0D 07 16 0D 07 16 0D 07 16 0D 07 16 0D 07 16 0D 07 16 0D 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 48 36 AF 32 D4 4D 21 00 00 22 D2 4D C9 EF 1C 9B 3A 00 4E 3D C8 EF 1C A2 C9 CD 91 12 3A A5 4D A7 C0 CD 66 10 CD 94 10 CD 9E 10 CD A8 10 CD B4 10 3A A4 4D A7 CA 39 10 CD 35 12 C9 CD 1D 17 CD 89 17 3A A4 4D A7 C0 CD 06 18 CD 36 1B CD 4B 1C CD 22 1D CD F9 1D 3A 04 4E FE 03 C0 CD 76 13 CD 69 20 CD 8C 20 CD AF 20 C9 3A AB 4D A7 C8 3D 20 08 32 AB 4D 3C 32 AC 4D C9 3D 20 08 32 AB 4D 3C 32 AD 4D C9 3D 20 08 32 AB 4D 3C 32 AE 4D C9 32 AF 4D 3D 32 AB 4D C9 3A AC 4D E7 0C 00 C0 10 D2 10 3A AD 4D E7 0C 00 18 11 2A 11 3A AE 4D E7 0C 00 5C 11 6E 11 8F 11 3A AF 4D E7 0C 00 C9 11 DB 11 FC 11 CD D8 1B 2A 00 4D 11 64 80 A7 ED 52 C0 21 AC 4D 34 C9 DD 21 01 33 FD 21 00 4D CD 00 20 22 00 4D 3E 01 32 28 4D 32 2C 4D 3A 00 4D FE 80 C0 21 2F 2E 22 0A 4D 22 31 4D AF 32 A0 4D 32 AC 4D 32 A7 4D DD 21 AC 4D DD B6 00 DD B6 01 DD B6 02 DD B6 03 C0 21 AC 4E CB B6 C9 CD AF 1C 2A 02 4D 11 64 80 A7 ED 52 C0 21 AD 4D 34 C9 DD 21 01 33 FD 21 02 4D CD 00 20 22 02 4D 3E 01 32 29 4D 32 2D 4D 3A 02 4D FE 80 C0 21 2F 2E 22 0C 4D 22 33 4D AF 32 A1 4D 32 AD 4D 32 A8 4D C3 01 11 CD 86 1D 2A 04 4D 11 64 80 A7 ED 52 C0 21 AE 4D 34 C9 DD 21 01 33 FD 21 04 4D CD 00 20 22 04 4D 3E 01 32 2A 4D 32 2E 4D 3A 04 4D FE 80 C0 21 AE 4D 34 C9 DD 21 03 33 FD 21 04 4D CD 00 20 22 04 4D 3E 02 32 2A 4D 32 2E 4D 3A 05 4D FE 90 C0 21 2F 30 22 0E 4D 22 35 4D 3E 01 32 2A 4D 32 2E 4D AF 32 A2 4D 32 AE 4D 32 A9 4D C3 01 11 CD 5D 1E 2A 06 4D 11 64 80 A7 ED 52 C0 21 AF 4D 34 C9 DD 21 01 33 FD 21 06 4D CD 00 20 22 06 4D 3E 01 32 2B 4D 32 2F 4D 3A 06 4D FE 80 C0 21 AF 4D 34 C9 DD 21 FF 32 FD 21 06 4D CD 00 20 22 06 4D AF 32 2B 4D 32 2F 4D 3A 07 4D FE 70 C0 21 2F 2C 22 10 4D 22 37 4D 3E 01 32 2B 4D 32 2F 4D AF 32 A3 4D 32 AF 4D 32 AA 4D C3 01 11 3A D1 4D E7 3F 12 0C 00 3F 12 21 00 4C 3A A4 4D 87 5F 16 00 19 3A D1 4D A7 20 27 3A D0 4D 06 27 80 47 3A 72 4E 4F 3A 09 4E A1 28 04 CB F0 CB F8 70 23 36 18 3E 00 32 0B 4C F7 4A 03 00 21 D1 4D 34 C9 36 20 3E 09 32 0B 4C 3A A4 4D 32 AB 4D AF 32 A4 4D 32 D1 4D 21 AC 4E CB F6 C9 3A A5 4D E7 0C 00 B7 12 B7 12 B7 12 B7 12 CB 12 F9 12 06 13 0E 13 16 13 1E 13 26 13 2E 13 36 13 3E 13 46 13 53 13 2A C5 4D 23 22 C5 4D 11 78 00 A7 ED 52 C0 3E 05 32 A5 4D C9 21 00 00 CD 7E 26 3E 34 11 B4 00 4F 3A 72 4E 47 3A 09 4E A0 28 04 3E C0 B1 4F 79 32 0A 4C 2A C5 4D 23 22 C5 4D A7 ED 52 C0 21 A5 4D 34 C9 21 BC 4E CB E6 3E 35 11 C3 00 C3 D6 12 3E 36 11 D2 00 C3 D6 12 3E 37 11 E1 00 C3 D6 12 3E 38 11 F0 00 C3 D6 12 3E 39 11 FF 00 C3 D6 12 3E 3A 11 0E 01 C3 D6 12 3E 3B 11 1D 01 C3 D6 12 3E 3C 11 2C 01 C3 D6 12 3E 3D 11 3B 01 C3 D6 12 21 BC 4E 36 20 3E 3E 11 59 01 C3 D6 12 3E 3F 32 0A 4C 2A C5 4D 23 22 C5 4D 11 B8 01 A7 ED 52 C0 21 14 4E 35 21 15 4E 35 CD 75 26 21 04 4E 34 C9 3A A6 4D A7 C8 DD 21 A7 4D DD 7E 00 DD B6 01 DD B6 02 DD B6 03 CA 98 13 2A CB 4D 2B 22 CB 4D 7C B5 C0 21 0B 4C 36 09 3A AC 4D A7 C2 A7 13 32 A7 4D 3A AD 4D A7 C2 B1 13 32 A8 4D 3A AE 4D A7 C2 BB 13 32 A9 4D 3A AF 4D A7 C2 C5 13 32 AA 4D AF 32 CB 4D 32 CC 4D 32 A6 4D 32 C8 4D 32 D0 4D 21 AC 4E CB AE CB BE C9 21 9E 4D 3A 0E 4E BE CA EE 13 21 00 00 22 97 4D C9 2A 97 4D 23 22 97 4D ED 5B 95 4D A7 ED 52 C0 21 00 00 22 97 4D 3A A1 4D A7 F5 CC 86 20 F1 C8 3A A2 4D A7 F5 CC A9 20 F1 C8 3A A3 4D A7 CC D1 20 C9 3A 72 4E 47 3A 09 4E A0 C8 47 DD 21 00 4C 1E 08 0E 08 16 07 3A 00 4D 83 DD 77 13 3A 01 4D 2F 82 DD 77 12 3A 02 4D 83 DD 77 15 3A 03 4D 2F 82 DD 77 14 3A 04 4D 83 DD 77 17 3A 05 4D 2F 81 DD 77 16 3A 06 4D 83 DD 77 19 3A 07 4D 2F 81 DD 77 18 3A 08 4D 83 DD 77 1B 3A 09 4D 2F 81 DD 77 1A 3A D2 4D 83 DD 77 1D 3A D3 4D 2F 81 DD 77 1C C3 FE 14 3A 72 4E 47 3A 09 4E A0 C0 47 1E 09 0E 07 16 06 DD 21 00 4C 3A 00 4D 2F 83 DD 77 13 3A 01 4D 82 DD 77 12 3A 02 4D 2F 83 DD 77 15 3A 03 4D 82 DD 77 14 3A 04 4D 2F 83 DD 77 17 3A 05 4D 81 DD 77 16 3A 06 4D 2F 83 DD 77 19 3A 07 4D 81 DD 77 18 3A 08 4D 2F 83 DD 77 1B 3A 09 4D 81 DD 77 1A 3A D2 4D 2F 83 DD 77 1D 3A D3 4D 81 DD 77 1C 3A A5 4D A7 C2 4B 15 3A A4 4D A7 C2 B4 15 21 1C 15 E5 3A 30 4D E7 8C 16 B1 16 D6 16 F7 16 78 A7 28 2B 0E C0 3A 0A 4C 57 A1 20 05 7A B1 C3 48 15 3A 30 4D FE 02 20 09 CB 7A 28 12 7A A9 C3 48 15 FE 03 20 09 CB 72 28 05 7A A9 32 0A 4C 21 C0 4D 56 3E 1C 82 DD 77 02 DD 77 04 DD 77 06 DD 77 08 0E 20 3A AC 4D A7 20 06 3A A7 4D A7 20 09 3A 2C 4D 87 82 81 DD 77 02 3A AD 4D A7 20 06 3A A8 4D A7 20 09 3A 2D 4D 87 82 81 DD 77 04 3A AE 4D A7 20 06 3A A9 4D A7 20 09 3A 2E 4D 87 82 81 DD 77 06 3A AF 4D A7 20 06 3A AA 4D A7 20 09 3A 2F 4D 87 82 81 DD 77 08 CD E6 15 CD 2D 16 CD 52 16 78 A7 C8 0E C0 3A 02 4C B1 32 02 4C 3A 04 4C B1 32 04 4C 3A 06 4C B1 32 06 4C 3A 08 4C B1 32 08 4C 3A 0C 4C B1 32 0C 4C C9 3A 06 4E D6 05 D8 3A 09 4D E6 0F FE 0C 38 04 16 18 18 12 FE 08 38 04 16 14 18 0A FE 04 38 04 16 10 18 02 16 14 DD 72 04 14 DD 72 06 14 DD 72 08 14 DD 72 0C DD 36 0A 3F 16 16 DD 72 05 DD 72 07 DD 72 09 DD 72 0D C9 3A 07 4E A7 C8 57 3A 3A 4D D6 3D 20 04 DD 36 0B 00 7A FE 0A D8 DD 36 02 32 DD 36 03 1D FE 0C D8 DD 36 02 33 C9 3A 08 4E A7 C8 57 3A 3A 4D D6 3D 20 04 DD 36 0B 00 7A FE 01 D8 3A C0 4D 1E 08 83 DD 77 02 7A FE 03 D8 3A 01 4D E6 08 0F 0F 0F 1E 0A 83 DD 77 0C 3C 3C DD 77 02 DD 36 0D 1E C9 3A 09 4D E6 07 FE 06 38 05 DD 36 0A 30 C9 FE 04 38 05 DD 36 0A 2E C9 FE 02 38 05 DD 36 0A 2C C9 DD 36 0A 2E C9 3A 08 4D E6 07 FE 06 38 05 DD 36 0A 2F C9 FE 04 38 05 DD 36 0A 2D C9 FE 02 38 05 DD 36 0A 2F C9 DD 36 0A 30 C9 3A 09 4D E6 07 FE 06 38 08 1E 2E CB FB DD 73 0A C9 FE 04 38 04 1E 2C 18 F2 FE 02 30 EC 1E 30 18 EA 3A 08 4D E6 07 FE 06 38 05 DD 36 0A 30 C9 FE 04 38 08 1E 2F CB F3 DD 73 0A C9 FE 02 38 04 1E 2D 18 F2 1E 2F 18 EE 06 04 ED 5B 39 4D 3A AF 4D A7 20 09 2A 37 4D A7 ED 52 CA 63 17 05 3A AE 4D A7 20 09 2A 35 4D A7 ED 52 CA 63 17 05 3A AD 4D A7 20 09 2A 33 4D A7 ED 52 CA 63 17 05 3A AC 4D A7 20 09 2A 31 4D A7 ED 52 CA 63 17 05 78 32 A4 4D 32 A5 4D A7 C8 21 A6 4D 5F 16 00 19 7E A7 C8 AF 32 A5 4D 21 D0 4D 34 46 04 CD 5A 2A 21 BC 4E CB DE C9 3A A4 4D A7 C0 3A A6 4D A7 C8 0E 04 06 04 DD 21 08 4D 3A AF 4D A7 20 13 3A 06 4D DD 96 00 B9 30 0A 3A 07 4D DD 96 01 B9 DA 63 17 05 3A AE 4D A7 20 13 3A 04 4D DD 96 00 B9 30 0A 3A 05 4D DD 96 01 B9 DA 63 17 05 3A AD 4D A7 20 13 3A 02 4D DD 96 00 B9 30 0A 3A 03 4D DD 96 01 B9 DA 63 17 05 3A AC 4D A7 20 13 3A 00 4D DD 96 00 B9 30 0A 3A 01 4D DD 96 01 B9 DA 63 17 05 C3 63 17 21 9D 4D 3E FF BE CA 11 18 35 C9 3A A6 4D A7 CA 2F 18 2A 4C 4D 29 22 4C 4D 2A 4A 4D ED 6A 22 4A 4D D0 21 4C 4D 34 C3 43 18 2A 48 4D 29 22 48 4D 2A 46 4D ED 6A 22 46 4D D0 21 48 4D 34 3A 0E 4E 32 9E 4D 3A 72 4E 4F 3A 09 4E A1 4F 21 3A 4D 7E 06 21 90 38 09 7E 06 3B 90 30 03 C3 AB 18 3E 01 32 BF 4D 3A 00 4E FE 01 CA 19 1A 3A 04 4E FE 10 D2 19 1A 79 A7 28 06 3A 40 50 C3 86 18 3A 00 50 CB 4F C2 99 18 2A 03 33 3E 02 32 30 4D 22 1C 4D C3 50 19 CB 57 C2 50 19 2A FF 32 AF 32 30 4D 22 1C 4D C3 50 19 3A 00 4E FE 01 CA 19 1A 3A 04 4E FE 10 D2 19 1A 79 A7 28 06 3A 40 50 C3 C8 18 3A 00 50 CB 4F CA C9 1A CB 57 CA D9 1A CB 47 CA E8 1A CB 5F CA F8 1A 2A 1C 4D 22 26 4D 06 01 DD 21 26 4D FD 21 39 4D CD 0F 20 E6 C0 D6 C0 20 4B 05 C2 16 19 3A 30 4D 0F DA 0B 19 3A 09 4D E6 07 FE 04 C8 C3 40 19 3A 08 4D E6 07 FE 04 C8 C3 40 19 DD 21 1C 4D CD 0F 20 E6 C0 D6 C0 20 2D 3A 30 4D 0F DA 35 19 3A 09 4D E6 07 FE 04 C8 C3 50 19 3A 08 4D E6 07 FE 04 C8 C3 50 19 2A 26 4D 22 1C 4D 05 CA 50 19 3A 3C 4D 32 30 4D DD 21 1C 4D FD 21 08 4D CD 00 20 3A 30 4D 0F DA 75 19 7D E6 07 FE 04 CA 85 19 DA 71 19 2D C3 85 19 2C C3 85 19 7C E6 07 FE 04 CA 85 19 DA 84 19 25 C3 85 19 24 22 08 4D CD 18 20 22 39 4D DD 21 BF 4D DD 7E 00 DD 36 00 00 A7 C0 3A D2 4D A7 28 2C 3A D4 4D A7 28 26 2A 08 4D 11 94 80 A7 ED 52 20 1B 06 19 4F CD 42 00 0E 15 81 4F 06 1C CD 42 00 CD 04 10 F7 54 05 00 21 BC 4E CB D6 3E FF 32 9D 4D 2A 39 4D CD 65 00 7E FE 10 28 03 FE 14 C0 DD 21 0E 4E DD 34 00 E6 0F CB 3F 06 40 70 06 19 4F CB 39 CD 42 00 3C FE 01 CA FD 19 87 32 9D 4D CD 08 1B CD 6A 1A 21 BC 4E 3A 0E 4E 0F 38 05 CB C6 CB 8E C9 CB 86 CB CE C9 21 1C 4D 7E A7 CA 2E 1A 3A 08 4D E6 07 FE 04 CA 38 1A C3 5C 1A 3A 09 4D E6 07 FE 04 C2 5C 1A 3E 05 CD D0 1E 38 03 EF 17 00 DD 21 26 4D FD 21 12 4D CD 00 20 22 12 4D 2A 26 4D 22 1C 4D 3A 3C 4D 32 30 4D DD 21 1C 4D FD 21 08 4D CD 00 20 C3 85 19 3A 9D 4D FE 06 C0 2A BD 4D 22 CB 4D 3E 01 32 A6 4D 32 A7 4D 32 A8 4D 32 A9 4D 32 AA 4D 32 B1 4D 32 B2 4D 32 B3 4D 32 B4 4D 32 B5 4D AF 32 C8 4D 32 D0 4D DD 21 00 4C DD 36 02 1C DD 36 04 1C DD 36 06 1C DD 36 08 1C DD 36 03 11 DD 36 05 11 DD 36 07 11 DD 36 09 11 21 AC 4E CB EE CB BE C9 2A 03 33 3E 02 32 3C 4D 22 26 4D 06 00 C3 E4 18 2A FF 32 AF 32 3C 4D 22 26 4D 06 00 C3 E4 18 2A 05 33 3E 03 32 3C 4D 22 26 4D 06 00 C3 E4 18 2A 01 33 3E 01 32 3C 4D 22 26 4D 06 00 C3 E4 18 3A 12 4E A7 CA 14 1B 21 9F 4D 34 C9 3A A3 4D A7 C0 3A A2 4D A7 CA 25 1B 21 11 4E 34 C9 3A A1 4D A7 CA 31 1B 21 10 4E 34 C9 21 0F 4E 34 C9 3A A0 4D A7 C8 3A AC 4D A7 C0 CD D7 20 2A 31 4D 01 99 4D CD 5A 20 3A 99 4D A7 CA 6A 1B 2A 60 4D 29 22 60 4D 2A 5E 4D ED 6A 22 5E 4D D0 21 60 4D 34 C3 D8 1B 3A A7 4D A7 CA 88 1B 2A 5C 4D 29 22 5C 4D 2A 5A 4D ED 6A 22 5A 4D D0 21 5C 4D 34 C3 D8 1B 3A B7 4D A7 CA A6 1B 2A 50 4D 29 22 50 4D 2A 4E 4D ED 6A 22 4E 4D D0 21 50 4D 34 C3 D8 1B 3A B6 4D A7 CA C4 1B 2A 54 4D 29 22 54 4D 2A 52 4D ED 6A 22 52 4D D0 21 54 4D 34 C3 D8 1B 2A 58 4D 29 22 58 4D 2A 56 4D ED 6A 22 56 4D D0 21 58 4D 34 21 14 4D 7E A7 CA ED 1B 3A 00 4D E6 07 FE 04 CA F7 1B C3 36 1C 3A 01 4D E6 07 FE 04 C2 36 1C 3E 01 CD D0 1E 38 1B 3A A7 4D A7 CA 0B 1C EF 0C 00 C3 19 1C 2A 0A 4D CD 52 20 7E FE 1A 28 03 EF 08 00 CD FE 1E DD 21 1E 4D FD 21 0A 4D CD 00 20 22 0A 4D 2A 1E 4D 22 14 4D 3A 2C 4D 32 28 4D DD 21 14 4D FD 21 00 4D CD 00 20 22 00 4D CD 18 20 22 31 4D C9 3A A1 4D FE 01 C0 3A AD 4D A7 C0 2A 33 4D 01 9A 4D CD 5A 20 3A 9A 4D A7 CA 7D 1C 2A 6C 4D 29 22 6C 4D 2A 6A 4D ED 6A 22 6A 4D D0 21 6C 4D 34 C3 AF 1C 3A A8 4D A7 CA 9B 1C 2A 68 4D 29 22 68 4D 2A 66 4D ED 6A 22 66 4D D0 21 68 4D 34 C3 AF 1C 2A 64 4D 29 22 64 4D 2A 62 4D ED 6A 22 62 4D D0 21 64 4D 34 21 16 4D 7E A7 CA C4 1C 3A 02 4D E6 07 FE 04 CA CE 1C C3 0D 1D 3A 03 4D E6 07 FE 04 C2 0D 1D 3E 02 CD D0 1E 38 1B 3A A8 4D A7 CA E2 1C EF 0D 00 C3 F0 1C 2A 0C 4D CD 52 20 7E FE 1A 28 03 EF 09 00 CD 25 1F DD 21 20 4D FD 21 0C 4D CD 00 20 22 0C 4D 2A 20 4D 22 16 4D 3A 2D 4D 32 29 4D DD 21 16 4D FD 21 02 4D CD 00 20 22 02 4D CD 18 20 22 33 4D C9 3A A2 4D FE 01 C0 3A AE 4D A7 C0 2A 35 4D 01 9B 4D CD 5A 20 3A 9B 4D A7 CA 54 1D 2A 78 4D 29 22 78 4D 2A 76 4D ED 6A 22 76 4D D0 21 78 4D 34 C3 86 1D 3A A9 4D A7 CA 72 1D 2A 74 4D 29 22 74 4D 2A 72 4D ED 6A 22 72 4D D0 21 74 4D 34 C3 86 1D 2A 70 4D 29 22 70 4D 2A 6E 4D ED 6A 22 6E 4D D0 21 70 4D 34 21 18 4D 7E A7 CA 9B 1D 3A 04 4D E6 07 FE 04 CA A5 1D C3 E4 1D 3A 05 4D E6 07 FE 04 C2 E4 1D 3E 03 CD D0 1E 38 1B 3A A9 4D A7 CA B9 1D EF 0E 00 C3 C7 1D 2A 0E 4D CD 52 20 7E FE 1A 28 03 EF 0A 00 CD 4C 1F DD 21 22 4D FD 21 0E 4D CD 00 20 22 0E 4D 2A 22 4D 22 18 4D 3A 2E 4D 32 2A 4D DD 21 18 4D FD 21 04 4D CD 00 20 22 04 4D CD 18 20 22 35 4D C9 3A A3 4D FE 01 C0 3A AF 4D A7 C0 2A 37 4D 01 9C 4D CD 5A 20 3A 9C 4D A7 CA 2B 1E 2A 84 4D 29 22 84 4D 2A 82 4D ED 6A 22 82 4D D0 21 84 4D 34 C3 5D 1E 3A AA 4D A7 CA 49 1E 2A 80 4D 29 22 80 4D 2A 7E 4D ED 6A 22 7E 4D D0 21 80 4D 34 C3 5D 1E 2A 7C 4D 29 22 7C 4D 2A 7A 4D ED 6A 22 7A 4D D0 21 7C 4D 34 21 1A 4D 7E A7 CA 72 1E 3A 06 4D E6 07 FE 04 CA 7C 1E C3 BB 1E 3A 07 4D E6 07 FE 04 C2 BB 1E 3E 04 CD D0 1E 38 1B 3A AA 4D A7 CA 90 1E EF 0F 00 C3 9E 1E 2A 10 4D CD 52 20 7E FE 1A 28 03 EF 0B 00 CD 73 1F DD 21 24 4D FD 21 10 4D CD 00 20 22 10 4D 2A 24 4D 22 1A 4D 3A 2F 4D 32 2B 4D DD 21 1A 4D FD 21 06 4D CD 00 20 22 06 4D CD 18 20 22 37 4D C9 87 4F 06 00 21 09 4D 09 7E FE 1D C2 E3 1E 36 3D C3 FC 1E FE 3E C2 ED 1E 36 1E C3 FC 1E 06 21 90 DA FC 1E 7E 06 3B 90 D2 FC 1E A7 C9 37 C9 3A B1 4D A7 C8 AF 32 B1 4D 21 FF 32 3A 28 4D EE 02 32 2C 4D 47 DF 22 1E 4D 3A 02 4E FE 22 C0 22 14 4D 78 32 28 4D C9 3A B2 4D A7 C8 AF 32 B2 4D 21 FF 32 3A 29 4D EE 02 32 2D 4D 47 DF 22 20 4D 3A 02 4E FE 22 C0 22 16 4D 78 32 29 4D C9 3A B3 4D A7 C8 AF 32 B3 4D 21 FF 32 3A 2A 4D EE 02 32 2E 4D 47 DF 22 22 4D 3A 02 4E FE 22 C0 22 18 4D 78 32 2A 4D C9 3A B4 4D A7 C8 AF 32 B4 4D 21 FF 32 3A 2B 4D EE 02 32 2F 4D 47 DF 22 24 4D 3A 02 4E FE 22 C0 22 1A 4D 78 32 2B 4D C9 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 5D E1"
PRNG_ROM_MEM = PRNG_ROM_MEM.split()

# Random direction associated to each combination of 2 least significant bits.
PRNG_BITS_TO_DIRECTION = [Vector2.RIGHT, Vector2.DOWN, Vector2.LEFT, Vector2.UP]

# --------------------------------------------------------------------