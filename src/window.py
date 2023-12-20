# -*- coding: utf-8 -*-

import pyglet

from src.activities.menu import Menu
from src.activities.game import Game
from src.graphics.painter import Painter
from src.constants import (WINDOW_INIT_KWARGS,
                           WINDOW_MINIMUM_SIZE,
                           GAME_TENTATIVE_UPDATES_INTERVAL,
                           WINDOW_ICON_PATH,
                           GAME_ORIGINAL_UPDATES_INTERVAL)


class Window(pyglet.window.Window):
    def __init__(self):
        super().__init__(**WINDOW_INIT_KWARGS)
        
        self.set_minimum_size(*WINDOW_MINIMUM_SIZE)

        icon = pyglet.image.load(WINDOW_ICON_PATH)
        self.set_icon(icon)
        
        self.painter = Painter()

        self._current_activity = Menu(self.painter)
        
        # FPS locked to screen refresh rate (vsync enabled).
        # Number of updates per second can be freely chosen though.
        pyglet.clock.schedule_interval(self.on_state_update, GAME_TENTATIVE_UPDATES_INTERVAL)
        self._residual_update_interval = 0

        
    def on_resize(self, width, height):
        desired_width, desired_height = WINDOW_MINIMUM_SIZE

        scale = min(width // desired_width, height // desired_height)
        viewport_width  = desired_width * scale
        viewport_height = desired_height * scale

        pad_x = (width  - viewport_width ) / 2
        pad_y = (height - viewport_height) / 2

        self.viewport = (pad_x, pad_y, viewport_width, viewport_height)

        x_max = desired_width  / 2
        y_max = desired_height / 2

        self.projection = pyglet.math.Mat4.orthogonal_projection(-x_max, +x_max, -y_max, +y_max, -255, 255)
        
        return pyglet.event.EVENT_HANDLED   # Don't call the default handler


    def on_key_press(self, symbol, modifiers):
        self._current_activity.event_key_pressed(symbol, modifiers)

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

        if symbol == key._1:
            self._current_activity._pellet_eaten((23, 1), MazeTiles.POWER_PELLET)
        # --------------------------------------




    def on_state_update(self, dt):
        if hasattr(self, 'paused') and self.paused:
            return

        # -------- DEBUG: TEMP BENCHMARK CODE ----------
        self.benchmark_dts = self.benchmark_dts if hasattr(self, 'benchmark_dts') else []
        self.benchmark_dts.append(dt)

        import time
        self.time_to_update = self.time_to_update if hasattr(self, 'time_to_update') else []
        self.time_to_update.append(time.time())
        # ---------------------------------------



        
        # Force updates to happen with the same frame-rate as in the original game.
        self._residual_update_interval += dt

        while self._residual_update_interval >= GAME_ORIGINAL_UPDATES_INTERVAL:
            self._residual_update_interval -= GAME_ORIGINAL_UPDATES_INTERVAL

            self.on_state_update_step()


        # -------- DEBUG: TEMP BENCHMARK CODE ----------
        self.time_to_update[-1] = time.time() - self.time_to_update[-1]


        if len(self.benchmark_dts) == 400:
            self.benchmark_dts .sort()
            self.time_to_update.sort()

            print('State updates dt summary:')
            print('    Min:', self.benchmark_dts[0])
            print('    25%:', self.benchmark_dts[100])
            print('    50%:', self.benchmark_dts[200])
            print('    75%:', self.benchmark_dts[300])
            print('    Max:', self.benchmark_dts[-1])

            print('Time to run update summary:')
            print('    Min:', self.time_to_update[0])
            print('    25%:', self.time_to_update[100])
            print('    50%:', self.time_to_update[200])
            print('    75%:', self.time_to_update[300])
            print('    Max:', self.time_to_update[-1])

            self.benchmark_dts = []
            self.time_to_update = []
        # ---------------------------------------



    def on_state_update_step(self):
        
        retval = self._current_activity.event_update_state()

        if isinstance(self._current_activity, Menu) and retval:
            # retval is True if we need to change from Menu to Game.
            self._current_activity = Game(self.painter)

            from pyglet.window import key
            self.on_key_press(key.P, None)

        
    def on_draw(self):
        self.clear()
        self._current_activity.event_draw_screen()