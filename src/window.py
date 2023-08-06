# -*- coding: utf-8 -*-

import pyglet

from src.activities.menu import Menu
from src.activities.game import Game
from src.graphics.painter import Painter
from src.constants import (WINDOW_INIT_KWARGS,
                           WINDOW_MINIMUM_SIZE,
                           GAME_UPDATES_INTERVAL,
                           WINDOW_ICON_PATH)


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
        pyglet.clock.schedule_interval(self.on_state_update, GAME_UPDATES_INTERVAL)

        
    def on_resize(self, width, height):
        desired_width, desired_height = WINDOW_MINIMUM_SIZE
        desired_aspect_ratio = desired_width / desired_height

        # Draw on the whole window.
        self.viewport = (0, 0, width, height)

        # Scale and translate the render space.
        if self.aspect_ratio > desired_aspect_ratio:
            y_max = desired_height / 2
            x_max = y_max * self.aspect_ratio
        else:
            x_max = desired_width / 2
            y_max = x_max / self.aspect_ratio

        self.projection = pyglet.math.Mat4.orthogonal_projection(-x_max, +x_max, -y_max, y_max, -255, 255)

        return pyglet.event.EVENT_HANDLED   # Don't call the default handler


    def on_key_press(self, symbol, modifiers):
        self._current_activity.event_key_pressed(symbol, modifiers)

    def on_key_release(self, symbol, modifiers):
        self._current_activity.event_key_released(symbol, modifiers)

    def on_state_update(self, dt):
        
        # -------- TEMP BENCHMARK CODE ----------
        self.benchmark_dts = self.benchmark_dts if hasattr(self, 'benchmark_dts') else []
        self.benchmark_dts.append(dt)
        if len(self.benchmark_dts) == 400:
            self.benchmark_dts.sort()
            print('State updates dt summary:')
            print('    Min:', self.benchmark_dts[0])
            print('    25%:', self.benchmark_dts[100])
            print('    50%:', self.benchmark_dts[200])
            print('    75%:', self.benchmark_dts[300])
            print('    Max:', self.benchmark_dts[-1])
            self.benchmark_dts = []
        # ---------------------------------------
        
        # It is possible for the dt to be very large due to events which case a lag spike.
        # An example is on_resize when going to fullscreen. 
        # To avoid issues in the downstream logic, we cap the maximum dt and execute multiple updates if needed.
        while dt > 0:
            dt_step = min(dt, GAME_UPDATES_INTERVAL)
            dt -= GAME_UPDATES_INTERVAL

            self.on_state_update_step(dt_step)



    def on_state_update_step(self, dt):
        

        retval = self._current_activity.event_update_state(dt)

        if isinstance(self._current_activity, Menu) and retval:
            # retval is True if we need to change from Menu to Game.
            self._current_activity = Game(self.painter)

        
    def on_draw(self):
        self.clear()
        self._current_activity.event_draw_screen()
        
        #self.painter.draw()




#class Gui():
#    """Class Gui. Implements the pygame event loop and delegates handling events to
#    current activities. Also deals with changing the current activity and interfaces
#    the sound engine for the background music."""
    
#    def __init__(self):
#        """Constructor for the class Gui."""
#        # First initialize sound engine, such that constructor sets desired
#        # values for the pygame.mixer.init function.
#        self._sound = SoundEngine()
        
#        # Initialize all pygame modules. pygame.mixer will not be re-initialized
#        # and hence the desired values for pygame.mixer.init will be kept.
#        pygame.init()
        
#        # Open a pygame window.
#        self._window = Window()

#        # Store current activity.
#        self._current_activity = Menu(self._window, self._sound)
        
        
#    def __del__(self):
#        """Destructor for the class Gui."""
#        del self._current_activity
#        del self._sound
#        del self._window
#        pygame.quit()
        
    
#    def run(self):
#        """Method implementing the pygame event loop, dealing with changing the
#        current activity, delegating events to current activity, exiting program
#        if the window was closed and interfacing sound engine for the background
#        music."""
#        pygame.event.set_allowed([QUIT, KEYDOWN, KEYUP])
        
#        # Variable used to limit the fps at which screen is being updated.
#        fps_clock = pygame.time.Clock()
        
#        while not self._window.closed:
#            fps_clock.tick(REFRESH_RATE)
#            self._current_activity.event_update_screen(fps_clock.get_fps())            
            
#            for event in pygame.event.get():    
#                if event.type == QUIT:
#                    self._window.close()
                
#                if event.type == KEYDOWN:
#                    if event.key == K_r:
#                        self._sound.change_track()
                        
#                    elif event.key == K_m:
#                        self._sound.toggle_mute()
                        
#                    else:
                    
#                        output = self._current_activity.event_key_pressed(event.key)
                        
#                        if isinstance(self._current_activity, Menu):
#                            change_activity, text_pressed = output
                            
#                            if change_activity:
#                                if text_pressed == 'Play':
#                                    # Enable Delayed Auto Shift.
#                                    pygame.key.set_repeat(DAS_DELAY, DAS_RATE)
                                    
#                                    self._current_activity = Game(self._window, self._sound)
#                                elif text_pressed == 'Controls':
#                                    self._current_activity = MenuControls(self._window, self._sound)
#                                elif text_pressed == 'Exit':
#                                    self._window.close()
#                                else:
#                                    raise RuntimeError("Unknown selected menu option")
                                    
#                        elif isinstance(self._current_activity, MenuControls) or isinstance(self._current_activity, Game):
#                            change_activity = output
                            
#                            if change_activity:
#                                self._current_activity = Menu(self._window, self._sound)
                                
#                                # Disable Delayed Auto Shift.
#                                pygame.key.set_repeat()

                
#                elif event.type == KEYUP:
#                    self._current_activity.event_key_released(event.key)