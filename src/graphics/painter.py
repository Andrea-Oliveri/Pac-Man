# -*- coding: utf-8 -*-

import pyglet.gl

from src.constants import (MAZE_START_IMAGE,
                           MAZE_TILE_PX_SIZE,
                           MAZE_TILES_ROWS,
                           MAZE_START_IMAGE_EMPTY_TILE_REGION_COORDS,
                           FontColors,
                           GAME_HIGH_SCORE_TEXT_COORDS,
                           GAME_1UP_TEXT_COORDS,
                           GAME_SCORE_NUMBER_COORDS,
                           GAME_HIGH_SCORE_NUMBER_COORDS,
                           MAX_SCORE_NUM_DIGITS,
                           GAME_DEFAULT_TEXT_COLOR,
                           UI_TILES_SHEET_PATH,
                           UI_TILES_PX_SIZE,
                           Fruits,
                           LIFE_ICON_UI,
                           GAME_LEFT_LIVES_ICON_COORDS,
                           GAME_RIGHT_FRUIT_ICON_COORDS,
                           GAME_MAX_FRUIT_ICON_NUMBER,
                           FRUIT_OF_LEVEL,
                           FRUIT_SPAWN_POSITION)
from src.directions import Vector2
from src.graphics import utils
from src.graphics.font import Font
from src.graphics.ghost_sprites import GhostSprite
from src.graphics.pacman_sprites import PacManSprite



class Painter:
    
    def __init__(self):
        # Load animated sprites.
        self._pacman_sprites = PacManSprite()
        self._ghost_sprites  = GhostSprite()

        # Load UI elements.
        self._font = Font()
        self._ui_tiles = utils.load_image_grid(UI_TILES_SHEET_PATH, UI_TILES_PX_SIZE)

        # Load maze and reset child attributes.
        self.new_level()        
    

    def draw_menu(self):
        # TODO: better menu
        image = utils.load_image(r".\assets\images\TMP-Menu.png")

        image.blit(0, 0)


    def update(self, pacman):
        self._pacman_sprites.update(pacman)
        self._ghost_sprites .update()


    def new_level(self):
        # Load initial maze image.
        self._maze_image = utils.load_image(MAZE_START_IMAGE)
        self._maze_empty_tile = self._maze_image.get_region(*MAZE_START_IMAGE_EMPTY_TILE_REGION_COORDS, MAZE_TILE_PX_SIZE, MAZE_TILE_PX_SIZE)

        # Reset sprite counters.
        self._pacman_sprites.reset()
        self._ghost_sprites .reset()
        

    def draw_game(self, pacman, ghosts, score, lives, level, fruit_active):

        self._maze_image.blit(0, 0)

        self._draw_gui(score, lives, level)

        self._pacman_sprites.draw(pacman)

        self._ghost_sprites.draw(ghosts)

        if fruit_active:
            self._draw_fruit(level)

        return
        # ----------------------------------------
        # DEBUG
        # ----------------------------------------
        pacman_coords = utils.calculate_coords_sprites(pacman.position)

        for c in range(-160, 160, 8):
            pyglet.shapes.Line(c, -160, c, 160, width=1, color=(155, 0, 0)).draw()
            pyglet.shapes.Line(-160, c-4, 160, c-4, width=1, color=(155, 0, 0)).draw()
        pyglet.shapes.Circle(pacman_coords.x, pacman_coords.y, 2, color = (0, 155, 0)).draw()
        for g in ghosts:
            g_coords = utils.calculate_coords_sprites(g.position)
            pyglet.shapes.Circle(g_coords.x, g_coords.y, 2, color = (0, 155, 0)).draw()
        
        origin = utils.calculate_coords_sprites(Vector2.NULL)
        pyglet.shapes.Circle(origin.x, origin.y, 2, color = (255, 0, 0)).draw()
      
        from src.constants import GHOSTS_EATEN_TARGET_TILE
        coords = utils.calculate_coords_sprites(GHOSTS_EATEN_TARGET_TILE)
        pyglet.shapes.Star(coords.x, coords.y, 5, 2, 4, color = (0, 255, 0)).draw()
        # ----------------------------------------


    def notify_fright_on(self, fright_duration, fright_flashes):
        self._ghost_sprites.notify_fright_on(fright_duration, fright_flashes)


    def _draw_gui(self, score, lives, level):
        # Print text on top of screen.
        self._font.print(*GAME_HIGH_SCORE_TEXT_COORDS, GAME_DEFAULT_TEXT_COLOR, 'HIGH SCORE')
        self._font.print(*GAME_1UP_TEXT_COORDS       , GAME_DEFAULT_TEXT_COLOR, '1UP')
        
        # Print score and high score numbers.
        high_score = score.high_score
        score      = score.score

        high_score = (''   if high_score == 0 else str(high_score)).rjust(MAX_SCORE_NUM_DIGITS, ' ')
        score      = ('00' if score      == 0 else str(score))     .rjust(MAX_SCORE_NUM_DIGITS, ' ')
        
        self._font.print(*GAME_HIGH_SCORE_NUMBER_COORDS, GAME_DEFAULT_TEXT_COLOR, high_score)
        self._font.print(*GAME_SCORE_NUMBER_COORDS     , GAME_DEFAULT_TEXT_COLOR, score)

        # Draw the lives.
        x, y = GAME_LEFT_LIVES_ICON_COORDS
        for _ in range(lives):
            self._ui_tiles[LIFE_ICON_UI].blit(x, y)
            x += UI_TILES_PX_SIZE

        # Draw the fruits.
        fruits = [FRUIT_OF_LEVEL(i) for i in range(level-GAME_MAX_FRUIT_ICON_NUMBER+1, level+1) if i >= 1]
        x, y = GAME_RIGHT_FRUIT_ICON_COORDS
        for fruit in fruits:
            self._ui_tiles[fruit].blit(x, y)
            x -= UI_TILES_PX_SIZE


    def _draw_fruit(self, level):
        fruit = FRUIT_OF_LEVEL(level) 
        fruit_coords = utils.calculate_coords_sprites(FRUIT_SPAWN_POSITION)
        self._ui_tiles[fruit].blit(fruit_coords.x, fruit_coords.y)


    def set_empty_tile(self, idx):
        maze_row, maze_col = idx

        destination_left_px   = maze_col * MAZE_TILE_PX_SIZE
        destination_bottom_px = (MAZE_TILES_ROWS - maze_row - 1) * MAZE_TILE_PX_SIZE

        source_texture      = self._maze_empty_tile.get_texture()
        destination_texture = self._maze_image.get_texture()

        pyglet.gl.glCopyImageSubData(source_texture.id,
 	                                 source_texture.target,
 	                                 source_texture.level,
                                     0,
                                     0,
                                     0,
                                     destination_texture.id,
                                     destination_texture.target,
                                     destination_texture.level,
                                     destination_left_px, 
                                     destination_bottom_px,
                                     0,
                                     source_texture.width,
                                     source_texture.height,
                                     1)