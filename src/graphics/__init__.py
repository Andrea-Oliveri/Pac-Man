# -*- coding: utf-8 -*-


from src.constants import (DynamicUIElements,
                           LAYOUT_RECORDINS_COORDS,
                           Z_COORD_RECORDING)
from src.graphics import utils
from src.graphics.painter import Painter
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

        # Instanciate object to render using shaders.
        self._painter = Painter()

        # Load sprite coordinators.
        self._pacman_sprite = PacManSprite(self._painter)
        self._ghost_sprite  = GhostSprite (self._painter)
        self._maze_sprite   = MazeSprite  (self._painter)
        self._score_sprite  = ScoreSprite (self._painter)
        self._ui_sprite     = UiSprite    (self._painter)


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

        self._painter.draw()


    def notify_fright_on(self, fright_duration, fright_flashes):
        self._ghost_sprite.notify_fright_on(fright_duration, fright_flashes)

    def notify_fruit_eaten(self, score):
        self._score_sprite.notify_fruit_eaten(score)

    def notify_ghost_eaten(self, score, position):
        self._score_sprite.notify_ghost_eaten(score, position)

    def notify_level_end(self):
        self._maze_sprite.notify_level_end()



    def recording_load(self, path, width, height):
        self._active_recording = utils.load_recording(path, width, height)

        return len(self._active_recording)

    def recording_draw(self, idx, level_to_draw_fruits = None):
        frame = self._active_recording[idx]

        self._painter.set_texture(frame)
        self._painter.add_quad(*LAYOUT_RECORDINS_COORDS, 0, 0, frame.width, frame.height, Z_COORD_RECORDING)
        self._painter.draw()

        if level_to_draw_fruits is not None:
            self._painter.set_texture()
            self._ui_sprite.draw_fruits(level_to_draw_fruits)
            self._painter.draw()

    def recording_free(self):
        self._active_recording = None
        self._painter.set_texture()
