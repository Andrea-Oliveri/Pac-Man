# -*- coding: utf-8 -*-


class Score:
    """Class Score. Class dealing with updating of the score."""

    def __init__(self):
        """Constructor for the class Score."""
        self._score = 0
        
        
    def _get_score(self):
        """Special function that allows to get the attribute _score from the exterior."""
        return self._score
    
    
    """Definition of a properties for parameter _score. This parameter can
    only be get from the exterior, not set nor deleted."""
    score = property(_get_score)
    
        
    def add_to_score(self, action_type, parameters):
        """Adds points to the score based on the action type and data in parameters dictionary."""
                    
        raise NotImplementedError