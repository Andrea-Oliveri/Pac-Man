
# https://github.com/davudk/OpenGL-TileMap-Demos/blob/master/Renderers/GeometryRenderer.cs


import pyglet
import ctypes

TileSize = 8
N_TILES_ROW_TEXTURE = 32
TileTexSize = 1 / N_TILES_ROW_TEXTURE
TileTexPadding = 1 / 4096

N_ROWS = 36
N_COLS = 28


class VertexBufferedRendererPyglet:

    def __init__(self, tilemap):
        pyglet.gl.glClearColor(0.5, 0.5, 0.5, 1)
        pyglet.gl.glEnable(pyglet.gl.GL_BLEND)
        pyglet.gl.glBlendFunc(pyglet.gl.GL_SRC_ALPHA, pyglet.gl.GL_ONE_MINUS_SRC_ALPHA)

        self._tilemap = tilemap
        self._texture = self._tilemap._texture
        self._batch = pyglet.graphics.Batch()

        self._program = self._build_shader_program()
        self._vlist   = self._create_vertex_list()


    def recalculate(self):
        self._vlist   = self._create_vertex_list()


    def _build_shader_program(self):

        vert_source = """
                         #version 330 core

                         in vec2 aPosition;
                         in vec2 aTexCoord;
                         uniform mat4 projection;

                         out vec2 texCoord;

                         void main()
                         {
                             gl_Position = projection * vec4(aPosition, 0.0, 1.0);
                             texCoord = aTexCoord;
                         }
                      """

        frag_source = """
                         #version 330 core

                         out vec4 FragColor;
                         in vec2 texCoord;

                         uniform sampler2D texture0;

                         void main()
                         {
                             FragColor = texture(texture0, texCoord);
                         }
                      """

        vert_shader = pyglet.graphics.shader.Shader(vert_source, 'vertex')
        frag_shader = pyglet.graphics.shader.Shader(frag_source, 'fragment')
        program     = pyglet.graphics.shader.ShaderProgram(vert_shader, frag_shader)

        return program


    def _create_vertex_list(self):
        vlist = self._program.vertex_list(len(self._tilemap) * 6, pyglet.gl.GL_TRIANGLES, batch = self._batch)

        n_cells = len(vlist.aPosition)

        positions  = [0] * n_cells
        tex_coords = [0] * n_cells

        i = 0
        for x in range(N_COLS):
            for y in range(N_ROWS):

                tile = self._tilemap[y, x]

                tx = (tile %  N_TILES_ROW_TEXTURE) * TileTexSize + TileTexPadding
                ty = (tile // N_TILES_ROW_TEXTURE) * TileTexSize + TileTexPadding
                tySize = TileTexSize - TileTexPadding * 2

                # Vertex 0 (top left)
                positions [i + 0] = x
                positions [i + 1] = y
                tex_coords[i + 0] = tx
                tex_coords[i + 1] = ty
                i += 2

                # Vertex 1 (top right)
                positions [i + 0] = x + 1
                positions [i + 1] = y
                tex_coords[i + 0] = tx + tySize
                tex_coords[i + 1] = ty
                i += 2

                # Vertex 2 (bottom left)
                positions [i + 0] = x
                positions [i + 1] = y + 1
                tex_coords[i + 0] = tx
                tex_coords[i + 1] = ty + tySize
                i += 2

                # Vertex 3 (top right)
                positions [i + 0] = x + 1
                positions [i + 1] = y
                tex_coords[i + 0] = tx + tySize
                tex_coords[i + 1] = ty
                i += 2

                # Vertex 4 (bottom left)
                positions [i + 0] = x
                positions [i + 1] = y + 1
                tex_coords[i + 0] = tx
                tex_coords[i + 1] = ty + tySize
                i += 2

                # Vertex 5 (bottom right)
                positions [i + 0] = x + 1
                positions [i + 1] = y + 1
                tex_coords[i + 0] = tx + tySize
                tex_coords[i + 1] = ty + tySize
                i += 2

        vlist.aPosition[:] = positions
        vlist.aTexCoord[:] = tex_coords

        return vlist

    def draw(self, width, height):
        pyglet.gl.glBindTexture(pyglet.gl.GL_TEXTURE_2D, self._texture.id)

        with self._program:
            projection = pyglet.math.Mat4.from_translation(pyglet.math.Vec3(-1, 0, 0)) @ \
                        pyglet.math.Mat4.from_scale(pyglet.math.Vec3(TileSize, TileSize, 1)) @ \
                        pyglet.math.Mat4.from_scale(pyglet.math.Vec3(2 / width, 2 / height, 1))
            
            self._vlist.projection = projection
        self._batch.draw()






class VertexBufferedRenderer:

    def __init__(self, tilemap):
        
        pyglet.gl.glClearColor(0.5, 0.5, 0.5, 1)
        pyglet.gl.glEnable(pyglet.gl.GL_BLEND)
        pyglet.gl.glBlendFunc(pyglet.gl.GL_SRC_ALPHA, pyglet.gl.GL_ONE_MINUS_SRC_ALPHA)

        self._tilemap = tilemap
        self._texture = self._tilemap._texture
        self._shaderHandle = None
        self._vboHandle = None
        self._vaoHandle = None
        
        self.CreateShader()
        self.GenerateVertexBufferObject()
        self.GenerateVertexArrayObject()

    def recalculate(self):
        self.GenerateVertexBufferObject()
        self.GenerateVertexArrayObject()

    def draw(self, width, height):
        pyglet.gl.glBindTexture(pyglet.gl.GL_TEXTURE_2D, self._texture.id)
        pyglet.gl.glBindVertexArray(self._vaoHandle)

        projection = pyglet.math.Mat4.from_translation(pyglet.math.Vec3(0, 0, 0)) @ \
                     pyglet.math.Mat4.from_scale(pyglet.math.Vec3(TileSize, TileSize, 1)) @ \
                     pyglet.math.Mat4.from_scale(pyglet.math.Vec3(2 / width, 2 / height, 1))
        
        name = ctypes.create_string_buffer("projection".encode('utf-8'))
        uniform_location = pyglet.gl.glGetUniformLocation(self._shaderHandle, name)
        projection = (ctypes.c_float * len(projection))(*projection)
        
        pyglet.gl.glProgramUniformMatrix4fv(self._shaderHandle, uniform_location, 1, False, projection)
        
        pyglet.gl.glUseProgram(self._shaderHandle)
        pyglet.gl.glDrawArrays(pyglet.gl.GL_TRIANGLES, 0, len(self._tilemap) * 6)

    def CreateShader(self):
        vert_source = """
                         #version 330 core

                         layout (location = 0) in vec2 aPosition;
                         layout (location = 1) in vec2 aTexCoord;
                         uniform mat4 projection;

                         out vec2 texCoord;

                         void main()
                         {
                             gl_Position = projection * vec4(aPosition, 0.0, 1.0);
                             texCoord = aTexCoord;
                         }
                      """.encode("utf8")

        frag_source = """
                         #version 330 core

                         out vec4 FragColor;
                         in vec2 texCoord;

                         uniform sampler2D texture0;

                         void main()
                         {
                             FragColor = texture(texture0, texCoord);
                         }
                      """.encode("utf8")
            
        vertHandle = pyglet.gl.glCreateShader(pyglet.gl.GL_VERTEX_SHADER)
        source_buffer_pointer = ctypes.cast(ctypes.c_char_p(vert_source), ctypes.POINTER(ctypes.c_char))
        pyglet.gl.glShaderSource(vertHandle, 1, ctypes.byref(source_buffer_pointer), ctypes.c_int(len(vert_source)))
        pyglet.gl.glCompileShader(vertHandle)

        fragHandle = pyglet.gl.glCreateShader(pyglet.gl.GL_FRAGMENT_SHADER)
        source_buffer_pointer = ctypes.cast(ctypes.c_char_p(frag_source), ctypes.POINTER(ctypes.c_char))
        pyglet.gl.glShaderSource(fragHandle, 1, ctypes.byref(source_buffer_pointer), ctypes.c_int(len(frag_source)))
        pyglet.gl.glCompileShader(fragHandle)

        self._shaderHandle = pyglet.gl.glCreateProgram()

        pyglet.gl.glAttachShader(self._shaderHandle, vertHandle)
        pyglet.gl.glAttachShader(self._shaderHandle, fragHandle)
        pyglet.gl.glLinkProgram(self._shaderHandle)

        pyglet.gl.glDetachShader(self._shaderHandle, vertHandle)
        pyglet.gl.glDeleteShader(vertHandle)

        pyglet.gl.glDetachShader(self._shaderHandle, fragHandle)
        pyglet.gl.glDeleteShader(fragHandle)


    def GenerateVertexBufferObject(self):
        buffer_id = pyglet.gl.GLuint()
        pyglet.gl.glGenBuffers(1, buffer_id)
        self._vboHandle = buffer_id.value
        pyglet.gl.glBindBuffer(pyglet.gl.GL_ARRAY_BUFFER, self._vboHandle)

        floatCount = len(self._tilemap) * 6 * 2 * 2
        # for each tile
        # there are 6 vertices (two triangles, each with 3 vertices)
        # each vertex has two components: Position and Texcoord
        # each component has two fields: x and y

        vertexData = [0.0] * floatCount

        i = 0
        for x in range(N_COLS):
            for y in range(N_ROWS):
                tile = self._tilemap[y, x]

                tx0 = (tile %  N_TILES_ROW_TEXTURE) * TileTexSize + TileTexPadding
                ty0 = (tile // N_TILES_ROW_TEXTURE) * TileTexSize + TileTexPadding
                tySize = TileTexSize - TileTexPadding * 2

                # vertex 0 (top left)
                vertexData[i + 0] = x # position x
                vertexData[i + 1] = y # position y
                vertexData[i + 2] = tx0 # texcoord x
                vertexData[i + 3] = ty0 # texcoord y
                i += 4

                # vertex 1 (top right)
                vertexData[i + 0] = x + 1 # position x
                vertexData[i + 1] = y # position y
                vertexData[i + 2] = tx0 + tySize # texcoord x
                vertexData[i + 3] = ty0 # texcoord y
                i += 4

                # vertex 2 (bottom left)
                vertexData[i + 0] = x # position x
                vertexData[i + 1] = y + 1 # position y
                vertexData[i + 2] = tx0 # texcoord x
                vertexData[i + 3] = ty0 + tySize # texcoord y
                i += 4

                # vertex 3 (top right)
                vertexData[i + 0] = x + 1 # position x
                vertexData[i + 1] = y # position y
                vertexData[i + 2] = tx0 + tySize # texcoord x
                vertexData[i + 3] = ty0 # texcoord y
                i += 4

                # vertex 4 (bottom left)
                vertexData[i + 0] = x # position x
                vertexData[i + 1] = y + 1 # position y
                vertexData[i + 2] = tx0 # texcoord x
                vertexData[i + 3] = ty0 + tySize # texcoord y
                i += 4

                # vertex 5 (bottom right)
                vertexData[i + 0] = x + 1 # position x
                vertexData[i + 1] = y + 1 # position y
                vertexData[i + 2] = tx0 + tySize # texcoord x
                vertexData[i + 3] = ty0 + tySize # texcoord y
                i += 4


        l = len(vertexData)
        import struct
        vertexData = struct.pack('f'*len(vertexData), *vertexData)

        pyglet.gl.glBufferData(pyglet.gl.GL_ARRAY_BUFFER, l * 4, vertexData, pyglet.gl.GL_STATIC_DRAW)

    def GenerateVertexArrayObject(self):
        arraid = pyglet.gl.GLuint()
        pyglet.gl.glGenVertexArrays(1, arraid)
        self._vaoHandle = arraid.value

        pyglet.gl.glBindVertexArray(self._vaoHandle)
        
        pyglet.gl.glBindBuffer(pyglet.gl.GL_ARRAY_BUFFER, self._vboHandle)
        
        pyglet.gl.glEnableVertexAttribArray(0)
        pyglet.gl.glVertexAttribPointer(0, 2, pyglet.gl.GL_FLOAT, False, 4 * 4, 0)

        pyglet.gl.glEnableVertexAttribArray(1)
        pyglet.gl.glVertexAttribPointer(1, 2, pyglet.gl.GL_FLOAT, False, 4 * 4, 4 * 2)

    def __del__(self):
        return
        pyglet.gl.glDeleteVertexArrays(1, self._vaoHandle)
        pyglet.gl.glDeleteBuffer(self._vboHandle)
        pyglet.gl.glDeleteProgram(self._shaderHandle)





class GeomBufferedRenderer:

    def __init__(self, tilemap):
        
        pyglet.gl.glClearColor(0.5, 0.5, 0.5, 1)
        pyglet.gl.glClipControl(pyglet.gl.GL_UPPER_LEFT, pyglet.gl.GL_NEGATIVE_ONE_TO_ONE)
        pyglet.gl.glEnable(pyglet.gl.GL_BLEND)
        pyglet.gl.glBlendFunc(pyglet.gl.GL_SRC_ALPHA, pyglet.gl.GL_ONE_MINUS_SRC_ALPHA)

        self._tilemap = tilemap
        self._texture = self._tilemap._texture
        self._shaderHandle = None
        self._vboHandle = None
        self._vaoHandle = None
        
        self.CreateShader()
        self.GenerateVertexBufferObject()
        self.GenerateVertexArrayObject()

    def draw(self, width, height):
        pyglet.gl.glBindTexture(pyglet.gl.GL_TEXTURE_2D, self._texture.id)
        pyglet.gl.glBindVertexArray(self._vaoHandle)

        projection = pyglet.math.Mat4.from_translation(pyglet.math.Vec3(0, 0, 0)) @ \
                     pyglet.math.Mat4.from_scale(pyglet.math.Vec3(TileSize, TileSize, 1)) @ \
                     pyglet.math.Mat4.from_scale(pyglet.math.Vec3(2 / width, 2 / height, 1))
        
        name = ctypes.create_string_buffer("projection".encode('utf-8'))
        uniform_location = pyglet.gl.glGetUniformLocation(self._shaderHandle, name)
        projection = (ctypes.c_float * len(projection))(*projection)        
        pyglet.gl.glProgramUniformMatrix4fv(self._shaderHandle, uniform_location, 1, False, projection)

        #name = ctypes.create_string_buffer("mapSize".encode('utf-8'))
        #uniform_location = pyglet.gl.glGetUniformLocation(self._shaderHandle, name)
        #pyglet.gl.glProgramUniform2f(self._shaderHandle, uniform_location, N_COLS, N_ROWS)
        
        pyglet.gl.glUseProgram(self._shaderHandle)
        pyglet.gl.glDrawArrays(pyglet.gl.GL_POINTS, 0, len(self._tilemap))

    def CreateShader(self):
        # in this shader I have put the / 15 and % 15, replacing the use of mapSize !!!
        vert_source = """
                         #version 330 core

                         uniform mat4 projection;
                         uniform ivec2 mapSize;

                         layout (location = 0) in uint aTileId;

                         out VS_OUT {
                             uint tileId;
                         } vs_out;

                         void main()
                         {
                             int i = gl_VertexID;
                             float x = float(i / 15); //float(i & 15);
                             float y = float(i % 15); //float((i >> 4) & 15);
                             gl_Position = vec4(x, y, 0, 1);
                            
                             vs_out.tileId = aTileId;
                         }
                      """.encode("utf8")

        frag_source = """
                         #version 330 core

                         uniform sampler2D texture0;
                         in vec2 texCoord;
                         out vec4 FragColor;

                         void main()
                         {
                             FragColor = texture(texture0, texCoord);
                         }
                      """.encode("utf8")

        geom_source = """
                          #version 330 core

                          uniform mat4 projection;

                          in VS_OUT {
                              uint tileId;
                          } gs_in[];

                          out vec2 texCoord;

                          layout (points) in;
                          layout (triangle_strip, max_vertices = 4) out;

                          void main() {
                              uint tileId = gs_in[0].tileId & 255u;
                              float tileX = float(tileId & 15u) / 16.0;
                              float tileY = float((tileId >> 4u) & 15u) / 16.0;

                              const float B = 1 / 256.0;
                              const float S = 1 / 15.0;

                              gl_Position = projection * gl_in[0].gl_Position;
                              texCoord = vec2(tileX + B, tileY + B);
                              EmitVertex();

                              gl_Position = projection * (gl_in[0].gl_Position + vec4(1.0, 0.0, 0.0, 0.0));
                              texCoord = vec2(tileX + S - B, tileY + B);
                              EmitVertex();

                              gl_Position = projection * (gl_in[0].gl_Position + vec4(0.0, 1.0, 0.0, 0.0));
                              texCoord = vec2(tileX + B, tileY + S - B);
                              EmitVertex();

                              gl_Position = projection * (gl_in[0].gl_Position + vec4(1.0, 1.0, 0.0, 0.0));
                              texCoord = vec2(tileX + S - B, tileY + S - B);
                              EmitVertex();

                              EndPrimitive();
                          }  
                      """.encode('utf8')
        
        vertHandle = pyglet.gl.glCreateShader(pyglet.gl.GL_VERTEX_SHADER)
        source_buffer_pointer = ctypes.cast(ctypes.c_char_p(vert_source), ctypes.POINTER(ctypes.c_char))
        pyglet.gl.glShaderSource(vertHandle, 1, ctypes.byref(source_buffer_pointer), ctypes.c_int(len(vert_source)))
        pyglet.gl.glCompileShader(vertHandle)

        fragHandle = pyglet.gl.glCreateShader(pyglet.gl.GL_FRAGMENT_SHADER)
        source_buffer_pointer = ctypes.cast(ctypes.c_char_p(frag_source), ctypes.POINTER(ctypes.c_char))
        pyglet.gl.glShaderSource(fragHandle, 1, ctypes.byref(source_buffer_pointer), ctypes.c_int(len(frag_source)))
        pyglet.gl.glCompileShader(fragHandle)

        geomHandle = pyglet.gl.glCreateShader(pyglet.gl.GL_GEOMETRY_SHADER)
        source_buffer_pointer = ctypes.cast(ctypes.c_char_p(geom_source), ctypes.POINTER(ctypes.c_char))
        pyglet.gl.glShaderSource(geomHandle, 1, ctypes.byref(source_buffer_pointer), ctypes.c_int(len(geom_source)))
        pyglet.gl.glCompileShader(geomHandle)

        self._shaderHandle = pyglet.gl.glCreateProgram()

        pyglet.gl.glAttachShader(self._shaderHandle, vertHandle)
        pyglet.gl.glAttachShader(self._shaderHandle, fragHandle)
        pyglet.gl.glAttachShader(self._shaderHandle, geomHandle)
        pyglet.gl.glLinkProgram(self._shaderHandle)

        pyglet.gl.glDetachShader(self._shaderHandle, vertHandle)
        pyglet.gl.glDeleteShader(vertHandle)

        pyglet.gl.glDetachShader(self._shaderHandle, fragHandle)
        pyglet.gl.glDeleteShader(fragHandle)

        pyglet.gl.glDetachShader(self._shaderHandle, geomHandle)
        pyglet.gl.glDeleteShader(geomHandle)
        
        
    def GenerateVertexBufferObject(self):
        buffer_id = pyglet.gl.GLuint()
        pyglet.gl.glGenBuffers(1, buffer_id)
        self._vboHandle = buffer_id.value
        pyglet.gl.glBindBuffer(pyglet.gl.GL_ARRAY_BUFFER, self._vboHandle)

        vertexData = self._tilemap._map

        l = len(vertexData)
        import struct
        vertexData = struct.pack('f'*len(vertexData), *vertexData)

        pyglet.gl.glBufferData(pyglet.gl.GL_ARRAY_BUFFER, l * 4, vertexData, pyglet.gl.GL_STATIC_DRAW)


    def GenerateVertexArrayObject(self):
        arraid = pyglet.gl.GLuint()
        pyglet.gl.glGenVertexArrays(1, arraid)
        self._vaoHandle = arraid.value

        pyglet.gl.glBindVertexArray(self._vaoHandle)
        
        pyglet.gl.glBindBuffer(pyglet.gl.GL_ARRAY_BUFFER, self._vboHandle)
        
        pyglet.gl.glEnableVertexAttribArray(0)
        pyglet.gl.glVertexAttribPointer(0, 1, pyglet.gl.GL_UNSIGNED_INT, False, 4, 0)


    def __del__(self):
        return
        pyglet.gl.glDeleteVertexArrays(1, self._vaoHandle)
        pyglet.gl.glDeleteBuffer(self._vboHandle)
        pyglet.gl.glDeleteProgram(self._shaderHandle)
