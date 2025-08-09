# -*- coding: utf-8 -*-

from pyglet.window import key

from src.activities.activity import Activity

from src.constants import (UpdatableUIElements,
                           GAME_COMPLETED_REWARD_INITIAL,
                           GAME_COMPLETED_REWARD_EXTRA_LIVES,
                           GAME_COMPLETED_REWARD_INCREMENT,
                           GAME_COMPLETED_REWARD_INCREMENT_PERIOD_FRAMES)


class GameCompleted(Activity):
    """Class GameCompleted. Displays a congratulations message and increases the
    score to account for split-screen levels which are not programmed."""
    
    def __init__(self, graphics, sounds, score, lives, level):
        """Override of method from Activity class, storing information passed by Game class."""
        super().__init__(graphics, sounds)

        self._score = score
        self._level = level

        self._score_to_add = GAME_COMPLETED_REWARD_INITIAL + lives * GAME_COMPLETED_REWARD_EXTRA_LIVES
        self._score_increment_counter = 0

        self._sounds.notify_game_completed()
        self._must_switch_to_menu = False


    def event_draw_screen(self):
        """Override of method from Activity class, drawing the ui and congratulations message."""
        self._graphics.draw_game_completed(self._score, lives = 0, level = self._level)
    

    def event_key_pressed(self, symbol, modifiers):
        """Override of method from Activity class, reacting to key presses."""
        if self._score_to_add > 0:
            return
        
        self._must_switch_to_menu = symbol in (key.RETURN, key.SPACE)
        

    def event_update_state(self):
        """Override of method from Activity class, updating the state of the activity."""
        
        self._graphics.update(pacman = None, ui_elements = UpdatableUIElements.UI)
        self._score_increment_counter += 1

        if self._score_to_add > 0 and not (self._score_increment_counter % GAME_COMPLETED_REWARD_INCREMENT_PERIOD_FRAMES):
            delta = min(self._score_to_add, GAME_COMPLETED_REWARD_INCREMENT)
            self._score_to_add -= delta
            self._score += delta

        return self._must_switch_to_menu