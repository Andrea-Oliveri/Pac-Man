# -*- coding: utf-8 -*-


class Score:
    """Class Score. Class dealing with updating of the score."""

    def __init__(self):
        """Constructor for the class Score."""
        self._score = 0
        self._high_score = 0
        
    
    # Defining properties for some private attributes.
    score      = property(lambda self: self._score)
    high_score = property(lambda self: self._high_score)
    
        
    def add_to_score(self, action_type, parameters): 
        """Adds points to the score based on the action type and data in parameters dictionary."""
                    
        raise NotImplementedError