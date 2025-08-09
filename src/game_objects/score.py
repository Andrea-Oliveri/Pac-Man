# -*- coding: utf-8 -*-

import os
import weakref
from dataclasses import dataclass

from src.constants import (ScoreActions,
                           SCORE_POINTS_EAT_PELLET,
                           SCORE_POINTS_EAT_POWER_PELLET,
                           SCORE_POINTS_EAT_GHOST_BASE,
                           SCORE_POINTS_EAT_FRUIT,
                           HIGH_SCORE_FILE,
                           HIGH_SCORE_FILE_NUM_BYTES)


# Dataclass needed just to hold the high-score value so we can pass it to weakref.finalizer without resuscitating the Score instance.
@dataclass(slots = True)
class _ScoreValues:
    score: int
    high_score: int

    _BYTES_INT_CONVERSION_KWARGS = {'byteorder': 'big', 'signed': False}

    def __init__(self):
        self.score = 0
        self.high_score = self._high_score_load()

    def _high_score_load(self):
        high_score = 0
        if os.path.isfile(HIGH_SCORE_FILE):
            with open(HIGH_SCORE_FILE, 'rb') as file:
                high_score = int.from_bytes(file.read(HIGH_SCORE_FILE_NUM_BYTES), **self._BYTES_INT_CONVERSION_KWARGS)
        return high_score

    def _high_score_save(self):
        with open(HIGH_SCORE_FILE, 'wb') as file:
            file.write(self.high_score.to_bytes(length = HIGH_SCORE_FILE_NUM_BYTES, **self._BYTES_INT_CONVERSION_KWARGS))


class Score:
    """Class Score. Class dealing with updating of the score."""

    def __init__(self):
        """Constructor for the class Score."""
        self._scores = _ScoreValues()
        
        weakref.finalize(self, self._scores._high_score_save)

        self._ghost_eaten_same_fright = None
        
    
    # Defining properties for some private attributes.
    score      = property(lambda self: self._scores.score)
    high_score = property(lambda self: self._scores.high_score)
    

    def __iadd__(self, value):
        self._scores.score += value

        if self._scores.score > self._scores.high_score:
            self._scores.high_score = self._scores.score
            # Score will be written to disk by finalizer.

        return self
    
    
    def add_to_score(self, action, level = None):
        """Adds points to the score based on the action type and data in parameters dictionary."""
        
        increment = 0
        match action:
            case ScoreActions.EAT_PELLET:
                increment = SCORE_POINTS_EAT_PELLET
            case ScoreActions.EAT_POWER_PELLET:
                increment = SCORE_POINTS_EAT_POWER_PELLET
            case ScoreActions.EAT_GHOST:
                increment = SCORE_POINTS_EAT_GHOST_BASE * (2 ** self._ghost_eaten_same_fright)
                self._ghost_eaten_same_fright += 1
            case ScoreActions.EAT_FRUIT:
                increment = SCORE_POINTS_EAT_FRUIT(level)
            case _:
                raise ValueError(f'Unvalid action provided for Score.add_to_score: {action}')

        self += increment
        return increment


    def notify_fright_on(self):
        self._ghost_eaten_same_fright = 0