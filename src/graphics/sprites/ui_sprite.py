# -*- coding: utf-8 -*-

from src.graphics.sprites.sprite import AbstractSprite
from src.constants import (LIVES_SPRITE_TEX_REGION,
                           FRUIT_SPRITE_TEX_REGION,
                           TEXT_SPRITE_TEX_REGION,
                           Z_COORD_UI_AND_TEXT,
                           Z_COORD_FRUIT_IN_MAZE,
                           FRUIT_OF_LEVEL,
                           FRUIT_SPAWN_POSITION,
                           UI_MAX_FRUIT_ICON_NUMBER,
                           UI_MAX_SCORE_NUM_DIGITS,
                           UI_DEFAULT_TEXT_COLOR,
                           UI_PLAYER_ONE_TEXT_COLOR,
                           UI_READY_TEXT_COLOR,
                           UI_GAME_OVER_TEXT_COLOR,
                           LAYOUT_1UP_TEXT_COORDS,
                           LAYOUT_HIGH_SCORE_TEXT_COORDS,
                           LAYOUT_SCORE_NUMBER_COORDS,
                           LAYOUT_HIGH_SCORE_NUMBER_COORDS,
                           LAYOUT_PLAYER_ONE_TEXT_COORDS,
                           LAYOUT_READY_TEXT_COORDS,
                           LAYOUT_GAME_OVER_TEXT_COORDS,
                           LAYOUT_RIGHT_FRUIT_ICON_COORDS,
                           LAYOUT_LEFT_LIVES_ICON_COORDS)
from src.graphics.utils import convert_maze_coord_to_layout_coord



class UiSprite(AbstractSprite):

    def reset(self):
        return


    def update(self):
        return


    def send_vertex_data(self, show_ready_text, show_player_one_text, show_game_over_text, show_fruit_in_maze, score, high_score, lives, level):
        if show_ready_text:
            self._print(*LAYOUT_READY_TEXT_COORDS     , UI_READY_TEXT_COLOR     , 'READY!')

        if show_player_one_text:
            self._print(*LAYOUT_PLAYER_ONE_TEXT_COORDS, UI_PLAYER_ONE_TEXT_COLOR, 'PLAYER ONE')

        if show_game_over_text:
            self._print(*LAYOUT_GAME_OVER_TEXT_COORDS , UI_GAME_OVER_TEXT_COLOR , 'GAME  OVER')

        if show_fruit_in_maze:
            self._draw_fruit_in_maze(level)

        self._draw_score_texts(score, high_score)
        self._draw_lives      (lives)
        self. draw_fruits     (level)


    def _draw_score_texts(self, score, high_score):
        # Print text on top of screen.
        self._print(*LAYOUT_HIGH_SCORE_TEXT_COORDS, UI_DEFAULT_TEXT_COLOR, 'HIGH SCORE')
        self._print(*LAYOUT_1UP_TEXT_COORDS       , UI_DEFAULT_TEXT_COLOR, '1UP')
        
        # Print score and high score numbers.
        high_score = (''   if high_score == 0 else str(high_score)).rjust(UI_MAX_SCORE_NUM_DIGITS, ' ')[-UI_MAX_SCORE_NUM_DIGITS:]
        score      = ('00' if score      == 0 else str(score))     .rjust(UI_MAX_SCORE_NUM_DIGITS, ' ')[-UI_MAX_SCORE_NUM_DIGITS:]
        
        self._print(*LAYOUT_HIGH_SCORE_NUMBER_COORDS, UI_DEFAULT_TEXT_COLOR, high_score)
        self._print(*LAYOUT_SCORE_NUMBER_COORDS     , UI_DEFAULT_TEXT_COLOR, score)


    def _draw_lives(self, lives):
        # Draw the lives.
        x, y = LAYOUT_LEFT_LIVES_ICON_COORDS
        for _ in range(lives):
            tex_coords = LIVES_SPRITE_TEX_REGION
            self._painter.add_quad(x, y, *tex_coords, Z_COORD_UI_AND_TEXT)
            x += 2


    def draw_fruits(self, level):
        fruits = [FRUIT_OF_LEVEL(i) for i in range(level-UI_MAX_FRUIT_ICON_NUMBER+1, level+1) if i >= 1]
        x, y = LAYOUT_RIGHT_FRUIT_ICON_COORDS
        for fruit in fruits:
            tex_coords = FRUIT_SPRITE_TEX_REGION(fruit)
            self._painter.add_quad(x, y, *tex_coords, Z_COORD_UI_AND_TEXT)
            x -= 2


    def _print(self, x, y, color, text):
        x_start = x

        for char in text:
            if char == '\n':
                y += 1
                x = x_start
                continue

            tex_coords = TEXT_SPRITE_TEX_REGION(char, color)
            self._painter.add_quad(x, y, *tex_coords, Z_COORD_UI_AND_TEXT)
            x += 1


    def _draw_fruit_in_maze(self, level):
        fruit = FRUIT_OF_LEVEL(level)

        tex_coords = FRUIT_SPRITE_TEX_REGION(fruit)
        coords = convert_maze_coord_to_layout_coord(FRUIT_SPAWN_POSITION)

        self._painter.add_quad(coords.x, coords.y, *tex_coords, Z_COORD_FRUIT_IN_MAZE)