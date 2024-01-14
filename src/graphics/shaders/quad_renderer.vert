#version 330 core


layout (location = 0) in float x_pos_center;
layout (location = 1) in float y_pos_center;
layout (location = 2) in float x_tex_left_px;
layout (location = 3) in float y_tex_bottom_px;
layout (location = 4) in float width_px;
layout (location = 5) in float height_px;
layout (location = 6) in float z_coord;


out VS_OUT {
    float x_tex_left_px;
    float y_tex_bottom_px;
    float width_px;
    float height_px;
} vs_out;


void main()
{
    vec2 pos_bottom_left = vec2(x, y) - (vec2(width_px, height_px) / 2);

    gl_Position = vec4(pos_bottom_left, z_coord, 1.0);
    
    vs_out.x_tex_left_px   = x_tex_left_px;
    vs_out.y_tex_bottom_px = y_tex_bottom_px;
    vs_out.width_px        = width_px;
    vs_out.height_px       = height_px;
}