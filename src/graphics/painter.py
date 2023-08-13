# -*- coding: utf-8 -*-

import pyglet.gl

from src.constants import (MAZE_START_IMAGE,
                           MAZE_TILE_PX_SIZE,
                           MAZE_TILES_ROWS,
                           MAZE_START_IMAGE_EMPTY_TILE_REGION_COORDS,
                           PACMAN_MOVE_ANIMATION,
                           PACMAN_DEATH_ANIMATION,
                           PACMAN_GHOSTS_SPRITES_PX_SIZE,
                           PACMAN_MOVE_ANIMATION_PERIOD_SECS,
                           PACMAN_DEATH_ANIMATION_PERIOD_SECS,
                           PacManStates,
                           PACMAN_SPAWNING_FRAME_IDX,
                           FontColors,
                           GAME_HIGH_SCORE_TEXT_COORDS,
                           GAME_1UP_TEXT_COORDS,
                           GAME_SCORE_NUMBER_COORDS,
                           GAME_HIGH_SCORE_NUMBER_COORDS,
                           MAX_SCORE_NUM_DIGITS,
                           GAME_DEFAULT_TEXT_COLOR,
                           UI_TILES_SHEET_PATH,
                           UI_TILES_PX_SIZE,
                           Fruits,
                           LIFE_ICON_UI,
                           GAME_LEFT_LIVES_ICON_COORDS,
                           GAME_RIGHT_FRUIT_ICON_COORDS,
                           GAME_MAX_FRUIT_ICON_NUMBER,
                           FRUIT_OF_LEVEL)
from src.directions import Vector2
from src.graphics import utils
from src.graphics.font import Font



class Painter:
    
    def __init__(self):
        
        # Load initial maze image.
        self._maze_image = utils.load_image(MAZE_START_IMAGE)
        self._maze_empty_tile = self._maze_image.get_region(*MAZE_START_IMAGE_EMPTY_TILE_REGION_COORDS, MAZE_TILE_PX_SIZE, MAZE_TILE_PX_SIZE)
        
        # Load animated sprites.
        self._pacman_move_sprite  = utils.load_animated_sprite(PACMAN_MOVE_ANIMATION , PACMAN_GHOSTS_SPRITES_PX_SIZE, PACMAN_MOVE_ANIMATION_PERIOD_SECS)
        self._pacman_death_sprite = utils.load_animated_sprite(PACMAN_DEATH_ANIMATION, PACMAN_GHOSTS_SPRITES_PX_SIZE, PACMAN_DEATH_ANIMATION_PERIOD_SECS)

        # Load UI elements.
        self._font = Font()
        self._ui_tiles = utils.load_image_grid(UI_TILES_SHEET_PATH, UI_TILES_PX_SIZE)



    def draw_menu(self):
        # TODO: better menu
        image = utils.load_image(r".\assets\images\TMP-Menu.png")

        image.blit(0, 0)


    def draw_game(self, pacman, ghosts, score, lives, level):

        self._draw_maze()

        self._draw_gui(score, lives, level)

        self._draw_pacman(pacman)

        self._draw_ghosts(ghosts)


        # ----------------------------------------
        # DEBUG
        # ----------------------------------------
        pacman_coords = utils.calculate_coords_sprites(pacman.position)

        for c in range(-160, 160, 8):
            pyglet.shapes.Line(c, -160, c, 160, width=1, color=(155, 0, 0)).draw()
            pyglet.shapes.Line(-160, c-4, 160, c-4, width=1, color=(155, 0, 0)).draw()
        pyglet.shapes.Circle(pacman_coords.x, pacman_coords.y, 2, color = (0, 155, 0)).draw()
        
        origin = utils.calculate_coords_sprites(Vector2(0, 0))
        pyglet.shapes.Circle(origin.x, origin.y, 2, color = (255, 0, 0)).draw()

        try:
            coll_box_coords = utils.calculate_coords_sprites(pacman.collision_point)
            pyglet.shapes.Circle(coll_box_coords.x, coll_box_coords.y, 2, color = (0, 155, 155)).draw()
        except:
            pass
      
        # ----------------------------------------


    def _draw_maze(self):
        self._maze_image.blit(0, 0)



    def _draw_pacman(self, pacman):
        # Convert in-game coordinates to render space coordinates.
        pacman_coords = utils.calculate_coords_sprites(pacman.position)

        # Determine rotation of Pac-Man sprite (only used for movement sprite).
        match pacman.direction:
            case Vector2.LEFT:
                rotation = 180
            case Vector2.UP:
                rotation = -90
            case Vector2.DOWN:
                rotation = 90
            case Vector2.RIGHT:
                rotation = 0
            case _:
                raise ValueError('Unvalid direction provided for Pac-Man to Painter')

        match pacman.state:
            case PacManStates.STUCK:
                # Freeze the animation, as long as Pac-Man is not a full yellow circle.
                if self._pacman_move_sprite.frame_index != PACMAN_SPAWNING_FRAME_IDX:
                    self._pacman_move_sprite.paused = True

                # Draw correct sprite.
                self._pacman_move_sprite.update(x=pacman_coords.x, y=pacman_coords.y, rotation=rotation)
                self._pacman_move_sprite.draw()

            case PacManStates.SPAWNING:
                # Freeze the animation on the correct frame.
                utils.freeze_animated_sprite(self._pacman_move_sprite, PACMAN_SPAWNING_FRAME_IDX)

                # Draw correct sprite.
                self._pacman_move_sprite.update(x=pacman_coords.x, y=pacman_coords.y, rotation=rotation)
                self._pacman_move_sprite.draw()

            case PacManStates.MOVING | PacManStates.TURNING:
                # Unfreeze the animation (this is silently ignored if paused property was already false).
                self._pacman_move_sprite.paused = False

                # Draw correct sprite.
                self._pacman_move_sprite.update(x=pacman_coords.x, y=pacman_coords.y, rotation=rotation)
                self._pacman_move_sprite.draw()

            case PacManStates.DEAD:
                # Unfreeze the animation (this is silently ignored if paused property was already false).
                self._pacman_death_sprite.paused = False

                # Draw correct sprite.
                self._pacman_death_sprite.update(x=pacman_coords.x, y=pacman_coords.y, rotation=0)
                self._pacman_death_sprite.draw()
            
            case _:
                raise ValueError('Unvalid state provided for Pac-Man to Painter')


    def _draw_gui(self, score, lives, level):
        # Print text on top of screen.
        self._font.print(*GAME_HIGH_SCORE_TEXT_COORDS, GAME_DEFAULT_TEXT_COLOR, 'HIGH SCORE')
        self._font.print(*GAME_1UP_TEXT_COORDS       , GAME_DEFAULT_TEXT_COLOR, '1UP')
        
        # Print score and high score numbers.
        high_score = score.high_score
        score      = score.score

        high_score = (''   if high_score == 0 else str(high_score)).rjust(MAX_SCORE_NUM_DIGITS, ' ')
        score      = ('00' if score      == 0 else str(score))     .rjust(MAX_SCORE_NUM_DIGITS, ' ')
        
        self._font.print(*GAME_HIGH_SCORE_NUMBER_COORDS, GAME_DEFAULT_TEXT_COLOR, high_score)
        self._font.print(*GAME_SCORE_NUMBER_COORDS     , GAME_DEFAULT_TEXT_COLOR, score)

        # Draw the lives.
        x, y = GAME_LEFT_LIVES_ICON_COORDS
        for _ in range(lives):
            self._ui_tiles[LIFE_ICON_UI].blit(x, y)
            x += UI_TILES_PX_SIZE

        # Draw the fruits.
        fruits = [FRUIT_OF_LEVEL(i) for i in range(level-GAME_MAX_FRUIT_ICON_NUMBER+1, level+1) if i >= 1]
        x, y = GAME_RIGHT_FRUIT_ICON_COORDS
        for fruit in fruits:
            self._ui_tiles[fruit].blit(x, y)
            x -= UI_TILES_PX_SIZE
            

    def _draw_ghosts(self, ghosts):
        for name, ghost in ghosts:

            from src.constants import Ghost
            colors = {Ghost.BLINKY: (255, 0, 0), Ghost.PINKY: (255, 183, 255), Ghost.INKY: (0, 255, 255), Ghost.CLYDE: (255, 183, 81)}
            ghost_center = utils.calculate_coords_sprites(ghost.position)
            pyglet.shapes.Circle(ghost_center.x, ghost_center.y, 5, color = colors[name]).draw()

        # --------------
        # Debug
        # --------------
        from src.constants import GHOSTS_SCATTER_MODE_TARGET_TILES, GHOSTS_EATEN_TARGET_TILE
        for name, tile_position in GHOSTS_SCATTER_MODE_TARGET_TILES.items():
            tile_position = utils.calculate_coords_sprites(tile_position)
            pyglet.shapes.Star(tile_position.x, tile_position.y, 5, 2, 4, color = colors[name]).draw()
        tile_position = utils.calculate_coords_sprites(GHOSTS_EATEN_TARGET_TILE)
        pyglet.shapes.Star(tile_position.x, tile_position.y, 5, 2, 4, color = (0, 255, 0)).draw()


        # --------------



    def set_empty_tile(self, idx):
        maze_row, maze_col = idx

        destination_left_px   = maze_col * MAZE_TILE_PX_SIZE
        destination_bottom_px = (MAZE_TILES_ROWS - maze_row - 1) * MAZE_TILE_PX_SIZE

        source_texture      = self._maze_empty_tile.get_texture()
        destination_texture = self._maze_image.get_texture()

        pyglet.gl.glCopyImageSubData(source_texture.id,
 	                                 source_texture.target,
 	                                 source_texture.level,
                                     0,
                                     0,
                                     0,
                                     destination_texture.id,
                                     destination_texture.target,
                                     destination_texture.level,
                                     destination_left_px, 
                                     destination_bottom_px,
                                     0,
                                     source_texture.width,
                                     source_texture.height,
                                     1)