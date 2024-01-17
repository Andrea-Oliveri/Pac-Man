#version 330 core


layout (location = 0) in float x_pos_center;
layout (location = 1) in float y_pos_center;
layout (location = 2) in float x_tex_left_px;
layout (location = 3) in float y_tex_bottom_px;
layout (location = 4) in float width_px;
layout (location = 5) in float height_px;
layout (location = 6) in float z_coord;

uniform float px_per_unit_lenght;
uniform int n_rows_grid;


out VS_OUT {
    float x_tex_left_px;
    float y_tex_bottom_px;
    float width_px;
    float height_px;
} vs_out;


void main()
{
    // Convert vertex so that grid has row 0 on the top instead of bottom and increases going down.
    vec2 new_pos_center = vec2(x_pos_center, n_rows_grid - y_pos_center);

    // Convert vertex from pointing to center into pointing to lower-left of quadrilater.
    vec2 pos_bottom_left = new_pos_center - (vec2(width_px, height_px) / px_per_unit_lenght) / 2;
    

    // Send attributes to geometry shader.
    gl_Position = vec4(pos_bottom_left, z_coord, 1.0);
    
    vs_out.x_tex_left_px   = x_tex_left_px;
    vs_out.y_tex_bottom_px = y_tex_bottom_px;
    vs_out.width_px        = width_px;
    vs_out.height_px       = height_px;
}