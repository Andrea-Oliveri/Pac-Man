# -*- coding: utf-8 -*-

from src.activities.activity import Activity

from src.constants import RECORDINGS_DETAILS


class Recording(Activity):
         
    
    def __init__(self, graphics, sounds, which):
        """Constructor for the class Recording."""
        super().__init__(graphics, sounds)
        
        details = RECORDINGS_DETAILS[which]
        path    = details['path']
        height, width = details['frame_shape']

        self._n_frames = self._graphics.recording_load(path, width, height)
        self._frame_idx = self._n_frames - 1

        self._ended = False


    def notify_destruction(self):
        self._graphics.recording_free()

        
    def event_draw_screen(self, **kwargs):
        """Redraws the activity in the window."""
        self._graphics.recording_draw(self._frame_idx, **kwargs)


    def event_update_state(self):
        """Updates the state of the activity."""
        self._frame_idx -= 1

        if self._frame_idx <= 0:
            self._frame_idx = self._n_frames - 1
            self._ended = True

        return self._ended


    def event_key_pressed(self, symbol, modifiers):
        """Reacts to key being pressed."""
        return