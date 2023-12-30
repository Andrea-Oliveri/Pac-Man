from pyglet.window import key

from src.activities.recording import Recording

from src.constants import RecordingsType




class Menu(Recording):
    """Class Menu. Implements screen update and reaction to key presses
    when the program is showing the main menu."""
    

    def __init__(self, painter):
        super().__init__(painter, RecordingsType.INTRO)
        self.must_switch_to_game = False
  
    def event_update_state(self):
        """Override of method from Activity class, updating the state of the
        activity."""
        super().event_update_state()

        return self.must_switch_to_game

    def event_key_pressed(self, symbol, modifiers):
        """Override of method from Activity class, reacting to key presses.
        Returns True if the game should start and False otherwise."""
        self.must_switch_to_game = symbol in (key.RETURN, key.SPACE)