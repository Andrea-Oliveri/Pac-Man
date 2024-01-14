# -*- coding: utf-8 -*-

import lzma

from src.constants import DynamicUIElements
from src.graphics import utils
from src.graphics.sprites.ghost_sprite import GhostSprite
from src.graphics.sprites.maze_sprite import MazeSprite
from src.graphics.sprites.pacman_sprite import PacManSprite
from src.graphics.sprites.score_sprite import ScoreSprite
from src.graphics.sprites.ui_sprite import UiSprite



class Graphics:
    
    def __init__(self):

        # Enable transparency for sprites.
        utils.enable_transparency_blit()

        # Enable depth testing to draw stuff on top of each other.
        utils.enable_depth_testing()

        # Variable holding the recording currently being displayed on screen.
        self._active_recording = None

        # Load sprite coordinators.
        self._pacman_sprite = PacManSprite()
        self._ghost_sprite  = GhostSprite()
        self._maze_sprite   = MazeSprite()
        self._score_sprite  = ScoreSprite()
        self._ui_sprite     = UiSprite()


    def reset_level(self):
        self._pacman_sprite.reset()
        self._ghost_sprite .reset()
        self._maze_sprite  .reset()
        self._score_sprite .reset()
        self._ui_sprite    .reset()


    def update(self, pacman, update_only_scores = False):
        self._score_sprite .update()

        if update_only_scores:
            return

        self._pacman_sprite.update(pacman)
        self._ghost_sprite .update()
        self._maze_sprite  .update()
        self._ui_sprite    .update()


    def draw_game(self, maze, pacman, ghosts, score, lives, level, ui_elements):

        self._maze_sprite.send_vertex_data(maze)
        self._ui_sprite  .send_vertex_data(DynamicUIElements.READY_TEXT      in ui_elements,
                                           DynamicUIElements.PLAYER_ONE_TEXT in ui_elements,
                                           DynamicUIElements.GAME_OVER_TEXT  in ui_elements,
                                           DynamicUIElements.FRUIT           in ui_elements,
                                           score.score,
                                           score.high_score,
                                           lives,
                                           level)

        if DynamicUIElements.GHOSTS in ui_elements:
            self._ghost_sprite .send_vertex_data(ghosts)

        if DynamicUIElements.ACTION_SCORES in ui_elements:
            self._score_sprite .send_vertex_data()
            
        if DynamicUIElements.PACMAN in ui_elements:
            self._pacman_sprite.send_vertex_data(pacman)

        
        # ----------------------------------------
        # DEBUG
        # ----------------------------------------
        return
        import pyglet 

        for c in range(-160, 160, 8):
            pyglet.shapes.Line(c, -160, c, 160, width=1, color=(155, 0, 0)).draw()
            pyglet.shapes.Line(-160, c-4, 160, c-4, width=1, color=(155, 0, 0)).draw()

        if pacman is not None:
            pacman_coords = utils.calculate_coords_sprites(pacman.position)
            pyglet.shapes.Circle(pacman_coords.x, pacman_coords.y, 2, color = (0, 155, 0)).draw()
        
        if ghosts is not None:
            for g in ghosts:
                g_coords = utils.calculate_coords_sprites(g.position)
                pyglet.shapes.Circle(g_coords.x, g_coords.y, 2, color = (0, 155, 0)).draw()
        
        from src.directions import Vector2
        origin = utils.calculate_coords_sprites(Vector2.NULL)
        pyglet.shapes.Circle(origin.x, origin.y, 2, color = (255, 0, 0)).draw()
      
        from src.constants import GHOSTS_EATEN_TARGET_TILE
        coords = utils.calculate_coords_sprites(GHOSTS_EATEN_TARGET_TILE)
        pyglet.shapes.Star(coords.x, coords.y, 5, 2, 4, color = (0, 255, 0)).draw()
        # ----------------------------------------


    def notify_fright_on(self, fright_duration, fright_flashes):
        self._ghost_sprite.notify_fright_on(fright_duration, fright_flashes)

    def notify_fruit_eaten(self, score):
        self._score_sprite.notify_fruit_eaten(score)

    def notify_ghost_eaten(self, score, position):
        self._score_sprite.notify_ghost_eaten(score, position)

    def notify_level_end(self):
        self._maze_sprite.notify_level_end()



    def recording_load(self, path, width, height):
        with lzma.open(path, 'r') as file:
            self._active_recording = utils.load_image_grid(path, width, height, file)

        return len(self._active_recording)

    def recording_draw(self, idx, level_to_draw_fruits = None):
        self._active_recording[idx].blit(0, 0)

        if level_to_draw_fruits is not None:
            self._draw_fruits(level_to_draw_fruits)

    def recording_free(self):
        self._active_recording = None