# -*- coding: utf-8 -*-

from random import randint

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
                           FRUIT_SPAWN_THRESHOLDS,
                           FRUIT_SPAWN_POSITION,
                           FRUIT_TIME_ACTIVE_RANGE,
                           FRIGHT_TIME_AND_FLASHES,
                           LevelStates,
                           LEVEL_STATES_DURATION,
                           DynamicUIElements)


class Game(Activity):
    """Class Game. Implements screen update, reaction to key presses
    and releases and game engine when the program is showing the game."""
    
    def __init__(self, painter):
        """Override of method from Activity class, instancing all game objects."""
        super().__init__(painter)

        self._score = Score()
        
        self._lives = STARTING_LIVES_PACMAN
        self._extra_life_awarded = False

        # Create private attributes to hold level state and duration of the state.
        self._level_state = None
        self._level_state_counter = 0

        # Create attributes that will be initialized in _new_level.
        self._level = 0
        self._maze   = None
        self._pacman = None
        self._ghosts = None
        self._fright_counter = None
        self._fruit_visible_counter = 0

        self._set_level_state(LevelStates.FIRST_WELCOME)


    def _reset_level(self, new):
        if new:
            self._level  += 1
            self._maze   = Maze()
            self._ghosts = GhostsCoordinator()
        
        self._pacman = PacMan()
        
        self._fright_counter = 0

        self._fruit_visible_counter = 0

        self._painter.reset_level(new)



    def event_draw_screen(self):
        """Override of method from Activity class, drawing the game state on the screen."""

        match self._level_state:
            case LevelStates.FIRST_WELCOME:
                ui_elements = DynamicUIElements.READY_TEXT | DynamicUIElements.PLAYER_ONE_TEXT
            case LevelStates.READY:
                ui_elements = DynamicUIElements.READY_TEXT | DynamicUIElements.PACMAN | DynamicUIElements.GHOSTS
            case LevelStates.DEATH:
                ui_elements = DynamicUIElements.PACMAN | DynamicUIElements.FRUIT
            case LevelStates.COMPLETED:
                ui_elements = DynamicUIElements.PACMAN
            case LevelStates.GAME_OVER:
                ui_elements = DynamicUIElements.GAME_OVER_TEXT
            case LevelStates.PAUSE_AFTER_EATING:
                ui_elements = DynamicUIElements.GHOSTS | DynamicUIElements.FRUIT
            case LevelStates.PLAYING | LevelStates.PAUSE_BEFORE_DEATH | LevelStates.PAUSE_BEFORE_COMPLETED:
                ui_elements = DynamicUIElements.PACMAN | DynamicUIElements.GHOSTS | DynamicUIElements.FRUIT
                
        if self._fruit_visible_counter <= 0:
            ui_elements &= (~DynamicUIElements.FRUIT)

        self._painter.draw_game(self._pacman, self._ghosts, self._score, self._lives, self._level, ui_elements)
        

    def event_key_pressed(self, symbol, modifiers):
        """Override of method from Activity class, reacting to key presses."""
        if symbol == key.UP:
            self._pacman.direction = Vector2.UP
        elif symbol == key.DOWN:
            self._pacman.direction = Vector2.DOWN
        elif symbol == key.LEFT:
            self._pacman.direction = Vector2.LEFT
        elif symbol == key.RIGHT:
            self._pacman.direction = Vector2.RIGHT



    def event_update_state(self):
        """Override of method from Activity class, updating the state of the activity."""
        
        # Update level state.
        match self._level_state:
            case LevelStates.PLAYING:
                self._update_game()

            case LevelStates.DEATH:
                self._painter.update(self._pacman)

            case LevelStates.PAUSE_AFTER_EATING:
                self._ghosts.update(self._level, True, self._maze, self._pacman, update_only_transparent = True)

        
        # Transition to new level state if needed.      
        change_state = self._level_state_counter <= 0
        self._level_state_counter -= 1
        
        match self._level_state:
            case LevelStates.PLAYING:
                self._calculate_new_game_state()

            case LevelStates.FIRST_WELCOME:
                if change_state:
                    self._set_level_state(LevelStates.READY)
                    self._reset_level(new = True)
                    self._lives -= 1

            case LevelStates.READY:
                if change_state:
                    self._set_level_state(LevelStates.PLAYING)
                    self._pacman.state_set_moving()

            case LevelStates.DEATH:
                if change_state:
                    self._lives -= 1
                    if self._lives >= 0:
                        self._set_level_state(LevelStates.READY)
                        self._reset_level(new = False)
                    else:
                        self._set_level_state(LevelStates.GAME_OVER)

            case LevelStates.COMPLETED:
                if change_state:
                    self._set_level_state(LevelStates.READY)
                    self._reset_level(new = True)

            case LevelStates.GAME_OVER:
                if change_state:
                    return True # Tell Window class we need to change activity.

            case LevelStates.PAUSE_AFTER_EATING:
                if change_state:
                    self._set_level_state(LevelStates.PLAYING)
                    self._ghosts.notify_clear_was_just_eaten()

                    # Test if collision with another ghost happened in the same spot. If so, function will autoatically change _level_state again.
                    self._calculate_new_game_state()

            case LevelStates.PAUSE_BEFORE_DEATH:
                if change_state:
                    self._set_level_state(LevelStates.DEATH)
                    self._pacman.state_set_death()
                    self._ghosts.notify_life_lost()
            
            case LevelStates.PAUSE_BEFORE_COMPLETED:
                if change_state:
                    self._set_level_state(LevelStates.COMPLETED)

        return False
        


    def _update_game(self):
        fright = False
        if self._fright_counter > 0:
            self._fright_counter -= 1
            fright = True

        if self._fruit_visible_counter > 0:
            self._fruit_visible_counter -= 1

        self._pacman.update(self._level, fright, self._maze)
        self._ghosts.update(self._level, fright, self._maze, self._pacman, update_only_transparent = False)

        self._painter.update(self._pacman)


    def _calculate_new_game_state(self):
        pacman_new_position = self._pacman.position

        # Check if eaten a fruit.
        if self._fruit_visible_counter:
            pacman_old_position = self._pacman.old_position

            was_on_fruit = (pacman_old_position.y == pacman_new_position.y == FRUIT_SPAWN_POSITION.y) and \
                           ((pacman_old_position.x <= FRUIT_SPAWN_POSITION.x <= pacman_new_position.x) or \
                            (pacman_new_position.x <= FRUIT_SPAWN_POSITION.x <= pacman_old_position.x))
            if was_on_fruit:
                self._fruit_visible_counter = 0
                self._score.add_to_score(ScoreActions.EAT_FRUIT, self._level)

        # Check if eaten a pellet.
        tile_coords, pellet_type = self._maze.eat_check_pellet(pacman_new_position)
        if tile_coords is not None:
            self._pellet_eaten(tile_coords, pellet_type)

        # Update lives if score high enough.
        if not self._extra_life_awarded and self._score.score >= EXTRA_LIFE_POINTS_REQUIREMENT:
            self._lives += 1
            self._extra_life_awarded = True

        # End level if completed.
        if self._maze.completed:
            self._set_level_state(LevelStates.PAUSE_BEFORE_COMPLETED)
            self._pacman.state_become_round()

        # Check if collided with any ghosts.
        life_lost, any_eaten = self._ghosts.check_collision(self._maze, self._pacman) 
        if any_eaten:
            self._score.add_to_score(ScoreActions.EAT_GHOST)
            self._set_level_state(LevelStates.PAUSE_AFTER_EATING)
        if life_lost:
            self._set_level_state(LevelStates.PAUSE_BEFORE_DEATH)


    def _pellet_eaten(self, tile_coords, pellet_type):
        self._painter.set_empty_tile(*tile_coords)
        self._pacman.add_penalty(pellet_type)
        self._ghosts.notify_pellet_eaten()
        self._score.add_to_score(ScoreActions.EAT_PELLET if pellet_type == MazeTiles.PELLET else ScoreActions.EAT_POWER_PELLET)

        if pellet_type == MazeTiles.POWER_PELLET:
            fright_duration, fright_flashes = FRIGHT_TIME_AND_FLASHES(self._level)

            self._fright_counter = fright_duration
            self._score.notify_fright_on()
            self._ghosts.notify_fright_on(fright_duration)
            self._painter.notify_fright_on(fright_duration, fright_flashes)

        if self._maze.n_pellets_remaining in FRUIT_SPAWN_THRESHOLDS:
            self._fruit_visible_counter = randint(*FRUIT_TIME_ACTIVE_RANGE)


    def _set_level_state(self, new_state):
        if new_state not in LevelStates:
            raise ValueError('Invalid state provided to Game._set_level_state')
        
        self._level_state = new_state
        self._level_state_counter = LEVEL_STATES_DURATION[new_state]