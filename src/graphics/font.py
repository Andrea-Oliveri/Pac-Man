# -*- coding: utf-8 -*-

import pyglet.image

from src.constants import (FONT_SHEET_PATH,
                           FONT_TILE_PX_SIZE,
                           FontColors,
                           FONT_SHEET_CHARACTERS)
from src.graphics import utils


class Font:

    def __init__(self):
        # Load grid.
        image_grid = utils.load_image_grid(FONT_SHEET_PATH, FONT_TILE_PX_SIZE)

        # Split into regions for each character and group them in dictionaries for faster access.
        iterator = iter(image_grid)
        self._char_tiles = [{char: tile for char, tile in zip(FONT_SHEET_CHARACTERS, iterator)} for color in FontColors]


    def print(self, x, y, color, text):        
        if color not in FontColors:
            raise ValueError(f'Invalid color provided to Font.print: {color}')

        x_start = x

        for char in text:
            if char == '\n':
                y -= FONT_TILE_PX_SIZE
                x = x_start
                continue

            self._char_tiles[color][char].blit(x, y)
            x += FONT_TILE_PX_SIZE