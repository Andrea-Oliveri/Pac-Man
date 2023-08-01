# -*- coding: utf-8 -*-

import os

from src.constants import (ScoreActions,
                           SCORE_POINTS_EAT_PELLET,
                           SCORE_POINTS_EAT_POWER_PELLET,
                           SCORE_POINTS_EAT_GHOST_BASE,
                           SCORE_POINTS_EAT_FRUIT,
                           HIGH_SCORE_FILE,
                           HIGH_SCORE_FILE_NUM_BYTES)

class Score:
    """Class Score. Class dealing with updating of the score."""

    def __init__(self):
        """Constructor for the class Score."""
        self._score = 0
        self._high_score = self._load_or_write_high_score(load = True)

        self._ghost_eaten_same_fright = None
        self._level = None
        
    
    # Defining properties for some private attributes.
    score      = property(lambda self: self._score)
    high_score = property(lambda self: self._high_score)
    

    def __iadd__(self, value):
        self._score += value

        if self._score > self._high_score:
            self._high_score = self._score
            self._load_or_write_high_score(load = False)


    def _load_or_write_high_score(self, load):
        
        if load:
            if not os.path.isfile(HIGH_SCORE_FILE):
                return self._score

            with open(HIGH_SCORE_FILE, 'rb') as file:
                return int.from_bytes(file.read(HIGH_SCORE_FILE_NUM_BYTES), byteorder = 'big', signed = False)
            
        with open(HIGH_SCORE_FILE, 'wb') as file:
            file.write(self._high_score.to_bytes(length = HIGH_SCORE_FILE_NUM_BYTES, byteorder = 'big', signed = False))

    
    def add_to_score(self, action): 
        """Adds points to the score based on the action type and data in parameters dictionary."""
        
        match action:
            case ScoreActions.EAT_PELLET:
                self += SCORE_POINTS_EAT_PELLET
            case ScoreActions.EAT_POWER_PELLET:
                self += SCORE_POINTS_EAT_POWER_PELLET
            case ScoreActions.EAT_GHOST:
                self += SCORE_POINTS_EAT_GHOST_BASE * (2 ** self._ghost_eaten_same_fright)
                self._ghost_eaten_same_fright += 1
            case ScoreActions.EAT_FRUIT:
                self += SCORE_POINTS_EAT_FRUIT(self._level)
            case _:
                raise ValueError(f'Unvalid action provided for Score.add_to_score: {action}')


    def notify_fright_on(self):
        self._ghost_eaten_same_fright = 0

    def notify_level_change(self, level):
        self._level = level