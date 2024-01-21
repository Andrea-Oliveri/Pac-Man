#version 330 core


uniform sampler2D texture0;
in vec2 tex_coord;
out vec4 frag_color;

void main()
{
    vec4 tex_color = texture(texture0, tex_coord);

    // Discard fragments if fully transparent. This allows to work with both depth testing and transparency without depth sorting.
    if(tex_color.a == 0.0)
        discard;

    frag_color = tex_color;
}