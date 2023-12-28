
# https://github.com/davudk/OpenGL-TileMap-Demos/blob/master/Renderers/GeometryRenderer.cs

# https://learnopengl.com/Getting-started/Coordinate-Systems





def glCheckError():
    errorcode = pyglet.gl.glGetError()
        
    while errorcode != pyglet.gl.GL_NO_ERROR:
        
        code_to_string = {pyglet.gl.GL_INVALID_ENUM     : "INVALID_ENUM",
                          pyglet.gl.GL_INVALID_VALUE    : "INVALID_VALUE",
                          pyglet.gl.GL_INVALID_OPERATION: "GL_INVALID_OPERATION",
                          pyglet.gl.GL_STACK_OVERFLOW: "GL_STACK_OVERFLOW",
                          pyglet.gl.GL_STACK_UNDERFLOW: "GL_STACK_UNDERFLOW",
                          pyglet.gl.GL_OUT_OF_MEMORY: "GL_OUT_OF_MEMORY",
                          pyglet.gl.GL_INVALID_FRAMEBUFFER_OPERATION: "GL_INVALID_FRAMEBUFFER_OPERATION"}
        
        print(code_to_string[errorcode])
        errorcode = pyglet.gl.glGetError()
        

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

        self._program = self._build_shader_program()
        self._vlist   = self._create_vertex_list()


    def recalculate(self):
        self._vlist = self._create_vertex_list()


    def _build_shader_program(self):

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
        vertex_count = len(self._tilemap) * 6 # For each tile, 2 triangles, each with 3 vertices.
        
        vlist = self._program.vertex_list(vertex_count, pyglet.gl.GL_TRIANGLES)

        positions  = [0.0] * len(vlist.aPosition)
        tex_coords = [0.0] * len(vlist.aTexCoord)

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

    def draw(self):
        pyglet.gl.glBindTexture(pyglet.gl.GL_TEXTURE_2D, self._texture.id)

        # Input vertex coordinates have origin on the top left with x increasing as we go right and y increasing as we go down.
        # Each tile has a width and a height of 1.

        # Model matrix so that origin is at the center of the tilemap.
        # Tilemap x_range = (- N_COLS / 2, N_COLS / 2), y_range = (- N_ROWS / 2, N_ROWS / 2)
        model_matrix = pyglet.math.Mat4.from_translation(pyglet.math.Vec3(-N_COLS / 2, -N_ROWS / 2, 0))

        # View matrix should not change anything.
        view_matrix  = pyglet.math.Mat4()
        
        # Projection matrix scales so that tilemap fits tightly into clip-space: ranging from -1 to +1 in each coordinate.
        proj_matrix  = pyglet.math.Mat4.from_scale(pyglet.math.Vec3(2 / N_COLS, 2 / N_ROWS, 0))
        
        
        projection = proj_matrix @ view_matrix @ model_matrix
        
        pyglet.gl.glBindTexture(pyglet.gl.GL_TEXTURE_2D, self._texture.id)
        

        with self._program:
            self._vlist.projection = projection

            self._vlist.texture0 = self._texture.id

            self._vlist.draw(pyglet.gl.GL_TRIANGLES)






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

    def draw(self):
        pyglet.gl.glBindTexture(pyglet.gl.GL_TEXTURE_2D, self._texture.id)
        pyglet.gl.glBindVertexArray(self._vaoHandle)

        # Input vertex coordinates have origin on the top left with x increasing as we go right and y increasing as we go down.
        # Each tile has a width and a height of 1.

        # Model matrix so that origin is at the center of the tilemap.
        # Tilemap x_range = (- N_COLS / 2, N_COLS / 2), y_range = (- N_ROWS / 2, N_ROWS / 2)
        model_matrix = pyglet.math.Mat4.from_translation(pyglet.math.Vec3(-N_COLS / 2, -N_ROWS / 2, 0))

        # View matrix should not change anything.
        view_matrix  = pyglet.math.Mat4()
        
        # Projection matrix scales so that tilemap fits tightly into clip-space: ranging from -1 to +1 in each coordinate.
        proj_matrix  = pyglet.math.Mat4.from_scale(pyglet.math.Vec3(2 / N_COLS, 2 / N_ROWS, 0))
        
        
        projection = proj_matrix @ view_matrix @ model_matrix
        
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
        vertexData = (ctypes.c_float * len(vertexData))(*vertexData)

        pyglet.gl.glBufferData(pyglet.gl.GL_ARRAY_BUFFER, l * ctypes.sizeof(ctypes.c_float), vertexData, pyglet.gl.GL_STATIC_DRAW)

    def GenerateVertexArrayObject(self):
        arraid = pyglet.gl.GLuint()
        pyglet.gl.glGenVertexArrays(1, arraid)
        self._vaoHandle = arraid.value

        pyglet.gl.glBindVertexArray(self._vaoHandle)
        
        pyglet.gl.glBindBuffer(pyglet.gl.GL_ARRAY_BUFFER, self._vboHandle)
        
        pyglet.gl.glEnableVertexAttribArray(0)
        pyglet.gl.glVertexAttribPointer(0, 2, pyglet.gl.GL_FLOAT, False, ctypes.sizeof(ctypes.c_float) * 4, 0)

        pyglet.gl.glEnableVertexAttribArray(1)
        pyglet.gl.glVertexAttribPointer(1, 2, pyglet.gl.GL_FLOAT, False, ctypes.sizeof(ctypes.c_float) * 4, ctypes.sizeof(ctypes.c_float) * 2)

    def __del__(self):
        try:
            pyglet.gl.glDeleteVertexArrays(1, ctypes.c_ulong(self._vaoHandle))
            pyglet.gl.glDeleteBuffers(1, ctypes.c_ulong(self._vboHandle))
            pyglet.gl.glDeleteProgram(self._shaderHandle)
        except ImportError:
            pass





class GeomBufferedRenderer:

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

    def draw(self):
        pyglet.gl.glBindTexture(pyglet.gl.GL_TEXTURE_2D, self._texture.id)
        pyglet.gl.glBindVertexArray(self._vaoHandle)

        # Input vertex coordinates have origin on the top left with x increasing as we go right and y increasing as we go down.
        # Each tile has a width and a height of 1.

        # Model matrix so that origin is at the center of the tilemap.
        # Tilemap x_range = (- N_COLS / 2, N_COLS / 2), y_range = (- N_ROWS / 2, N_ROWS / 2)
        model_matrix = pyglet.math.Mat4.from_translation(pyglet.math.Vec3(-N_COLS / 2, -N_ROWS / 2, 0))

        # View matrix should not change anything.
        view_matrix  = pyglet.math.Mat4()
        
        # Projection matrix scales so that tilemap fits tightly into clip-space: ranging from -1 to +1 in each coordinate.
        proj_matrix  = pyglet.math.Mat4.from_scale(pyglet.math.Vec3(2 / N_COLS, 2 / N_ROWS, 0))
        
        
        projection = proj_matrix @ view_matrix @ model_matrix
        
        name = ctypes.create_string_buffer("projection".encode('utf-8'))
        uniform_location = pyglet.gl.glGetUniformLocation(self._shaderHandle, name)
        projection = (ctypes.c_float * len(projection))(*projection)
        
        pyglet.gl.glProgramUniformMatrix4fv(self._shaderHandle, uniform_location, 1, False, projection)
        
        name = ctypes.create_string_buffer("n_cols".encode('utf-8'))
        uniform_location = pyglet.gl.glGetUniformLocation(self._shaderHandle, name)
        pyglet.gl.glProgramUniform1i(self._shaderHandle, uniform_location, N_COLS)
        
        pyglet.gl.glUseProgram(self._shaderHandle)
        pyglet.gl.glDrawArrays(pyglet.gl.GL_POINTS, 0, len(self._tilemap))
        
        

    def CreateShader(self):
        # in this shader I have put the / 15 and % 15, replacing the use of mapSize !!!
        vert_source = """
                         #version 330 core

                         uniform int n_cols;

                         layout (location = 0) in uint aTileId;
 
                         out VS_OUT {
                             uint tileId;
                         } vs_out;

                         void main()
                         {
                             int i = gl_VertexID;
                             float x = float(int(i % n_cols));
                             float y = float(int(i / n_cols));
                             gl_Position = vec4(x, y, 0.0, 1.0);
                             
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
                              uint tileId = gs_in[0].tileId;
                              float tileX = float(tileId % {n_tiles_row_texture}) * {tile_tex_size} + {tile_tex_padding};
                              float tileY = float(tileId / {n_tiles_row_texture}) * {tile_tex_size} + {tile_tex_padding};

                              const float B = {tile_tex_padding};
                              const float S = {tile_tex_size} - 2 * {tile_tex_padding};

                              gl_Position = projection * gl_in[0].gl_Position;
                              texCoord = vec2(tileX, tileY);
                              EmitVertex();

                              gl_Position = projection * (gl_in[0].gl_Position + vec4(1.0, 0.0, 0.0, 0.0));
                              texCoord = vec2(tileX + S, tileY);
                              EmitVertex();

                              gl_Position = projection * (gl_in[0].gl_Position + vec4(0.0, 1.0, 0.0, 0.0));
                              texCoord = vec2(tileX, tileY + S);
                              EmitVertex();

                              gl_Position = projection * (gl_in[0].gl_Position + vec4(1.0, 1.0, 0.0, 0.0));
                              texCoord = vec2(tileX + S, tileY + S);
                              EmitVertex();

                              EndPrimitive();
                          }
                      """.replace('{n_tiles_row_texture}', str(N_TILES_ROW_TEXTURE)) \
                         .replace('{tile_tex_size}'      , str(TileTexSize)) \
                         .replace('{tile_tex_padding}'   , str(TileTexPadding)) \
                         .encode('utf8')
                                                                        
        handles = []
        for source, shader_type in [(vert_source, pyglet.gl.GL_VERTEX_SHADER),
                                    (frag_source, pyglet.gl.GL_FRAGMENT_SHADER),
                                    (geom_source, pyglet.gl.GL_GEOMETRY_SHADER)]:
            handle = pyglet.gl.glCreateShader(shader_type)
            handles.append(handle)
            source_buffer_pointer = ctypes.cast(ctypes.c_char_p(source), ctypes.POINTER(ctypes.c_char))
            pyglet.gl.glShaderSource(handle, 1, ctypes.byref(source_buffer_pointer), ctypes.c_int(len(source)))
            pyglet.gl.glCompileShader(handle)
            
            temp = ctypes.c_int(0)
            pyglet.gl.glGetShaderiv(handle, pyglet.gl.GL_COMPILE_STATUS, ctypes.byref(temp))
            if not temp:
                # retrieve the log length
                pyglet.gl.glGetShaderiv(handle, pyglet.gl.GL_INFO_LOG_LENGTH, ctypes.byref(temp))
                # create a buffer for the log
                buffer = ctypes.create_string_buffer(temp.value)
                # retrieve the log text
                pyglet.gl.glGetShaderInfoLog(handle, temp, None, buffer)
                # print the log to the console
                raise RuntimeError(buffer.value.decode())
                

        self._shaderHandle = pyglet.gl.glCreateProgram()
        
        for handle in handles:
            pyglet.gl.glAttachShader(self._shaderHandle, handle)
        pyglet.gl.glLinkProgram(self._shaderHandle)

        temp = ctypes.c_int(0)
		# retrieve the link status
        pyglet.gl.glGetProgramiv(self._shaderHandle, pyglet.gl.GL_LINK_STATUS, ctypes.byref(temp))
		# if linking failed, print the log
        if not temp:
			#   retrieve the log length
            pyglet.gl.glGetProgramiv(self._shaderHandle, pyglet.gl.GL_INFO_LOG_LENGTH, ctypes.byref(temp))
			# create a buffer for the log
            buffer = ctypes.create_string_buffer(temp.value)
			# retrieve the log text
            pyglet.gl.glGetProgramInfoLog(self._shaderHandle, temp, None, buffer)
			# print the log to the console
            raise RuntimeError(buffer.value.decode())

        for handle in handles:
            pyglet.gl.glDetachShader(self._shaderHandle, handle)
            pyglet.gl.glDeleteShader(handle)
        
        glCheckError()
        
        
    def GenerateVertexBufferObject(self):
        buffer_id = pyglet.gl.GLuint()
        pyglet.gl.glGenBuffers(1, buffer_id)
        self._vboHandle = buffer_id.value
        pyglet.gl.glBindBuffer(pyglet.gl.GL_ARRAY_BUFFER, self._vboHandle)

        vertexData = self._tilemap._map

        l = len(vertexData)
        vertexData = (ctypes.c_uint32 * len(vertexData))(*vertexData)

        pyglet.gl.glBufferData(pyglet.gl.GL_ARRAY_BUFFER, l * ctypes.sizeof(ctypes.c_uint32), vertexData, pyglet.gl.GL_STATIC_DRAW)
        glCheckError()


    def GenerateVertexArrayObject(self):
        arraid = pyglet.gl.GLuint()
        pyglet.gl.glGenVertexArrays(1, arraid)
        self._vaoHandle = arraid.value

        pyglet.gl.glBindVertexArray(self._vaoHandle)
        
        pyglet.gl.glBindBuffer(pyglet.gl.GL_ARRAY_BUFFER, self._vboHandle)
        
        pyglet.gl.glEnableVertexAttribArray(0)
        pyglet.gl.glVertexAttribIPointer(0, 1, pyglet.gl.GL_UNSIGNED_INT, ctypes.sizeof(ctypes.c_uint32), 0)
        glCheckError()


    def __del__(self):
        try:
            pyglet.gl.glDeleteVertexArrays(1, ctypes.c_ulong(self._vaoHandle))
            pyglet.gl.glDeleteBuffers(1, ctypes.c_ulong(self._vboHandle))
            pyglet.gl.glDeleteProgram(self._shaderHandle)
        except ImportError:
            pass