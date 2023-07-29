# -*- coding: utf-8 -*-

import pyglet.image
import pyglet.gl

from src.constants import (MAZE_START_IMAGE,
                           MAZE_TILE_PX_SIZE,
                           MAZE_TILES_COLS,
                           MAZE_TILES_ROWS,
                           MAZE_START_IMAGE_EMPTY_TILE_REGION_COORDS,
                           PACMAN_MOVE_ANIMATION,
                           PACMAN_DEATH_ANIMATION,
                           PACMAN_GHOSTS_SPRITES_PX_SIZE,
                           ANIMATION_PERIOD_SECS)
from src.utils import Vector2



class Painter:
    
    def __init__(self):
        
        # Load initial maze image.
        self.maze_image = self.load_image(MAZE_START_IMAGE)
        self.maze_empty_tile = self.maze_image.get_region(*MAZE_START_IMAGE_EMPTY_TILE_REGION_COORDS, MAZE_TILE_PX_SIZE, MAZE_TILE_PX_SIZE)
        
        # Load animated sprites.
        self.pacman_move_sprite  = self.load_animated_sprite(PACMAN_MOVE_ANIMATION , PACMAN_GHOSTS_SPRITES_PX_SIZE, ANIMATION_PERIOD_SECS)
        self.pacman_death_sprite = self.load_animated_sprite(PACMAN_DEATH_ANIMATION, PACMAN_GHOSTS_SPRITES_PX_SIZE, ANIMATION_PERIOD_SECS)


    def draw_menu(self):
        image = self.load_image(r"C:\Users\andre\Desktop\Python Pac-Man\assets\images\TMP-Menu.png")

        image.blit(0, 0)


    def draw_game(self, pacman_maze_position, pacman_direction):
        self.maze_image.blit(0, 0)

        # Convert in-game coordinates to render space coordinates.
        pacman_position = self.calculate_coords_sprites(pacman_maze_position)

        # Determine rotation of Pac-Man sprite.
        if pacman_direction == Vector2.LEFT:
            rotation = 180
        elif pacman_direction == Vector2.UP:
            rotation = 90
        elif pacman_direction == Vector2.DOWN:
            rotation = -90
        elif pacman_direction == Vector2.RIGHT:
            rotation = 0
        else:
            raise ValueError('Unvalid direction provided for Pac-Man to Painter')

        # Update Pac-Man position and rotation.
        self.pacman_move_sprite.update(x=pacman_position.x, y=pacman_position.y, rotation=rotation)
        self.pacman_move_sprite.draw()

        for c in range(-160, 160, 8):
            pyglet.shapes.Line(c, -160, c, 160, width=1, color=(155, 0, 0)).draw()
            pyglet.shapes.Line(-160, c-4, 160, c-4, width=1, color=(155, 0, 0)).draw()
        pyglet.shapes.Circle(pacman_position.x, pacman_position.y, 2, color = (0, 155, 0)).draw()
      
   
    @staticmethod
    def calculate_coords_sprites(maze_coords):
        new_coords = Vector2(x = (- MAZE_TILES_COLS / 2 + maze_coords.x + 0.5) * MAZE_TILE_PX_SIZE,
                             y = (+ MAZE_TILES_ROWS / 2 - maze_coords.y - 0.5) * MAZE_TILE_PX_SIZE)
        return new_coords

    @staticmethod
    def load_animated_sprite(path, tile_size_px, duration):
        sprite_sheet = pyglet.image.load(path)

        n_rows = sprite_sheet.height // tile_size_px
        n_cols = sprite_sheet.width // tile_size_px

        image_grid = pyglet.image.ImageGrid(sprite_sheet, rows=n_rows, columns=n_cols)

        # Set anchor points to center and interpolate avoiding blur for every frame of animation.
        for image in image_grid:
            image.anchor_x = tile_size_px // 2
            image.anchor_y = tile_size_px // 2

            pyglet.gl.glBindTexture(pyglet.gl.GL_TEXTURE_2D, image.get_texture().id)
            pyglet.gl.glTexParameteri(pyglet.gl.GL_TEXTURE_2D, pyglet.gl.GL_TEXTURE_MAG_FILTER, pyglet.gl.GL_NEAREST)

        animation = pyglet.image.Animation.from_image_sequence(image_grid, duration=duration)
        sprite = pyglet.sprite.Sprite(img=animation)

        return sprite

    @staticmethod
    def load_image(path):
        image = pyglet.image.load(path)
        
        # Set anchor points to center.
        image.anchor_x = image.width // 2
        image.anchor_y = image.height // 2

        # Interpolate avoiding blur.
        pyglet.gl.glBindTexture(pyglet.gl.GL_TEXTURE_2D, image.get_texture().id)
        pyglet.gl.glTexParameteri(pyglet.gl.GL_TEXTURE_2D, pyglet.gl.GL_TEXTURE_MAG_FILTER, pyglet.gl.GL_NEAREST)

        return image


        

        


#def draw_text(message, font_size, color = COLORS["text"]):
#    """Function that returns a pygame.Surface containing the rendered text 
#    with message, size and color passed as parameters."""
#    return pygame.font.SysFont(FONT, font_size).render(message, True, color, COLORS["background"])













#import pyglet
#import os

#from src.constants.graphics import WINDOW_SIZE, COLORS, IMAGE_DIRECTORY, LOGO_IMAGE_NAME, ICON_IMAGE_NAME, CURSOR_IMAGE_NAME, MENU_LOGO_SURFACE_HEIGHT, MENU_TEXT_FONT_SIZE, MENU_TEXT_SURFACE_HEIGHT, MENU_CONTROLS_TEXT_FONT_SIZE
#from src.graphics import utils
#from src.graphics.regions.hold_region import HoldRegion
#from src.graphics.regions.grid_region import GridRegion
#from src.graphics.regions.queue_region import QueueRegion
#from src.graphics.regions.fps_region import FPSRegion
#from src.graphics.regions.level_region import LevelRegion
#from src.graphics.regions.score_region import ScoreRegion
#from src.graphics.regions.game_info_region import GameInfoRegion


#class Window:
#    """Class Window. Class dealing with all graphical output."""
    
#    def __init__(self):
#        """Constructor for the class Window."""
#        self._screen = pygame.display.set_mode(WINDOW_SIZE)
#        icon = pygame.image.load(os.path.join(IMAGE_DIRECTORY, ICON_IMAGE_NAME)).convert_alpha()
#        pygame.display.set_caption("Tetris")
#        pygame.display.set_icon(icon)

#        # Variable used to describe if the window was closed or not.
#        self._closed = False
            
#    def _get_closed(self):
#        """Getter for the attribute _closed."""
#        return self._closed
    
#    def close(self):
#        """method allowing to set the the value of _closed parameter to True."""
#        self._closed = True
        
#    """Definition of a properties for parameter _closed. This parameter can
#    only be get from the exteriour, not set nor deleted."""
#    closed = property(_get_closed)
        
        
#    def draw_menu(self, text_lines, idx_line_selected):
#        """Method drawing the main menu screen on the whole window."""
#        # Load logo and cursor assets.
#        logo = pygame.image.load(os.path.join(IMAGE_DIRECTORY, LOGO_IMAGE_NAME)).convert_alpha()
#        cursor = pygame.image.load(os.path.join(IMAGE_DIRECTORY, CURSOR_IMAGE_NAME)).convert_alpha()

#        # Convert color of menu cursor.
#        color_selected = COLORS['menu_text_selected']
#        width, height = cursor.get_size()
#        for col in range(width):
#            for line in range(height):
#                _, _, _, transparency = cursor.get_at((col, line))
#                cursor.set_at((col, line), (*color_selected, transparency))

#        # Generating text in menu.
#        text_surfaces = []
#        for idx, text in enumerate(text_lines):
#            text_surface = utils.draw_text(text, MENU_TEXT_FONT_SIZE, 
#                                           color = color_selected if idx == idx_line_selected else COLORS['text'])
#            text_surfaces.append(text_surface)
        
#        # Add cursor to selected line.
#        text_surfaces[idx_line_selected] = utils.merge_surfaces_horizontally([cursor, text_surfaces[idx_line_selected]], True)
        
#        ## Add padding to logo, cursor and text surfaces.
#        logo          = utils.merge_surfaces_vertically([logo], False, MENU_LOGO_SURFACE_HEIGHT)
#        text_surfaces = [utils.merge_surfaces_vertically([surface], False, MENU_TEXT_SURFACE_HEIGHT) for surface in text_surfaces]

#        whole_surface = utils.merge_surfaces_vertically([logo, *text_surfaces])
        
#        self._draw_whole_screen(whole_surface)
        
    
#    def draw_menu_controls(self, controls_lines):
#        """Method drawing the controls menu screen on the whole window."""        
#        keys_surfaces = []
#        text_surfaces = []
#        for text, key_files in controls_lines.items():
#            keys_surface = [pygame.image.load(os.path.join(IMAGE_DIRECTORY, key_file)).convert_alpha() for key_file in key_files]
            
#            keys_surfaces.append(utils.merge_surfaces_horizontally(keys_surface))
#            text_surfaces.append(utils.draw_text(text, MENU_CONTROLS_TEXT_FONT_SIZE))
            
#        whole_surface = utils.merge_surfaces_in_table(keys_surfaces, text_surfaces)
        
#        self._draw_whole_screen(whole_surface)  
        
        
#    def init_game(self):
#        """Method instanciating game screen regions as class attributes that will
#        then be called at each screen update."""        
#        self._hold_region = HoldRegion()
#        self._grid_region = GridRegion()
#        self._queue_region = QueueRegion()
#        self._fps_region   = FPSRegion()
#        self._level_region = LevelRegion()
#        self._score_region = ScoreRegion()
#        self._game_info_region = GameInfoRegion()
        
        
#    def end_game(self):
#        """Method deleting the game screen regions attributes.""" 
#        del self._hold_region
#        del self._grid_region
#        del self._queue_region
#        del self._fps_region
#        del self._level_region
#        del self._score_region
#        del self._game_info_region


#    def update_game(self, current_grid, current_tetrimino, queue, held, score,
#                    level, goal, lines, fps, show_fps, game_state_text):
#        """Window drawing the current game state on the whole window. Calls
#        game regions attributes to update themselves and then merges them together
#        into the whole frame."""
#        self._hold_region.update(held = held)
#        self._grid_region.update(current_grid = current_grid, current_tetrimino = current_tetrimino)
#        self._queue_region.update(queue = queue)
#        self._level_region.update(level = level, goal = goal, lines = lines)
#        self._score_region.update(score = score)
#        self._game_info_region.update(game_state_text = game_state_text)
        
#        surfaces_right_column = [self._queue_region.surface, self._level_region.surface]
#        if show_fps:
#            self._fps_region.update(fps = fps)
#            surfaces_right_column.append(self._fps_region.surface)

#        right_column = utils.merge_surfaces_vertically(surfaces_right_column, False)
#        central_column = utils.merge_surfaces_vertically([self._grid_region.surface, self._score_region.surface])
#        left_column = utils.merge_surfaces_vertically([self._hold_region.surface, self._game_info_region.surface])

#        whole_surface = utils.merge_surfaces_horizontally([left_column, central_column, right_column])
        
#        self._draw_whole_screen(whole_surface)
        
    
#    def _draw_whole_screen(self, surface):
#        """Clears the whole window screen and then blits the surface passed as parameter
#        in the window, centering it both horizontally and vertically."""
#        self._screen.fill(COLORS["background"])
#        self._screen.blit(surface, ((self._screen.get_width()-surface.get_width())/2,
#                                    (self._screen.get_height()-surface.get_height())/2))        
#        pygame.display.update()
   