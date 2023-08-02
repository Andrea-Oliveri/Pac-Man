# -*- coding: utf-8 -*-

from pyglet.window import key
import pyglet.clock

from src.activities.activity import Activity
from src.directions import Vector2

from src.game_objects.pacman import PacMan
from src.game_objects.maze import Maze
from src.game_objects.score import Score

from src.constants import (MazeTiles,
                           ScoreActions,
                           STARTING_LIVES_PACMAN,
                           EXTRA_LIFE_POINTS_REQUIREMENT,
                           FRUIT_SPAWN_COORDINATES,
                           FRIGHT_TIME_AND_FLASHES)


class Game(Activity):
    """Class Game. Implements screen update, reaction to key presses
    and releases and game engine when the program is showing the game."""
    
    def __init__(self, painter):
        """Override of method from Activity class, instancing all game objects."""
        super().__init__(painter)

        self._maze = Maze()
        self._pacman = PacMan()
        
        self._score = Score()

        self._level = 1

        self._fright = False
        self._next_fright = False

        self._lives = STARTING_LIVES_PACMAN
        self._extra_life_awarded = False
        


    def event_draw_screen(self):
        """Override of method from Activity class, drawing the controls menu
        on the screen."""
        self._painter.draw_game(self._pacman, self._score, self._lives, self._level)
        

    def event_update_state(self, dt):
        """Override of method from Activity class, updating the state of the
        activity."""
        self._pacman.update(dt, self._level, self._fright, self._maze)

        self._calculate_new_game_state()

        # To avoid threading-related inconsistencies, only update fright at the end of the update step.
        self._fright = self._next_fright

        
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

        # ------------------------------
        # DEBUG: slow down pacman
        # ------------------------------
        if symbol == key.SPACE:
            import src.constants as const
            if not hasattr(self, '_original_speed'):
                self._original_speed = float(const.REFERENCE_SPEED)
            const.REFERENCE_SPEED = self._original_speed if const.REFERENCE_SPEED < self._original_speed else 1


        # ------------------------------


    def _calculate_new_game_state(self):
        # Check if passed on to fruit spawning point.
        pacman_old_position = self._pacman.old_position
        pacman_new_position = self._pacman.position

        was_on_fruit = (pacman_old_position.y == pacman_new_position.y == FRUIT_SPAWN_COORDINATES.y) and \
                       ((pacman_old_position.x <= FRUIT_SPAWN_COORDINATES.x <= pacman_new_position.x) or \
                        (pacman_new_position.x <= FRUIT_SPAWN_COORDINATES.x <= pacman_old_position.x))

        if was_on_fruit:
            self._fruit_eaten()

        # Check if eaten a pellet.
        tile_coords, pellet_type = self._maze.eat_check_pellet(pacman_new_position)
        if tile_coords is not None:
            self._pellet_eaten(tile_coords, pellet_type)

        # Check if collided with any ghosts.
        pass


        # Update lives if score high enough.
        if not self._extra_life_awarded and self._score.score >= EXTRA_LIFE_POINTS_REQUIREMENT:
            self._lives += 1

        # End level if completed.
        if self._maze.completed():
            self._end_level()


    def _fruit_eaten(self):
        # TODO: Fill this function
        print('Was on fruit')


    def _pellet_eaten(self, tile_coords, pellet_type):
        self._painter.set_empty_tile(tile_coords)
        self._pacman.add_penalty(pellet_type)
        self._score.add_to_score(ScoreActions.EAT_PELLET if pellet_type == MazeTiles.PELLET else ScoreActions.EAT_POWER_PELLET)

        if pellet_type == MazeTiles.POWER_PELLET:
            fright_duration, _ = FRIGHT_TIME_AND_FLASHES(self._level)
            if fright_duration > 0:
                self._fright = self._next_fright = True
                pyglet.clock.schedule_once(self._turn_fright_off, fright_duration)
                self._score.notify_fright_on()

    def _end_level():
        print('Level completed')

    def _turn_fright_off(self, dt):
        self._next_fright = False
        print('Fright off')