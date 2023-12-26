# -*- coding: utf-8 -*-

from src.constants import (FontColors,
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
                           FRUIT_SPAWN_POSITION,
                           LEVEL_PLAYER_ONE_TEXT_COORDS,
                           LEVEL_PLAYER_ONE_TEXT_COLOR,
                           LEVEL_READY_TEXT_COORDS,
                           LEVEL_READY_TEXT_COLOR,
                           LEVEL_GAME_OVER_TEXT_COORDS,
                           LEVEL_GAME_OVER_TEXT_COLOR,
                           DynamicUIElements)
from src.directions import Vector2
from src.graphics import utils
from src.graphics.font import Font
from src.graphics.maze_sprites import MazeSprite
from src.graphics.ghost_sprites import GhostSprite
from src.graphics.pacman_sprites import PacManSprite



class Painter:
    
    def __init__(self):

        # Enable transparency for sprites.
        utils.enable_transparency_blit()

        # Load animated sprites.
        self._pacman_sprites = PacManSprite()
        self._ghost_sprites  = GhostSprite()
        self._maze_sprites   = MazeSprite()

        # Load UI elements.
        self._font = Font()
        self._ui_tiles = utils.load_image_grid(UI_TILES_SHEET_PATH, UI_TILES_PX_SIZE)

        # Reset child attributes.
        self.reset_level(new = True)

        # variable holding the recording currently being displayed on screen.
        self._active_recording = None


    def reset_level(self, new):
        # Load initial maze image.
        if new:
            self._maze_sprites.reset()

        # Reset sprite counters.
        self._pacman_sprites.reset()
        self._ghost_sprites .reset()
        

    def update(self, pacman):
        self._maze_sprites  .update()
        self._pacman_sprites.update(pacman)
        self._ghost_sprites .update()


    def draw_game(self, pacman, ghosts, score, lives, level, ui_elements):

        self._maze_sprites.draw()
        
        self._draw_gui(score, lives, level)

        if DynamicUIElements.READY_TEXT in ui_elements:
            self._font.print(*LEVEL_READY_TEXT_COORDS     , LEVEL_READY_TEXT_COLOR     , 'READY!')

        if DynamicUIElements.PLAYER_ONE_TEXT in ui_elements:
            self._font.print(*LEVEL_PLAYER_ONE_TEXT_COORDS, LEVEL_PLAYER_ONE_TEXT_COLOR, 'PLAYER ONE')

        if DynamicUIElements.GAME_OVER_TEXT in ui_elements:
            self._font.print(*LEVEL_GAME_OVER_TEXT_COORDS , LEVEL_GAME_OVER_TEXT_COLOR , 'GAME  OVER')

        if DynamicUIElements.FRUIT in ui_elements:
            self._draw_fruit(level)

        if DynamicUIElements.GHOSTS in ui_elements:
            self._ghost_sprites.draw(ghosts)

        if DynamicUIElements.PACMAN in ui_elements:
            self._pacman_sprites.draw(pacman)

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


    def set_empty_tile(self, maze_row, maze_col):
        self._maze_sprites.set_empty_tile(maze_row, maze_col)

    def notify_level_end(self):
        self._maze_sprites.notify_level_end()

    def recording_load(self, path, width, height):
        self._active_recording = utils.load_image_grid(path, width, height)
        return len(self._active_recording)

    def recording_draw(self, idx):
        self._active_recording[idx].blit(0, 0)

    def recording_free(self):
        self._active_recording = None
