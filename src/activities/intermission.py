# -*- coding: utf-8 -*-

from src.activities.recording import Recording

from src.constants import LEVEL_WITH_INTERMISSIONS


class Intermission(Recording):
    
    def __init__(self, painter, game_level):
        """Constructor for the class Recording."""
        self._game_level = game_level

        which = LEVEL_WITH_INTERMISSIONS[game_level]
        super().__init__(painter, which)
        
    def event_draw_screen(self):
        """Redraws the activity in the window."""
        self._painter.recording_draw(self._frame_idx, self._game_level)