# -*- coding: utf-8 -*-

from pyglet.window import Window
from enum import IntEnum
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
GAME_UPDATES_INTERVAL = 1 / 100

# Constant defining where the image are stored.
WINDOW_ICON_PATH = "./assets/images/icon.ico"

# --------------------------------------------------------------------


# --------------------------------------------------------------------
# Constants related to the maze.
# --------------------------------------------------------------------

# Enum defining types of tiles.
MazeTiles = IntEnum('MazeTiles', ['WALL', 'EMPTY', 'PELLET', 'POWER_PELLET'])

# Location of image with maze starting configuration.
MAZE_START_IMAGE = "./assets/images/Maze Initial.png"

# Coordinates (left pixel counting from left, bottom pixel counting from bottom) of an empty tile in the initial maze.
MAZE_START_IMAGE_EMPTY_TILE_REGION_COORDS = (0, 128)

# Size of maze tiles expressed in pixels.
MAZE_TILE_PX_SIZE = 8

# Initial maze design expressed as a 1D array of tile indices.
MAZE_START_TILES = (MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.POWER_PELLET, MazeTiles.WALL, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.WALL, MazeTiles.POWER_PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.EMPTY, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.EMPTY, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.EMPTY, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.EMPTY, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.EMPTY, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.EMPTY, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.EMPTY, MazeTiles.WALL, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.WALL, MazeTiles.EMPTY, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.PELLET, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.WALL, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.WALL, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.PELLET, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.EMPTY, MazeTiles.WALL, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.WALL, MazeTiles.EMPTY, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.EMPTY, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.EMPTY, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.EMPTY, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.EMPTY, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.EMPTY, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.EMPTY, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.POWER_PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.POWER_PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL)

# Dimentions of maze expressed in number of tiles.
MAZE_TILES_COLS = 28
MAZE_TILES_ROWS = 31

# Warp tunnel tiles.
WARP_TUNNEL_ROW = 14
WARP_TUNNEL_TELEPORT_MARGIN = 2

# --------------------------------------------------------------------


# --------------------------------------------------------------------
# Constants related to the animated sprites.
# --------------------------------------------------------------------

# Paths of images containing the sprite sheets for the animations.
PACMAN_MOVE_ANIMATION  = "./assets/images/Pac-Man Movement Animation Sequence.png"
PACMAN_DEATH_ANIMATION = "./assets/images/Pac-Man Death Animation Sequence.png"

# Duration of each frame in the animations, in seconds.
PACMAN_MOVE_ANIMATION_PERIOD_SECS  = 2 / 60
PACMAN_DEATH_ANIMATION_PERIOD_SECS = 10 / 60

# Size of Pac-Man and Ghost sprites expressed in pixels.
PACMAN_GHOSTS_SPRITES_PX_SIZE = 16

# Index of frame in PACMAN_MOVE_ANIMATION to use when Pac-Man is stuck.
PACMAN_STUCK_FRAME_IDX = 1

# Index of frame in PACMAN_MOVE_ANIMATION to use when Pac-Man is spawning.
PACMAN_SPAWNING_FRAME_IDX = 0

# --------------------------------------------------------------------


# --------------------------------------------------------------------
# Constants related to the font.
# --------------------------------------------------------------------

# Path of image containing the font sheet.
FONT_SHEET_PATH = "./assets/images/Font.png"

# Size of font tiles expressed in pixels.
FONT_TILE_PX_SIZE = 8

# Colors present, ordered as in the font sheet (ordered from bottom to top due to how pyglet increases y-axis).
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
PACMAN_START_TILE = (14, 23.5)

# One-frame penalty when eating pellet, 3 frames penalty when eating power pellet (in original game frame-rate: 60 fps).
PACMAN_PELLET_PENALTIES = {MazeTiles.PELLET: 1 / 60, MazeTiles.POWER_PELLET: 3 / 60}

# --------------------------------------------------------------------


# --------------------------------------------------------------------
# Constants related to speed of Pac-Man and Ghosts.
# --------------------------------------------------------------------

# Maximum Pac-Man move speed.
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

# Function returning the Ghost speed depending on the current level, if fright is on and if ghost is in warp tunnel.
def GHOSTS_SPEED(level, fright, tunnel):
    multiplier = None

    if level == 1:
        multiplier = 0.40 if tunnel else 0.50 if fright else 0.75
    elif level <= 4:
        multiplier = 0.45 if tunnel else 0.55 if fright else 0.85
    elif level <= 20:
        multiplier = 0.50 if tunnel else 0.60 if fright else 0.95
    else:
        multiplier = 0.50 if tunnel else 0.95

    return multiplier * REFERENCE_SPEED


# --------------------------------------------------------------------


# --------------------------------------------------------------------
# Constants related to Game UI.
# --------------------------------------------------------------------

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
    if level == 1:
        return 100
    elif level == 2:
        return 300
    elif level <= 4:
        return 500
    elif level <= 6:
        return 700
    elif level <= 8:
        return 1000
    elif level <= 10:
        return 2000
    elif level <= 12:
        return 3000

    return 5000

# Path of file where to store high score.
HIGH_SCORE_FILE = os.path.join(os.path.expanduser('~'), '.pacman_game')
HIGH_SCORE_FILE_NUM_BYTES = 4

# --------------------------------------------------------------------


