# -*- coding: utf-8 -*-

import time
from pyglet.window import key

from src.activities.activity import Activity
from src.directions import Vector2

from src.game_objects.pacman import PacMan
from src.game_objects.maze import Maze
from src.game_objects.score import Score
from src.game_objects.ghosts.ghost_coordinator import GhostsCoordinator

from src.constants import (MazeTiles,
                           ScoreActions,
                           STARTING_LIVES_PACMAN,
                           EXTRA_LIFE_POINTS_REQUIREMENT,
                           FRUIT_SPAWN_POSITION,
                           FRIGHT_TIME_AND_FLASHES)


class Game(Activity):
    """Class Game. Implements screen update, reaction to key presses
    and releases and game engine when the program is showing the game."""
    
    def __init__(self, painter):
        """Override of method from Activity class, instancing all game objects."""
        super().__init__(painter)

        self._maze = Maze()
        self._pacman = PacMan()
        self._ghosts = GhostsCoordinator()
        
        self._score = Score()

        self._level = 1

        self._fright_off_time = None

        self._lives = STARTING_LIVES_PACMAN
        self._extra_life_awarded = False
        


    def event_draw_screen(self):
        """Override of method from Activity class, drawing the controls menu
        on the screen."""
        self._painter.draw_game(self._pacman, self._ghosts, self._score, self._lives, self._level)
        

    def event_update_state(self, dt):
        """Override of method from Activity class, updating the state of the
        activity."""

        # Update fright timer and tick game in a conservative way: if switching from fright to not, tick game at edge and then tick for remaining dt.
        # Can't rely on dt exclusively because start time would depend on how long game update has taken. 
        if self._fright_off_time is not None:
            time_now = time.time()

            if time_now > self._fright_off_time:
                remaining_fright_time = time_now - self._fright_off_time

                self._game_tick(remaining_fright_time)
                dt -= remaining_fright_time
                self._fright_off_time = None
                print('Fright off')
            
        self._game_tick(dt)



    def _game_tick(self, dt):
        fright = self._fright_off_time is not None

        self._pacman.update(dt, self._level, fright, self._maze)
        self._ghosts.update(dt, self._level, fright, self._maze, self._pacman)

        self._calculate_new_game_state()

        
    def event_key_pressed(self, symbol, modifiers):
        """Override of method from Activity class, reacting to key presses.
        Returns True if the game should start and False otherwise."""
        if symbol == key.UP:
            self._pacman.direction = Vector2.UP
        elif symbol == key.DOWN:
            self._pacman.direction = Vector2.DOWN
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
            const.REFERENCE_SPEED = self._original_speed if const.REFERENCE_SPEED < self._original_speed else self._original_speed * 0.1

        # ------------------------------


    def _calculate_new_game_state(self):
        # Check if passed on to fruit spawning point.
        pacman_old_position = self._pacman.old_position
        pacman_new_position = self._pacman.position

        was_on_fruit = (pacman_old_position.y == pacman_new_position.y == FRUIT_SPAWN_POSITION.y) and \
                       ((pacman_old_position.x <= FRUIT_SPAWN_POSITION.x <= pacman_new_position.x) or \
                        (pacman_new_position.x <= FRUIT_SPAWN_POSITION.x <= pacman_old_position.x))

        if was_on_fruit:
            self._fruit_eaten()

        # Check if eaten a pellet.
        tile_coords, pellet_type = self._maze.eat_check_pellet(pacman_new_position)
        if tile_coords is not None:
            self._pellet_eaten(tile_coords, pellet_type)

        # Check if collided with any ghosts.
        if self._ghosts.check_collision(self._maze, self._pacman.position):
            self._ghost_collision()

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
                self._fright_off_time = time.time() + fright_duration
                self._score.notify_fright_on()


    def _ghost_collision(self):
        print('Ghost collision')


    def _end_level():
        print('Level completed')
