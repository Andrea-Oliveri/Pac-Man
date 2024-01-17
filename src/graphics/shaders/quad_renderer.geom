#version 330 core
                 
   
uniform int width_whole_tex_px;
uniform int height_whole_tex_px;
uniform float tex_padding;
uniform mat4 projection;
uniform float px_per_unit_lenght;


in VS_OUT {
    float x_tex_left_px;
    float y_tex_bottom_px;
    float width_px;
    float height_px;
} gs_in[];


out vec2 tex_coord;


layout (points) in;
layout (triangle_strip, max_vertices = 4) out;

void main() {
    float x_tex_left_norm   = float(gs_in[0].x_tex_left_px)   / width_whole_tex_px  + tex_padding;
    float y_tex_bottom_norm = float(gs_in[0].y_tex_bottom_px) / height_whole_tex_px + tex_padding;
    float width_norm        = float(gs_in[0].width_px)        / width_whole_tex_px  - (2 * tex_padding);
    float height_norm       = float(gs_in[0].height_px)       / height_whole_tex_px - (2 * tex_padding);
    float width_lenghts     = float(gs_in[0].width_px)        / px_per_unit_lenght;
    float height_lenghts    = float(gs_in[0].height_px)       / px_per_unit_lenght;

    // Bottom left vertex of quadrilateral.
    gl_Position = projection * gl_in[0].gl_Position;
    tex_coord = vec2(x_tex_left_norm, y_tex_bottom_norm);
    EmitVertex();

    // Bottom right vertex of quadrilateral.
    gl_Position = projection * (gl_in[0].gl_Position + vec4(width_lenghts, 0.0, 0.0, 0.0));
    tex_coord = vec2(x_tex_left_norm + width_norm, y_tex_bottom_norm);
    EmitVertex();


    // Top left vertex of quadrilateral.
    gl_Position = projection * (gl_in[0].gl_Position + vec4(0.0, height_lenghts, 0.0, 0.0));
    tex_coord = vec2(x_tex_left_norm, y_tex_bottom_norm + height_norm);
    EmitVertex();

    // Top right vertex of quadrilateral.
    gl_Position = projection * (gl_in[0].gl_Position + vec4(width_lenghts, height_lenghts, 0.0, 0.0));
    tex_coord = vec2(x_tex_left_norm + width_norm, y_tex_bottom_norm + height_norm);
    EmitVertex();

    EndPrimitive();
}