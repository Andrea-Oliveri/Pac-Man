# -*- coding: utf-8 -*-

import pyglet

from src.activities.menu import Menu
from src.activities.game import Game
from src.activities.game_completed import GameCompleted
from src.activities.intermission import Intermission
from src.graphics import Graphics
from src.sounds import Sounds
from src.constants import (WINDOW_INIT_KWARGS,
                           WINDOW_MINIMUM_SIZE,
                           GAME_TENTATIVE_UPDATES_INTERVAL,
                           WINDOW_ICON_PATH,
                           BACKGROUND_COLOR,
                           GAME_ORIGINAL_UPDATES_INTERVAL,
                           LAYOUT_PX_PER_UNIT_LENGHT,
                           LAYOUT_N_ROWS_TILES,
                           LAYOUT_N_COLS_TILES,
                           GAME_COMPLETED_LEVEL)


class Window(pyglet.window.Window):
    def __init__(self):
        super().__init__(**WINDOW_INIT_KWARGS, visible = False)

        self.set_minimum_size(*WINDOW_MINIMUM_SIZE)

        icon = pyglet.image.load(WINDOW_ICON_PATH)
        self.set_icon(icon)
        
        # Set background color.
        pyglet.gl.glClearColor(*BACKGROUND_COLOR, 1)
        self._first_time_drawing = True

        self._graphics = Graphics()
        self._sounds   = Sounds()

        self._current_activity = Menu(self._graphics, self._sounds)
        self._backup_activity = None # Used only to store Game activity during intermissions.

        # FPS locked to screen refresh rate (vsync enabled).
        # Number of updates per second can be freely chosen though.
        pyglet.clock.schedule_interval(self.on_state_update, GAME_TENTATIVE_UPDATES_INTERVAL)
        self._residual_update_interval = 0

        
    def on_resize(self, width, height):
        desired_width  = LAYOUT_N_COLS_TILES * LAYOUT_PX_PER_UNIT_LENGHT
        desired_height = LAYOUT_N_ROWS_TILES * LAYOUT_PX_PER_UNIT_LENGHT

        scale = min(width // desired_width, height // desired_height)
        viewport_width  = desired_width * scale
        viewport_height = desired_height * scale

        pad_x = (width  - viewport_width ) / 2
        pad_y = (height - viewport_height) / 2

        self.viewport = (pad_x, pad_y, viewport_width, viewport_height)
        
        return pyglet.event.EVENT_HANDLED   # Don't call the default handler


    def on_key_press(self, symbol, modifiers):
        self._current_activity.event_key_pressed(symbol, modifiers)

        # ------------------------------
        # DEBUG: slow down pacman
        # ------------------------------
        from pyglet.window import key

        if symbol == key.SPACE:
            import src.constants as const
            if not hasattr(self, '_original_speed'):
                self._original_speed = float(const.REFERENCE_SPEED)
            const.REFERENCE_SPEED = self._original_speed if const.REFERENCE_SPEED < self._original_speed else self._original_speed * 0.1

        # ------------------------------

        # --------------------------------------
        # DEBUG: single-tick game update
        # --------------------------------------

        from pyglet.window import key

        if symbol == key.P:
            self.paused = True if not hasattr(self, 'paused') else not self.paused
        if symbol == key.O:
            self.on_state_update_step()
        # --------------------------------------

        # --------------------------------------
        # DEBUG: force state on ghosts
        # --------------------------------------

        from pyglet.window import key
        from src.constants import MazeTiles

        if isinstance(self._current_activity, Game):
            if symbol == key._1:
                self._current_activity._pellet_eaten(MazeTiles.POWER_PELLET)
            if symbol == key._2:
                self._current_activity._level += 1
            if symbol == key._3:
                self._current_activity._maze._n_pellets = 0

        # --------------------------------------




    def on_state_update(self, dt):
        # --------------------------------------
        # DEBUG
        # --------------------------------------

        if hasattr(self, 'paused') and self.paused:
            return

        # --------------------------------------


        # Force updates to happen with the same frame-rate as in the original game.
        self._residual_update_interval += dt

        while self._residual_update_interval >= GAME_ORIGINAL_UPDATES_INTERVAL:
            self._residual_update_interval -= GAME_ORIGINAL_UPDATES_INTERVAL

            self.on_state_update_step()



    def on_state_update_step(self):
        
        retval = self._current_activity.event_update_state()

        if retval is False:
            return

        retval_destruction = self._current_activity.notify_destruction()

        if isinstance(self._current_activity, Menu):
            # retval is True if we need to change from Menu to Game.
            self._current_activity = Game(self._graphics, self._sounds)

        elif isinstance(self._current_activity, Game):
            if retval is True:
                # retval is True if we need to change from Game to Menu.
                self._current_activity = Menu(self._graphics, self._sounds)
            # retval is an integer representing the game level.
            elif retval == GAME_COMPLETED_LEVEL:
                self._current_activity = GameCompleted(self._graphics, self._sounds, **retval_destruction)
            # It must be time for an intermission.
            else:
                self._backup_activity  = self._current_activity
                self._current_activity = Intermission(self._graphics, self._sounds, retval)

        elif isinstance(self._current_activity, Intermission):
            self._current_activity = self._backup_activity
            self._backup_activity  = None

        elif isinstance(self._current_activity, GameCompleted):
            self._current_activity = Menu(self._graphics, self._sounds)

        
    def on_draw(self):
        if self._first_time_drawing:
            self.set_visible(True)
            self._first_time_drawing = False
        
        self.clear()
        self._current_activity.event_draw_screen()


        return
        # -------- DEBUG: FPS DISPLAY ----------
        if not hasattr(self, 'fps_display'):
            self.fps_display = pyglet.window.FPSDisplay(window=self)
            self.fps_display.label = pyglet.text.Label('', x=185, y=285, font_size=12, weight=True, color = (255, 0, 0, 255))

        self.fps_display.draw()
        from src.graphics import utils
        utils.enable_transparency_blit()
        # ---------------------------------------
