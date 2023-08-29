# -*- coding: utf-8 -*-

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

        self._level = 0
        self._score = Score()
        
        self._lives = STARTING_LIVES_PACMAN
        self._extra_life_awarded = False

        self._new_level()

        

        


    def _new_level(self):
        self._level += 1

        self._maze = Maze()
        self._pacman = PacMan()
        self._ghosts = GhostsCoordinator()
        
        self._fright_counter = 0

        self._painter.new_level()


    def event_draw_screen(self):
        """Override of method from Activity class, drawing the controls menu
        on the screen."""
        self._painter.draw_game(self._pacman, self._ghosts, self._score, self._lives, self._level)
        

    def event_update_state(self):
        """Override of method from Activity class, updating the state of the activity."""

        fright = False
        if self._fright_counter > 0:
            self._fright_counter -= 1
            fright = True

        self._pacman .update(self._level, fright, self._maze)
        self._ghosts .update(self._level, fright, self._maze, self._pacman)

        self._calculate_new_game_state()

        self._painter.update(self._pacman)

        
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
        life_lost, count_eaten = self._ghosts.check_collision(self._maze, self._pacman) 
        for _ in range(count_eaten):
            self._score.add_to_score(ScoreActions.EAT_GHOST)
        if life_lost:
            self._life_lost()

        # Update lives if score high enough.
        if not self._extra_life_awarded and self._score.score >= EXTRA_LIFE_POINTS_REQUIREMENT:
            self._lives += 1
            self._extra_life_awarded = True

        # End level if completed.
        if self._maze.completed():
            self._end_level()


    def _fruit_eaten(self):
        # TODO: Fill this function
        print('Was on fruit')


    def _pellet_eaten(self, tile_coords, pellet_type):
        self._painter.set_empty_tile(tile_coords)
        self._pacman.add_penalty(pellet_type)
        self._ghosts.notify_pellet_eaten()
        self._score.add_to_score(ScoreActions.EAT_PELLET if pellet_type == MazeTiles.PELLET else ScoreActions.EAT_POWER_PELLET)

        if pellet_type == MazeTiles.POWER_PELLET:
            fright_duration, fright_flashes = FRIGHT_TIME_AND_FLASHES(self._level)

            self._fright_counter = fright_duration
            self._score.notify_fright_on()
            self._ghosts.notify_fright_on(fright_duration)
            self._painter.notify_fright_on(fright_duration, fright_flashes)


    def _life_lost(self):
        
        print('Life lost')

        # TODO: when life is lost, should not delete ghost_coordinator instance as it contains the global dot counter.


    def _end_level(self):
        self._new_level()
