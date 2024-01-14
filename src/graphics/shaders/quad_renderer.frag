#version 330 core


uniform sampler2D texture0;
in vec2 tex_coord;
out vec4 frag_color;

void main()
{
    frag_color = texture(texture0, tex_coord);
}