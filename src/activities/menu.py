from pyglet.window import key

from src.activities.activity import Activity



# Decide what to do with this class. It could be merged with the recording class, this one could inherit from that, ...



class Menu(Activity):
    """Class Menu. Implements screen update and reaction to key presses
    when the program is showing the main menu."""
    

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.must_switch_to_game = False

    def __del__(self):
        self._painter.recording_free()

    def event_draw_screen(self):
        """Override of method from Activity class, drawing the main menu
        on the screen."""
        self._painter.draw_menu()
        
    def event_update_state(self):
        """Override of method from Activity class, updating the state of the
        activity."""
        return self.must_switch_to_game

    def event_key_pressed(self, symbol, modifiers):
        """Override of method from Activity class, reacting to key presses.
        Returns True if the game should start and False otherwise."""
        self.must_switch_to_game = symbol in (key.RETURN, key.SPACE)