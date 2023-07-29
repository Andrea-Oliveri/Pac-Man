# -*- coding: utf-8 -*-

from pyglet.window import Window
from enum import IntEnum

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

# Approximate number of times to update game state per second.
GAME_UPDATES_PER_SEC = 100

# Constant defining where the image are stored.
WINDOW_ICON_PATH = "./assets/images/icon.ico"

# --------------------------------------------------------------------


# --------------------------------------------------------------------
# Constants related to the maze.
# --------------------------------------------------------------------

# Enum defining types of tiles.
MazeTiles = IntEnum('MazeTiles', ['WALL', 'EMPTY', 'PELLET', 'POWER_PELLET'])

# Location of image with maze starting configuration and coordinates (left, bottom pixel) of an empty tile in the initial maze.
MAZE_START_IMAGE = "./assets/images/Maze Initial.png"
MAZE_START_IMAGE_EMPTY_TILE_REGION_COORDS = (0, 120)

# Size of maze tiles expressed in pixels.
MAZE_TILE_PX_SIZE = 8

# Initial maze design expressed as a 1D array of tile indices.
MAZE_START_TILES = (MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.POWER_PELLET, MazeTiles.WALL, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.WALL, MazeTiles.POWER_PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.EMPTY, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.EMPTY, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.EMPTY, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.EMPTY, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.EMPTY, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.EMPTY, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.EMPTY, MazeTiles.WALL, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.WALL, MazeTiles.EMPTY, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.PELLET, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.WALL, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.WALL, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.PELLET, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.EMPTY, MazeTiles.WALL, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.WALL, MazeTiles.EMPTY, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.EMPTY, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.EMPTY, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.EMPTY, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.EMPTY, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.EMPTY, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.EMPTY, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.POWER_PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.EMPTY, MazeTiles.EMPTY, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.POWER_PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.PELLET, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL, MazeTiles.WALL)

# Dimentions of maze expressed in number of tiles.
MAZE_TILES_COLS = 28
MAZE_TILES_ROWS = 31

# --------------------------------------------------------------------


# --------------------------------------------------------------------
# Constants related to the animated sprites.
# --------------------------------------------------------------------

# Paths of images containing the sprite sheets for the animations.
PACMAN_MOVE_ANIMATION  = "./assets/images/Pac-Man Movement Animation Sequence.png"
PACMAN_DEATH_ANIMATION = "./assets/images/Pac-Man Death Animation Sequence.png"

# Duration of each frame in the animations, in seconds.
ANIMATION_PERIOD_SECS = 0.033333

# Size of Pac-Man and Ghost sprites expressed in pixels.
PACMAN_GHOSTS_SPRITES_PX_SIZE = 16

# Index of frame in PACMAN_MOVE_ANIMATION to use when Pac-Man is stuck.
PACMAN_STUCK_FRAME_IDX = 2


# --------------------------------------------------------------------


# --------------------------------------------------------------------
# Constants related to Pac-Man.
# --------------------------------------------------------------------

# Pac-Man states.
PacManStates = IntEnum('PacManStates', ['SPAWNING', 'MOVING', 'STUCK', 'DEAD'])

# Speed at which Pac-Man moves.
PACMAN_MOVE_SPEED_TILES = 11 * 0.1

# Coordinates of tile where Pac-Man starts the game.
PACMAN_START_TILE = (14, 23.5)

# --------------------------------------------------------------------



