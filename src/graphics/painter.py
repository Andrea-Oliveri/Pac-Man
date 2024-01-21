# -*- coding: utf-8 -*-

import array

import pyglet


from src.graphics import utils
from src.constants import (GRAPHICS_ATLAS_PATH, 
                           SHADERS_VERT_PATH,
                           SHADERS_GEOM_PATH,
                           SHADERS_FRAG_PATH,
                           SHADERS_TEX_PADDING,
                           SHADERS_MAX_QUADS,
                           LAYOUT_N_ROWS_TILES,
                           LAYOUT_N_COLS_TILES,
                           LAYOUT_PX_PER_UNIT_LENGHT)







class Painter:

    def __init__(self):
        self._default_atlas = utils.load_image(GRAPHICS_ATLAS_PATH)

        self._texture = None
        self._texture_width_px  = None
        self._texture_height_px = None

        self._shader_program = None
        self._vertex_list = None
        self._attributes_tmp_buffer = None
        self._attributes_tmp_buffer_idx = None

        self._create_shader()
        self._allocate_vertex_list()
        

    def _create_shader(self):
        shaders = []
        for path, shader_type in [(SHADERS_VERT_PATH, 'vertex'),
                                  (SHADERS_GEOM_PATH, 'geometry'),
                                  (SHADERS_FRAG_PATH, 'fragment')]:

            with open(path, 'r') as file:
                source = file.read()

            shader = pyglet.graphics.shader.Shader(source, shader_type)
            shaders.append(shader)
        
        self._shader_program = pyglet.graphics.shader.ShaderProgram(*shaders)


    @staticmethod
    def _get_projection_matrix():
        # Input vertex coordinates have origin on the top left with x increasing as we go right and y increasing as we go down.
        # Each quad has a width and a height equal to 1.

        return pyglet.math.Mat4.orthogonal_projection(0, LAYOUT_N_COLS_TILES, 0, LAYOUT_N_ROWS_TILES, +1, -1)
    


    def set_texture(self, image = None):
        if image is None:
            image = self._default_atlas

        # Store whole Texture class instance rather than just ID to avoid deallocation from destructor.
        self._texture = image.get_texture()
        self._texture_width_px  = image.width
        self._texture_height_px = image.height

        self._set_uniforms()



    def _set_uniforms(self):
        self._shader_program.use()

        self._shader_program['px_per_unit_lenght']  = LAYOUT_PX_PER_UNIT_LENGHT
        self._shader_program['n_rows_grid']         = LAYOUT_N_ROWS_TILES
        self._shader_program['width_whole_tex_px']  = self._texture_width_px
        self._shader_program['height_whole_tex_px'] = self._texture_height_px
        self._shader_program['tex_padding']         = SHADERS_TEX_PADDING
        self._shader_program['projection']          = self._get_projection_matrix()

        self._shader_program.stop()


    def _allocate_vertex_list(self):
        self._vertex_list = self._shader_program.vertex_list(SHADERS_MAX_QUADS, pyglet.gl.GL_POINTS)
        self._reset_attributes_tmp_buffer()


    def _reset_attributes_tmp_buffer(self):
        nan_list = [+float('inf')] * SHADERS_MAX_QUADS

        # Initialize local buffers to allow providing entire buffers to Pyglet's ShaderProgram.
        self._attributes_tmp_buffer = {name: array.array('f', nan_list) for name in self._shader_program.attributes.keys()}
        self._attributes_tmp_buffer_idx = 0


    def add_quad(self, x_pos_center, y_pos_center, x_tex_left_px, y_tex_bottom_px, width_px, height_px, z_coord):
        idx = self._attributes_tmp_buffer_idx
        self._attributes_tmp_buffer_idx += 1

        self._attributes_tmp_buffer['x_pos_center']   [idx] = x_pos_center
        self._attributes_tmp_buffer['y_pos_center']   [idx] = y_pos_center
        self._attributes_tmp_buffer['x_tex_left_px']  [idx] = x_tex_left_px
        self._attributes_tmp_buffer['y_tex_bottom_px'][idx] = y_tex_bottom_px
        self._attributes_tmp_buffer['width_px']       [idx] = width_px
        self._attributes_tmp_buffer['height_px']      [idx] = height_px
        self._attributes_tmp_buffer['z_coord']        [idx] = z_coord


    def draw(self):
        # Since we are using both depth testing and transparency, we would need to sort sort quads from furthest to closest to avoid artefacts.
        # Fortunately, by using only fully transparent or fully opaque objects, this can be avoided and dealth with in fragment shader.
        

        # Push buffers into ShaderProgram and reset them.
        for name, data in self._attributes_tmp_buffer.items():
            getattr(self._vertex_list, name)[:] = data
        self._reset_attributes_tmp_buffer()

        # Draw.
        self._shader_program.use()

        self._texture.bind()
        self._vertex_list.draw(pyglet.gl.GL_POINTS)

        self._shader_program.stop()