# -*- coding: utf-8 -*-

from src.activities.recording import Recording

from src.constants import LEVEL_WITH_INTERMISSIONS


class Intermission(Recording):
    
    def __init__(self, graphics, sounds, game_level):
        """Constructor for the class Recording."""
        self._game_level = game_level

        which = LEVEL_WITH_INTERMISSIONS[game_level]
        super().__init__(graphics, sounds, which)

        self._sounds.notify_intermission()
        

    def event_draw_screen(self):
        """Redraws the activity in the window."""
        super().event_draw_screen(level_to_draw_fruits = self._game_level)


    def event_update_state(self):
        super().event_update_state()

        if self._ended:
            self._sounds.stop()

        return self._ended