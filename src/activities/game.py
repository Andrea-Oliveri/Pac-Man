# -*- coding: utf-8 -*-

from pyglet.window import key

from src.activities.activity import Activity
from src.utils import Vector2

from src.game_objects.pacman import PacMan
from src.game_objects.maze import Maze



class Game(Activity):
    """Class Game. Implements screen update, reaction to key presses
    and releases and game engine when the program is showing the game."""
    
    def __init__(self, painter):
        """Override of method from Activity class, instancing all game objects."""
        super().__init__(painter)

        self._maze = Maze()
        self._pacman = PacMan()

        self._level = 1
        self._fright = False


    def event_draw_screen(self):
        """Override of method from Activity class, drawing the controls menu
        on the screen."""
        self._painter.draw_game(self._pacman)
        
    def event_update_state(self, dt):
        """Override of method from Activity class, updating the state of the
        activity."""
        self._pacman.update(dt, self._level, self._fright, self._maze)
        tile_emptied_idx, pellet_type = self._maze.update_tile(self._pacman.position)

        if tile_emptied_idx is not None:
            self._painter.set_empty_tile(tile_emptied_idx)
            self._pacman.add_penalty(pellet_type)

        if self._maze.completed():
            print('Level completed')

    def event_key_pressed(self, symbol, modifiers):
        """Override of method from Activity class, reacting to key presses.
        Returns True if the game should start and False otherwise."""
        if symbol == key.UP:
            self._pacman.direction = Vector2.DOWN
        elif symbol == key.DOWN:
            self._pacman.direction = Vector2.UP
        elif symbol == key.LEFT:
            self._pacman.direction = Vector2.LEFT
        elif symbol == key.RIGHT:
            self._pacman.direction = Vector2.RIGHT