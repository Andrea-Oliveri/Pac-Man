from abc import ABC, abstractmethod


class Activity(ABC):
    """Class Activity. Class representing a program state that can be shown on the window."""
         
    
    def __init__(self, painter):
        """Constructor for the class Activity."""
        self._painter = painter
    
    @abstractmethod
    def event_draw_screen(self):
        """Redraws the activity in the window."""
        return

    @abstractmethod
    def event_update_state(self):
        """Updates the state of the activity."""
        return
    
    @abstractmethod
    def event_key_pressed(self, symbol, modifiers):
        """Reacts to key being pressed."""
        return