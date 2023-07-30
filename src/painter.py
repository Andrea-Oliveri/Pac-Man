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
                           ANIMATION_PERIOD_SECS,
                           PacManStates,
                           PACMAN_STUCK_FRAME_IDX,
                           PACMAN_SPAWNING_FRAME_IDX)
from src.utils import Vector2



class Painter:
    
    def __init__(self):
        
        # Load initial maze image.
        self._maze_image = self._load_image(MAZE_START_IMAGE)
        self._maze_empty_tile = self._maze_image.get_region(*MAZE_START_IMAGE_EMPTY_TILE_REGION_COORDS, MAZE_TILE_PX_SIZE, MAZE_TILE_PX_SIZE)
        
        # Load animated sprites.
        self._pacman_move_sprite  = self._load_animated_sprite(PACMAN_MOVE_ANIMATION , PACMAN_GHOSTS_SPRITES_PX_SIZE, ANIMATION_PERIOD_SECS)
        self._pacman_death_sprite = self._load_animated_sprite(PACMAN_DEATH_ANIMATION, PACMAN_GHOSTS_SPRITES_PX_SIZE, ANIMATION_PERIOD_SECS)


    def draw_menu(self):
        image = self._load_image(r"C:\Users\andre\Desktop\Python Pac-Man\assets\images\TMP-Menu.png")

        image.blit(0, 0)


    def draw_game(self, pacman):
        self._maze_image.blit(0, 0)

        self._draw_pacman(pacman)


        # ----------------------------------------
        # DEBUG
        # ----------------------------------------
        pacman_coords = self._calculate_coords_sprites(pacman.position)

        for c in range(-160, 160, 8):
            pyglet.shapes.Line(c, -160, c, 160, width=1, color=(155, 0, 0)).draw()
            pyglet.shapes.Line(-160, c-4, 160, c-4, width=1, color=(155, 0, 0)).draw()
        pyglet.shapes.Circle(pacman_coords.x, pacman_coords.y, 2, color = (0, 155, 0)).draw()
        
        origin = self._calculate_coords_sprites(Vector2(0, 0))
        pyglet.shapes.Circle(origin.x, origin.y, 2, color = (255, 0, 0)).draw()

        try:
            coll_box_coords = self._calculate_coords_sprites(pacman.collision_point_1)
            pyglet.shapes.Circle(coll_box_coords.x, coll_box_coords.y, 2, color = (0, 155, 155)).draw()
            coll_box_coords = self._calculate_coords_sprites(pacman.collision_point_2)
            pyglet.shapes.Circle(coll_box_coords.x, coll_box_coords.y, 2, color = (0, 155, 155)).draw()
        except:
            pass
      
        # ----------------------------------------



    def _draw_pacman(self, pacman):
        # Convert in-game coordinates to render space coordinates.
        pacman_coords = self._calculate_coords_sprites(pacman.position)

        # Determine rotation of Pac-Man sprite (only used for movement sprite).
        match pacman.direction:
            case Vector2.LEFT:
                rotation = 180
            case Vector2.UP:
                rotation = 90
            case Vector2.DOWN:
                rotation = -90
            case Vector2.RIGHT:
                rotation = 0
            case _:
                raise ValueError('Unvalid direction provided for Pac-Man to Painter')

        match pacman.state:
            case PacManStates.STUCK:
                # Freeze the animation on the correct frame.
                self._freeze_animated_sprite(self._pacman_move_sprite, PACMAN_STUCK_FRAME_IDX)

                # Draw correct sprite.
                self._pacman_move_sprite.update(x=pacman_coords.x, y=pacman_coords.y, rotation=rotation)
                self._pacman_move_sprite.draw()

            case PacManStates.SPAWNING:
                # Freeze the animation on the correct frame.
                self._freeze_animated_sprite(self._pacman_move_sprite, PACMAN_SPAWNING_FRAME_IDX)

                # Draw correct sprite.
                self._pacman_move_sprite.update(x=pacman_coords.x, y=pacman_coords.y, rotation=rotation)
                self._pacman_move_sprite.draw()

            case PacManStates.MOVING:
                # Unfreeze the animation (this is silently ignored if paused property was already false).
                self._pacman_move_sprite.paused = False

                # Draw correct sprite.
                self._pacman_move_sprite.update(x=pacman_coords.x, y=pacman_coords.y, rotation=rotation)
                self._pacman_move_sprite.draw()

            case PacManStates.DEAD:
                # Unfreeze the animation (this is silently ignored if paused property was already false).
                self.pacman_death_sprite.paused = False

                # Draw correct sprite.
                self.pacman_death_sprite.update(x=pacman_coords.x, y=pacman_coords.y, rotation=0)
                self.pacman_death_sprite.draw()
            
            case _:
                raise ValueError('Unvalid state provided for Pac-Man to Painter')


    def set_empty_tile(self, idx):
        maze_row = idx // MAZE_TILES_COLS
        maze_col = idx % MAZE_TILES_COLS

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
               
    @staticmethod
    def _calculate_coords_sprites(maze_coords):
        new_coords = Vector2(x = (- MAZE_TILES_COLS / 2 + maze_coords.x) * MAZE_TILE_PX_SIZE,
                             y = (+ MAZE_TILES_ROWS / 2 - maze_coords.y) * MAZE_TILE_PX_SIZE)
        return new_coords

    @staticmethod
    def _load_animated_sprite(path, tile_size_px, duration):
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
    def _load_image(path):
        image = pyglet.image.load(path)
        
        # Set anchor points to center.
        image.anchor_x = image.width // 2
        image.anchor_y = image.height // 2

        # Interpolate avoiding blur.
        texture = image.get_texture()
        pyglet.gl.glBindTexture(texture.target, texture.id)
        pyglet.gl.glTexParameteri(texture.target, pyglet.gl.GL_TEXTURE_MAG_FILTER, pyglet.gl.GL_NEAREST)

        return image

    @staticmethod
    def _freeze_animated_sprite(sprite, frame_index):
        sprite.paused = True
        sprite.frame_index = frame_index

        # Needed due to Pyglet issue #908 present in Pyglet version 2.0.8:
        # https://github.com/pyglet/pyglet/issues/906
        frame = sprite._animation.frames[sprite._frame_index]
        sprite._set_texture(frame.image.get_texture())

        if frame.duration is not None:
            sprite._next_dt = frame.duration

