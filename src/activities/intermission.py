# -*- coding: utf-8 -*-

from src.activities.recording import Recording

from src.constants import LEVEL_WITH_INTERMISSIONS


class Intermission(Recording):
    
    def __init__(self, graphics, game_level):
        """Constructor for the class Recording."""
        self._game_level = game_level

        which = LEVEL_WITH_INTERMISSIONS[game_level]
        super().__init__(graphics, which)
        
    def event_draw_screen(self):
        """Redraws the activity in the window."""
        super().event_draw_screen(level_to_draw_fruits = self._game_level)